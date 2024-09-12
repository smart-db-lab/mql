import React from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();
  return (
    <div className="flex items-center">
      <div className="cursor-pointer" onClick={() => navigate("/")}>
        <h1 className="font-[monospace] font-bold tracking-tight text-4xl">
          <span className="text-blue-500">M</span>
          <span className="text-orange-500">QL</span>
        </h1>
      </div>
      <ul className="flex items-center gap-4 font-secondary font-semibold text-lg w-full justify-end">
        <li>
          <Link
            to={"/operation"}
            className="hover:text-blue-400 hover:underline"
          >
            Operations
          </Link>
        </li>
        <li>
          <Link
            to={"/about-us"}
            className="hover:text-blue-400 hover:underline"
          >
            About Us
          </Link>
        </li>
      </ul>
    </div>
  );
}

export default Navbar;
