import React from "react";
import { Route, Routes, Navigate } from "react-router-dom";
import "regenerator-runtime/runtime";
import Navbar from "./Components/Navbar";
import AboutUs from "./Pages/AboutUs";
import Home from "./Pages/Home";
import Operations from "./Pages/Operations";
import Sidebar from "./Components/Sidebar";

function App() {
  return (
    <div className="p-6 px-8">
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/mql" />} />
        <Route path="/mql" element={<Home />} />
        <Route path="/mql/operation" element={<Operations />} />
        <Route path="/mql/about-us" element={<AboutUs />} />
      </Routes>
    </div>
  );
}

export default App;
