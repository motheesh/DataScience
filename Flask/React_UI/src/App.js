import React, { useEffect } from "react";
import Person from "./components/person/person";
function App() {
  useEffect(() => {
    document.title = "Flask API Project";
  }, []);
  return (
    <div className="container">
      <Person />
    </div>
  );
}

export default App;
