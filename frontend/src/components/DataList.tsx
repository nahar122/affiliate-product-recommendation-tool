import React, { useState, useEffect } from "react";

interface DataItem {
  // Define the structure of your data item here
  id: number;
  domain: string;
  // other fields...
}

const DataList: React.FC = () => {
  const [data, setData] = useState<DataItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://localhost:5000/api/get-domains") // Replace with your Flask API endpoint
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      {data.map((item) => (
        <div key={item.id} className="flex flex-col text-left">
          {/* Render your data items here */}
          {item.domain}as
          {/* other fields... */}
        </div>
      ))}
    </div>
  );
};

export default DataList;
