import React, { useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { FaSun, FaMoon, FaBars, FaTimes } from "react-icons/fa";
import useTheme from "../hooks/useTheme";
import Cookies from "js-cookie";
import DropdownUser from "./DropdownUser";

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isDark, setIsDark] = useTheme();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const isActive = (path) => location.pathname === path;

  useEffect(() => {
    const token = Cookies.get("token");
    setIsLoggedIn(!!token);
  }, [location.pathname]); // Refresh state on route change

  return (
    <div className="w-full border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm bg-white dark:bg-gray-900 dark:text-white">
      <div className="flex justify-between items-center px-2 py-1">
        {/* Logo */}
        <div className="cursor-pointer" onClick={() => navigate("/")}>
          <h1 className="font-mono font-bold tracking-tight text-3xl md:text-4xl">
            <span className="text-blue-500">M</span>
            <span className="text-orange-500">QL</span>
          </h1>
        </div>

        {/* Desktop Nav Links */}
        <ul className="hidden md:flex items-center gap-6 font-medium text-lg">
          {[
            { label: "Home", path: "/" },
            { label: "About Us", path: "/mql/about-us" },
            { label: "Contact Us", path: "/mql/contact" },
            { label: "Operations", path: "/mql/operation" },
          ].map((link) => (
            <li key={link.path}>
              <Link
                to={link.path}
                className={`transition-colors hover:text-blue-500 ${
                  isActive(link.path)
                    ? "text-blue-600 font-semibold underline"
                    : ""
                }`}
              >
                {link.label}
              </Link>
            </li>
          ))}
        </ul>

        {/* Right Side Buttons */}
        <div className="flex items-center gap-4">
          <button
            onClick={() => setIsDark(!isDark)}
            title={isDark ? "Light Mode" : "Dark Mode"}
            className="text-xl hover:text-yellow-400 transition"
          >
            {isDark ? <FaSun /> : <FaMoon />}
          </button>
          {isLoggedIn ? (
  <DropdownUser />
) : (
  <Link
    to="/signin"
    className="hidden md:block text-white border border-blue-600 rounded-lg bg-blue-800 px-4 py-2 hover:underline font-semibold"
  >
    Login / Sign Up
  </Link>
)}

          <button
            className="md:hidden text-2xl"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <FaTimes /> : <FaBars />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden px-6 pb-4 space-y-3">
          {[
            { label: "Home", path: "/" },
            { label: "About Us", path: "/mql/about-us" },
            { label: "Contact Us", path: "/mql/contact" },
            { label: "Operations", path: "/mql/operation" },
          ].map((link) => (
            <Link
              key={link.path}
              to={link.path}
              onClick={() => setMobileMenuOpen(false)}
              className={`block text-base font-medium hover:text-blue-500 ${
                isActive(link.path)
                  ? "text-blue-600 font-semibold underline"
                  : ""
              }`}
            >
              {link.label}
            </Link>
          ))}
          <Link
            to={isLoggedIn ? "/dashboard" : "/signin"}
            onClick={() => setMobileMenuOpen(false)}
            className="block w-full text-center bg-blue-700 hover:bg-blue-800 text-white rounded px-4 py-2 font-semibold"
          >
            {isLoggedIn ? "Dashboard" : "Login / Sign Up"}
          </Link>
        </div>
      )}
    </div>
  );
}

export default Navbar;
