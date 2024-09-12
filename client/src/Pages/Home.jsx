import React from "react";
import Navbar from "../Components/Navbar";

function Home() {
  return (
    <div>
      
      <div className="mt-16 max-w-3xl text-center mx-auto">
        <h1 className="font-primary font-black text-3xl mb-4 text-blue-950">
          Machine Learning Using Declarative Language
        </h1>
        <p className="font-secondary max-w-xl mx-auto text-gray-700 ">
          A Database Management Tools using ML
        </p>
        <img src="hero.gif" alt="" className="w-[500px] mx-auto" />
      </div>
    </div>
  );
}

export default Home;
