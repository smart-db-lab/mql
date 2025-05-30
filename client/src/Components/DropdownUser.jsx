import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { FaUserCircle } from 'react-icons/fa';
import apiRequest from '../Utility/api';
import Loader from './Loader/Loader';

const DropdownUser = () => {
    const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const navigate = useNavigate();
  const dropdownRef = useRef(null);

  // Close dropdown if clicked outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = async() => {
    const token = Cookies.get('token');
    const refresh = Cookies.get('refresh');
    setLoading(true);
    try{
    const response = await apiRequest(`${import.meta.env.VITE_LOGOUT_URL}`, 'POST' , token, { refresh_token:refresh });  
    if (response.success) {
      toast.success(response.message ||'Logout successful!');
      Cookies.remove('token');
      Cookies.remove('refresh');
      navigate('/signin');
    } 
  }catch(error){
    console.log(error);
  } finally{
    setLoading(false);
  }
  };

  return (
    <>
    {
        loading && <Loader />
    }
        <div className="relative" ref={dropdownRef}>
      {/* Profile Icon */}
      <button
        onClick={() => setOpen(!open)}
        className="text-2xl text-gray-700 dark:text-gray-300 hover:text-yellow-400"
        title="Account"
      >
        <FaUserCircle />
      </button>

      {/* Dropdown */}
      {open && (
        <div className="absolute right-0 mt-2 w-44 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md shadow-lg z-50">
          <Link
            to="/dashboard"
            onClick={() => setOpen(false)}
            className="block px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-200"
          >
            Dashboard
          </Link>
          <button
            onClick={handleLogout}
            className="block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 text-red-600 dark:text-red-400"
          >
            Logout
          </button>
        </div>
      )}
    </div>
    </>
  );
};

export default DropdownUser;
