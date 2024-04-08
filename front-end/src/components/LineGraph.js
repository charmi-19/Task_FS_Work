import React, { useEffect, useState } from "react";
import { LineChart, Line, CartesianGrid, XAxis, YAxis } from "recharts";

const LineGraph = ({ selectedOption }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5050/get/stats")
      .then((response) => response.json())
      .then((res) => {
        const newData = [];
        res.result.map((item) => {
          const dataEntry = {
            name: item.timestamp,
            noofhuman: Object.keys(item.data.instances).length,
          };
          const instances = Object.values(item.data.instances);
          let positions = 0.0;
          instances.map((pos) => {
            positions += pos.pos_x;
          });
          dataEntry["xposofhuman"] = positions / dataEntry.noofhuman;

          newData.push(dataEntry);
        });
        setData([...newData]);
      })
      .catch((error) => {
        console.log("error", error);
      });
  }, []);

  return (
    <LineChart width={1000} height={300} data={data}>
      <Line type="monotone" dataKey={selectedOption} stroke="#8884d8" />
      <CartesianGrid stroke="#ccc" strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
    </LineChart>
  );
};

export default LineGraph;
