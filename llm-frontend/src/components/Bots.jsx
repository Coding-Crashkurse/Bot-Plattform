import React, { useEffect, useState } from "react";
import axios from "axios";

const Bots = ({ token }) => {
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
      } catch (err) {
        console.error("Failed to fetch user data:", err);
      }
    };

    fetchUserData();
  }, [token]);

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Your Bots</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {bots.map((bot) => (
          <div key={bot.id} className="card bg-base-100 shadow-xl">
            <figure>
              <img
                src={bot.image || "/bot.JPG"}
                alt={bot.name}
                style={{ width: "200px", height: "200px", objectFit: "cover" }}
              />
            </figure>
            <div className="card-body">
              <h3 className="card-title">{bot.name}</h3>
              <p>{bot.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Bots;
