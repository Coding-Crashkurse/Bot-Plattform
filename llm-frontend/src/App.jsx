import React, { useState } from "react";
import Login from "./components/Login";
import Bots from "./components/Bots";
import Chat from "./components/Chat";

function App() {
  const [token, setToken] = useState(null);
  const [selectedBotId, setSelectedBotId] = useState(null);

  return (
    <div className="App flex flex-col min-h-screen bg-gray-100">
      {!token ? (
        <Login setToken={setToken} />
      ) : (
        <div className="flex flex-col flex-grow">
          <div className="flex-grow">
            <Bots
              token={token}
              selectedBotId={selectedBotId}
              setSelectedBotId={setSelectedBotId}
            />
          </div>
          <div className="flex-none">
            <Chat token={token} selectedBotId={selectedBotId || 1} />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
