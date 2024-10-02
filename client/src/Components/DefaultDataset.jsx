import React, { useEffect, useState } from "react";
import { Button, Spin } from "antd";
import toast from "react-hot-toast";
import axios from "axios";

const DefaultDataset = () => {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [dsloading, setDSLoading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loadingDataset, setLoadingDataset] = useState(null);

  useEffect(() => {
    const fetchDatasets = async () => {
      try {
        setLoading(true);
        const res = await axios.get("http://localhost:8000/datasets/");
        setDatasets(res.data.datasets);
        setLoading(false);
      } catch (error) {
        setLoading(false);
        console.error("Error fetching datasets:", error);
        toast.error("Failed to fetch datasets.");
      }
    };
    fetchDatasets();
  }, []);

  const handleSelectDataset = (fileName) => {
    setDSLoading(true);
    setLoadingDataset(fileName);
    axios
      .post("http://localhost:8000/set_datasets/", { file_name: fileName })
      .then((response) => {
        setSelectedDataset(fileName);
        toast.success("Dataset selected successfully.");
        setDSLoading(false);
      })
      .catch((error) => {
        console.error("There was an error processing the file:", error);
        toast.error("Failed to select dataset.");
        setDSLoading(false);
        setLoadingDataset(null);
      })
      .finally(() => {
        setDSLoading(false);
        setLoadingDataset(null);
      });
  };

  return (
    <>
      <div className="font-bold text-2xl border bg-slate-300 text-center rounded-lg mb-4">
        Default Dataset
      </div>
      {loading ? (
        <Spin />
      ) : (
        <div>
          {datasets.length === 0 ? (
            <div>No datasets available.</div>
          ) : (
            <ul className="list-none">
              {datasets.map((dataset, index) => (
                <li
                  key={index}
                  className="mb-2 flex justify-between border-b-2 mt-1 p-2"
                >
                  <span className="mr-4">{dataset}</span>
                  <Button
                    type={selectedDataset === dataset ? "default" : "default"}
                    onClick={() => handleSelectDataset(dataset)}
                  >
                    {loadingDataset === dataset && <Spin className="mr-3"/>}
                    {selectedDataset === dataset ? "Selected" : "Select"}
                  </Button>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </>
  );
};

export default DefaultDataset;