import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ForgotPassword = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Send email to backend
    setMessage('Password reset instructions sent to your email.');
    console.log('Forgot password requested for:', email);
  };

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-8 border border-gray-200">
        <h2 className="text-3xl font-bold text-center text-gray-800 dark:text-white mb-6">
          Forgot Password
        </h2>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">
              Enter your registered email
            </label>
            <input
              type="email"
              required
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 rounded-lg transition"
          >
            Send Reset Link
          </button>
        </form>

        {message && (
          <p className="mt-4 text-sm text-green-600 dark:text-green-400 text-center">
            {message}
          </p>
        )}

        <p className="text-sm text-center text-gray-500 dark:text-gray-400 mt-6">
          Remembered your password?{' '}
          <button
            onClick={() => navigate('/signin')}
            className="text-blue-600 hover:underline"
          >
            Back to Sign In
          </button>
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;
