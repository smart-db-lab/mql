import React from "react";

function AboutUs() {
  return (
    <div className="min-h-[90vh] flex items-center justify-center px-4">
      <div className="w-full max-w-3xl bg-white dark:bg-gray-800 p-10 rounded-2xl shadow-lg text-center font-secondary">
        {/* Logo & Title */}
        <h1 className="text-4xl font-bold font-mono tracking-tight text-gray-800 dark:text-white mb-2">
          <span className="text-blue-500">M</span>
          <span className="text-orange-500">QL</span>
        </h1>
        {/* <p className="text-gray-600 dark:text-gray-400 text-sm mb-6">
          Empowering Learners through Machine Learning & Deep Learning */}
        {/* </p> */}

        {/* Description */}
        <p className="text-gray-700 dark:text-gray-300 text-lg leading-relaxed mb-8">
          Machine Learning Query Language
        </p>

        {/* Mission & Vision
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-left text-gray-700 dark:text-gray-300">
          <div className="bg-gray-50 dark:bg-gray-700 p-5 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2 text-blue-600 dark:text-blue-400">🎯 Our Mission</h3>
            <p>
              To democratize AI education by offering simplified, hands-on, and structured learning resources for students and educators worldwide.
            </p>
          </div>
          <div className="bg-gray-50 dark:bg-gray-700 p-5 rounded-lg shadow">
            <h3 className="text-xl font-semibold mb-2 text-orange-500 dark:text-orange-400">🌐 Our Vision</h3>
            <p>
              To create a global community where learning, sharing, and building AI solutions becomes second nature for everyone.
            </p>
          </div>
        </div> */}

        {/* Contact Info */}
        {/* <div className="mt-8 text-center text-sm text-gray-600 dark:text-gray-400 space-y-2 text-left">
          <p>
            📍 <span className="font-medium">Location:</span> Comilla University, Bangladesh
          </p>
          <p>
            📧 <span className="font-medium">Email:</span> info@dl4ml.org
          </p>
          <p>
            ☎️ <span className="font-medium">Phone:</span> +880 1234 567 890
          </p>
        </div> */}

      </div>
    </div>
  );
}

export default AboutUs;
