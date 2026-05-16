import wikipediaapi, requests, os, re, time
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

load_dotenv()

class QueryList(BaseModel):
    queries: List[str]

wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='wikipedia-rag-chatbot/1.0'
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

query_llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.5
).with_structured_output(QueryList)

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.2
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=70
)

def split_by_sections(docs):
    split_docs = []

    for doc in docs:
        title = doc.metadata.get("title", "")

        # Split on Wikipedia headings
        sections = re.split(r"(==+.*?==+)", doc.page_content)

        current_heading = "Introduction"

        for part in sections:
            if re.match(r"==+.*?==+", part):
                current_heading = part.strip("=").strip()
            else:
                content = part.strip()

                if len(content) > 100:
                    split_docs.append(
                        Document(
                            page_content=content,
                            metadata={
                                "title": title,
                                "section": current_heading
                            }
                        )
                    )

    return split_docs

# Question -> Query prompt template
multi_query_prompt = ChatPromptTemplate.from_template("""
Generate 3 concise Wikipedia search queries for the question. Each query should explore a different conceptual angle. Avoid vague or generic wording.

Question:
{question}
""")

def generate_queries(question):
    result = (
        multi_query_prompt
        | query_llm
    ).invoke({"question": question})

    queries = result.queries[:3]

    def clean_query(q):
        q = q.replace('"', '')
        q = q.replace("Wikipedia", "")
        q = q.strip()
        return q[:100]

    return [clean_query(q) for q in queries]

wiki_cache = {}

# Multi-Query Retriever
def wiki_retriever_multi(question):
    def safe_wikipedia_load(query):
        docs = []

        try:
            url = "https://en.wikipedia.org/w/api.php"

            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": 5
            }

            headers = {"User-Agent": "wikipedia-rag-chatbot/1.0"}

            response = requests.get(url, params=params, headers=headers, timeout=10)
            data = response.json()
            search_results = data["query"]["search"]

            for result in search_results:
                title = result["title"]
                page = wiki.page(title)

                if page.exists():
                    docs.append(
                        Document(
                            page_content=page.text,
                            metadata={"title": page.title}
                        )
                    )

                time.sleep(0.2)

        except Exception as e:
            print(f"Wikipedia fetch failed: {e}")

        return docs

    queries = generate_queries(question)
    print(f"queries:\n{queries}\n")     # Print queries in the terminal

    all_docs = []
    seen_titles = set()

    # Fetch docs for each query
    for q in queries:
        docs = safe_wikipedia_load(q)

        # Deduplicate by title
        for doc in docs:
            title = doc.metadata.get("title", "")
            if title not in seen_titles:
                seen_titles.add(title)
                all_docs.append(doc)

    if not all_docs:
        raise ValueError("No Wikipedia documents retrieved.")

    # Chunk
    section_docs = split_by_sections(all_docs)
    splits = splitter.split_documents(section_docs)

    # Embed + MMR retrieval
    vectorstore = FAISS.from_documents(splits, embeddings)
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 15}
    )

    all_results = []

    for q in queries:
        results = retriever.invoke(q)
        all_results.extend(results)

    unique_chunks = {}

    for doc in all_results:
        key = doc.page_content[:200]

        if key not in unique_chunks:
            unique_chunks[key] = doc

    return list(unique_chunks.values())

# Final prompt template
final_prompt = ChatPromptTemplate.from_template("""
Answer the question using the retrieved Wikipedia context.

Rules:
- Use ONLY the provided context
- Combine information from multiple contexts when helpful
- Provide a complete but concise answer
- If information the retrieved Wikipedia context is incomplete, mention that clearly
- Do NOT invent unsupported facts

Context:
{context}

Question:
{question}
""")

# Format retrieved docs
def format_docs(docs):
    formatted_docs = "\n\n".join(
        f"[Article: {doc.metadata.get('title','')}]\n"
        f"[Section: {doc.metadata.get('section','Unknown')}]\n"
        f"{doc.page_content}"
        for doc in docs
    )
    print(f"formatted_docs:\n{formatted_docs}\n")   # Print formatted_docs in the terminal
    return formatted_docs

# RAG chain
rag_chain = (
    {"context": RunnablePassthrough() | wiki_retriever_multi | format_docs, "question": RunnablePassthrough()}
    | final_prompt
    | llm
    | StrOutputParser()
)

def ask_question(question):
    response = rag_chain.invoke(question)
    print(f"response:\n{response}\n")   # Print response in the terminal
    return response