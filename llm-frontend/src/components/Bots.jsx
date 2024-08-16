import React, { useEffect, useState } from "react";
import axios from "axios";

const Bots = ({ token }) => {
  const [bots, setBots] = useState([]);
  const [selectedBotId, setSelectedBotId] = useState(null); // Change from array to single value

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

        // Default to selecting the first bot if available
        if (userBots.length > 0) {
          setSelectedBotId(userBots[0].id);
        }
      } catch (err) {
        console.error("Failed to fetch user data:", err);
      }
    };

    fetchUserData();
  }, [token]);

  const selectBot = (botId) => {
    setSelectedBotId(botId); // Set the selected bot ID
  };

  useEffect(() => {
    if (selectedBotId) {
      console.log(`Selected Bot ID: ${selectedBotId}`);
    }
  }, [selectedBotId]);

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Your Bots</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {bots.map((bot) => (
          <div
            key={bot.id}
            className={`card w-40 bg-base-100 shadow-xl cursor-pointer ${
              selectedBotId === bot.id ? "border-4 border-blue-500" : ""
            }`}
            onClick={() => selectBot(bot.id)}
          >
            <figure className="w-full h-40">
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
              <h3 className="card-title text-sm">{bot.name}</h3>
              <p className="text-xs">{bot.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Bots;
