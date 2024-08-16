import React, { useState } from "react";
import Login from "./components/Login";
import Bots from "./components/Bots";
import Chat from "./components/Chat";

function App() {
  const [token, setToken] = useState(null);
  const [selectedBotId, setSelectedBotId] = useState(null);

  return (
    <div className="App">
      {!token ? (
        <Login setToken={setToken} />
      ) : (
        <>
          <Bots token={token} setSelectedBotId={setSelectedBotId} />
          <Chat token={token} selectedBotId={selectedBotId || 1} />
        </>
      )}
    </div>
  );
}

export default App;
