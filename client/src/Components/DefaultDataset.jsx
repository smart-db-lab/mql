import React, { useEffect, useState } from "react";
import { Button, Spin } from "antd";
import toast from "react-hot-toast";
import { listDatasets, setDataset } from "../services/apiServices";

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
        const res = await listDatasets();
        setDatasets(res.datasets);
        setLoading(false);
      } catch (error) {
        setLoading(false);
        toast.error("Failed to fetch datasets.");
      }
    };
    fetchDatasets();
  }, []);

  const handleSelectDataset = async (fileName) => {
    setDSLoading(true);
    setLoadingDataset(fileName);
    try {
      await setDataset(fileName);
      setSelectedDataset(fileName);
      toast.success("Dataset selected successfully.");
    } catch (error) {
      toast.error("Failed to select dataset.");
    } finally {
      setDSLoading(false);
      setLoadingDataset(null);
    }
  };

  return (
    <>
      <div className=" text-lg border bg-slate-200 text-center rounded-lg mb-4">
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
                  <span className="mr-4">{dataset.file || dataset}</span>
                  <Button
                    type={selectedDataset === (dataset.file || dataset) ? "default" : "default"}
                    onClick={() => handleSelectDataset(dataset.file || dataset)}
                  >
                    {loadingDataset === (dataset.file || dataset) && <Spin className="mr-3" />}
                    {selectedDataset === (dataset.file || dataset) ? "Selected" : "Select"}
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