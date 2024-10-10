
import { Button, Radio, Spin } from "antd";
import TextArea from "antd/es/input/TextArea";
import Upload from "antd/es/upload/Upload";
import React, { useState } from "react";
import toast, { Toaster } from "react-hot-toast";
import { BiText } from "react-icons/bi";
import { FaRegFileAudio } from "react-icons/fa6";
import DefaultDataset from "./DefaultDataset";
const Sidebar = () => {
  const [showSidebar, setShowSidebar] = useState(true); 

  return (
    <div className="bg-slate-300 h-full">
      {/* Sidebar for Default Dataset */}
      {showSidebar && (
        <div className="w-64 p-4">
          <h2 className="text-lg font-semibold mb-4">Default Dataset</h2>
          <DefaultDataset />
        </div>
      )}
      {/* Toggle button for Sidebar */}
      <div className="p-2 flex">
        <Button
          onClick={() => setShowSidebar(!showSidebar)}
          className="text-lg"
        >
          {showSidebar ? "←" : "→"}
        </Button>
      </div>
    </div>
  );
};

export default Sidebar;
