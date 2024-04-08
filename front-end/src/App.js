import React, { useState } from "react";
import LineGraph from "./components/LineGraph";

function App() {
  const [selectedOption, setSelectedOption] = useState("noofhuman");

  const handleSelectChange = (event) => {
    setSelectedOption(event.target.value);
  };

  return (
    <div className="container">
      <div className="dropdown-menu">
        <select
          id="dropdown"
          value={selectedOption}
          onChange={handleSelectChange}
        >
          <option value="noofhuman">Number of humans</option>
          <option value="xposofhuman">X position of human</option>
        </select>
      </div>
      <LineGraph selectedOption={selectedOption} />
    </div>
  );
}

export default App;
