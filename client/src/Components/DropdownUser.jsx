import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import { FaUserCircle } from 'react-icons/fa';
import apiRequest from '../Utility/api';
import Loader from './Loader/Loader';
import { removeToken, fetchWithAuth } from '../services/apiServices';
import { toast } from 'react-hot-toast';
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

  const handleLogout = async () => {
    setLoading(true);
    try {
        const url = `${import.meta.env.VITE_BACKEND_BASE_URL}${import.meta.env.VITE_LOGOUT_URL}`;
        const response = await fetchWithAuth(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh_token: Cookies.get('refresh_token') }),
        });
        const data = await response.json();
        if (response.ok && data.success) {
            toast.success(data.message || 'Logout successful!');
            removeToken();
            navigate('/signin');
        } else {
            toast.error(data.error || 'Logout failed!');
        }
    } catch (error) {
        console.error('Logout error:', error);
        toast.error('An error occurred during logout.');
    } finally {
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
