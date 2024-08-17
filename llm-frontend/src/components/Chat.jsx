import React, { useState } from "react";
import axios from "axios";

const Chat = ({ token, selectedBotId }) => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async () => {
    if (newMessage.trim() === "") return;

    const userMessage = { role: "user", content: newMessage };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setNewMessage("");
    setLoading(true);

    console.log(`SELECTED BOT: ${selectedBotId}`);

    try {
      const response = await axios.post(
        `http://localhost:8000/chat/${selectedBotId}`,
        updatedMessages,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("Response from server:", response.data);

      const botMessage = {
        role: response.data.role,
        content: response.data.content,
      };

      setMessages([...updatedMessages, botMessage]);
    } catch (error) {
      console.error("Failed to send message:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container p-4 bg-cover bg-center">
      {messages.length > 0 && (
        <div
          className="messages mb-4 p-4 bg-white bg-opacity-80 rounded-md overflow-y-auto shadow-lg"
          style={{ maxHeight: "60vh" }}
        >
          {messages.map((message, index) => (
            <div
              key={index}
              className={`chat ${
                message.role === "user" ? "chat-start" : "chat-end"
              }`}
            >
              <div
                className={`chat-bubble ${
                  message.role === "user"
                    ? "chat-bubble bg-gray-300 text-gray-900"
                    : "chat-bubble bg-gray-100 text-gray-700"
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="chat chat-end">
              <div className="chat-bubble bg-gray-100 text-gray-700">
                <div className="animate-pulse">
                  Typing<span className="dot">.</span>
                  <span className="dot">.</span>
                  <span className="dot">.</span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
      <div className="message-input flex">
        <input
          type="text"
          className="input input-bordered flex-grow mr-2"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button
          className="btn btn-neutral"
          onClick={handleSendMessage}
          disabled={loading}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
