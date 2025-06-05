import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiEye, FiEyeOff } from 'react-icons/fi';
import toast from 'react-hot-toast';
import Loader from '../Components/Loader/Loader';
import { login, setToken } from '../services/apiServices';

const LoginPage = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [loggedInUser, setLoggedInUser] = useState(null); // State to store logged-in user

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await login(username, password);
      setToken(response.access);
      setLoggedInUser(username); // Set the logged-in user
      toast.success('Login successful!');
      navigate('/mql');
    } catch (error) {
      const message =
        error?.non_field_errors?.[0] ||
        error?.error?.non_field_errors?.[0] ||
        error?.message ||
        'Invalid username or password';
      setError(message);
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {loading && <Loader />}

      <div className="min-h-[80vh] flex items-center justify-center px-4">
        <div className="w-full max-w-md bg-white text-gray-800 border border-gray-200 dark:bg-gray-800 rounded-2xl shadow-lg p-8">
          {loggedInUser ? (
            <h2 className="text-3xl font-bold text-center text-gray-800 dark:text-white mb-8">
              Login, {loggedInUser}! 🎉
            </h2>
          ) : (
            <h2 className="text-3xl font-bold text-center text-gray-800 dark:text-white mb-8">
              Login 
            </h2>
          )}

          {!loggedInUser && (
            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Username */}
              <div>
                <label className="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-200">
                  Username
                </label>
                <input
                  type="text"
                  className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="username"
                  value={username}
                  onChange={(e) => {
                    setUsername(e.target.value);
                    setError('');
                  }}
                  required
                />
              </div>

              {/* Password */}
              <div>
                <label className="block mb-1 text-sm font-medium text-gray-700 dark:text-gray-200">
                  Password
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500 pr-10"
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => {
                      setPassword(e.target.value);
                      setError('');
                    }}
                    required
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-3 flex items-center text-gray-500 dark:text-gray-300"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? <FiEyeOff /> : <FiEye />}
                  </button>
                </div>
              </div>

              {/* Error Message */}
              {error && <p className="text-sm text-red-500">{error}</p>}

              {/* Remember Me + Forgot Password */}
              <div className="flex items-center justify-between">
                <label className="inline-flex items-center text-sm text-gray-700 dark:text-gray-300">
                  <input
                    type="checkbox"
                    className="form-checkbox h-4 w-4 text-blue-600 rounded"
                    checked={remember}
                    onChange={(e) => setRemember(e.target.checked)}
                  />
                  <span className="ml-2">Remember me</span>
                </label>
                <a
                  href="/forgot-password"
                  className="text-sm text-blue-600 hover:underline"
                >
                  Forgot password?
                </a>
              </div>

              {/* Submit */}
              <button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 rounded-lg transition"
              >
                Sign In
              </button>
            </form>
          )}

          {/* Footer */}
          {!loggedInUser && (
            <p className="text-sm text-center text-gray-500 dark:text-gray-400 mt-6">
              Don&apos;t have an account?{' '}
              <a href="/signup" className="text-blue-600 hover:underline">
                Register
              </a>
            </p>
          )}
        </div>
      </div>
    </>
  );
};

export default LoginPage;
