import React from 'react';
import { Link } from 'react-router-dom';
import { FaFacebookF, FaGithub, FaLinkedinIn, FaTwitter } from 'react-icons/fa';

const Footer = () => {
  return (
    <footer className="bg-white w-full dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 mt-16">
      <div className="mx-auto w-full px-6 py-10 flex flex-col md:flex-row justify-between items-start gap-8">
        {/* Logo & Description */}
        <div>
          <h2 className="text-3xl font-extrabold text-gray-800 dark:text-white">
            <span className="text-blue-500">M</span>
            <span className="text-orange-500">QL</span>
          </h2>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 max-w-xs">
            MQL empowers students and educators with insightful tools and learning solutions.
          </p>
        </div>

        {/* Social Icons */}
        <div className="flex gap-4 mt-4 md:mt-0">
          <a href="#" className="p-2 bg-gray-100 dark:bg-gray-800 text-blue-500 rounded-full hover:bg-blue-100 dark:hover:bg-gray-700 transition">
            <FaFacebookF size={16} />
          </a>
          <a href="#" className="p-2 bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition">
            <FaGithub size={16} />
          </a>
          <a href="#" className="p-2 bg-gray-100 dark:bg-gray-800 text-blue-700 rounded-full hover:bg-blue-100 dark:hover:bg-gray-700 transition">
            <FaLinkedinIn size={16} />
          </a>
          <a href="#" className="p-2 bg-gray-100 dark:bg-gray-800 text-sky-500 rounded-full hover:bg-sky-100 dark:hover:bg-gray-700 transition">
            <FaTwitter size={16} />
          </a>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="text-center text-gray-400 text-xs py-4 border-t border-gray-100 dark:border-gray-800 mt-4">
        &copy; {new Date().getFullYear()} MQL. All rights reserved.
      </div>
    </footer>
  );
};

export default Footer;
