import React from 'react';
import { Navigate } from 'react-router-dom'; // ✅ needed for redirect
import { getToken } from '../services/apiServices';

const PrivateRoute = ({ children }) => {
  const token = getToken();
  const isAuthenticated = !!token;
  return isAuthenticated ? children : <Navigate to="/signin" replace />;
};

export default PrivateRoute;
