import React, { useEffect, useState } from "react";
import axios from "axios";

const Bots = ({ token, selectedBotId, setSelectedBotId }) => {
  const [bots, setBots] = useState([]);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get("http://localhost:8000/users/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const userBots = response.data.bots || [];
        setBots(userBots);

        if (userBots.length > 0 && !selectedBotId) {
          setSelectedBotId(userBots[0].id);
        }
      } catch (err) {
        console.error("Failed to fetch user data:", err);
      }
    };

    fetchUserData();
  }, [token, selectedBotId, setSelectedBotId]);

  const selectBot = (botId) => {
    setSelectedBotId(botId);
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4 text-gray-700">Your Bots</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {bots.map((bot) => (
          <div
            key={bot.id}
            className={`card w-40 bg-white shadow-lg cursor-pointer transition-transform transform hover:scale-105 ${
              selectedBotId === bot.id
                ? "border-2 border-gray-500"
                : "border border-gray-300"
            }`}
            onClick={() => selectBot(bot.id)}
          >
            <figure className="w-full h-40 bg-gray-100">
              <img
                src={bot.image}
                alt={bot.name}
                className="w-full h-full object-cover"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = "/bot.JPG";
                }}
              />
            </figure>
            <div className="card-body p-2 flex flex-col items-center justify-center text-center">
              <h3 className="card-title text-sm text-gray-700">{bot.name}</h3>
              <p className="text-xs text-gray-500">{bot.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Bots;
