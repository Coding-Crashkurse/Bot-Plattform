import React, { useState } from "react";
import Login from "./components/Login";
import Bots from "./components/Bots";

function App() {
  const [token, setToken] = useState(null);

  return (
    <div className="App">
      {!token ? <Login setToken={setToken} /> : <Bots token={token} />}
    </div>
  );
}

export default App;
