import React, { useState } from "react";
import axios from "axios";

const Chat = ({ token, selectedBotId }) => {
  const [messages, setMessages] = useState([
    { role: "system", content: "You are a helpful assistant." },
  ]);
  const [newMessage, setNewMessage] = useState("");

  const handleSendMessage = async () => {
    if (newMessage.trim() === "") return;

    const userMessage = { role: "user", content: newMessage };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setNewMessage("");

    // Log the request payload
    console.log("Request payload:", JSON.stringify(updatedMessages, null, 2));

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

      // Since response.data is a single object, you don't need to use map
      const botMessage = {
        role: response.data.role,
        content: response.data.content,
      };

      setMessages([...updatedMessages, botMessage]);
    } catch (error) {
      console.error("Failed to send message:", error);
    }
  };

  return (
    <div className="chat-container p-4">
      <div className="messages mb-4 p-4 bg-gray-100 rounded-md h-96 overflow-y-auto">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message p-2 mb-2 rounded-md ${
              message.role === "user"
                ? "bg-blue-200 text-right"
                : "bg-gray-200 text-left"
            }`}
          >
            {message.content}
          </div>
        ))}
      </div>
      <div className="message-input flex">
        <input
          type="text"
          className="input input-bordered flex-grow mr-2"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button className="btn btn-primary" onClick={handleSendMessage}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
