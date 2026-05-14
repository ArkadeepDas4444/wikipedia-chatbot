import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = {
      role: "user",
      text: message
    };

    setChat(prev => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: message
        })
      });

      const data = await response.json();

      const botMessage = {
        role: "bot",
        text: data.response
      };

      setChat(prev => [...prev, botMessage]);

    } catch (error) {
      setChat(prev => [
        ...prev,
        {
          role: "bot",
          text: error.message
        }
      ]);
    }

    setLoading(false);
    setMessage("");
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex justify-center p-6">

      <div className="w-full max-w-3xl">

        <h1 className="text-4xl font-bold mb-6 text-center">
          Wikipedia RAG Chatbot
        </h1>

        <div className="bg-zinc-900 rounded-2xl p-4 h-[70vh] overflow-y-auto shadow-lg">

          {chat.map((msg, index) => (

            <div
              key={index}
              className={`mb-4 flex ${
                msg.role === "user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >

              <div
                className={`max-w-[80%] px-4 py-3 rounded-2xl ${
                  msg.role === "user"
                    ? "bg-blue-600"
                    : "bg-zinc-800"
                }`}
              >
                {msg.text}
              </div>

            </div>
          ))}

          {loading && (
            <div className="text-zinc-400">
              Thinking...
            </div>
          )}

        </div>

        <div className="flex mt-4 gap-3">

          <input
            type="text"
            className="flex-1 bg-zinc-800 rounded-xl px-4 py-3 outline-none"
            placeholder="Ask a Wikipedia question..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />

          <button
            onClick={sendMessage}
            className="bg-blue-600 px-6 py-3 rounded-xl hover:bg-blue-700"
          >
            Send
          </button>

        </div>

      </div>

    </div>
  );
}

export default App;