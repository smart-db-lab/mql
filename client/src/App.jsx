import React from "react";
import { Route, Routes, Navigate, useLocation } from "react-router-dom";
import "regenerator-runtime/runtime";
import { Toaster } from "react-hot-toast";

import Navbar from "./Components/Navbar";
import Footer from "./Components/Footer";
import Home from "./Pages/Home";
import AboutUs from "./Pages/AboutUs";
import Operations from "./Pages/Operations";
import SignupPage from "./Pages/SignupPage";
import LoginPage from "./Pages/LoginPage";
import ContactUs from "./Components/ContactUs";
import ForgotPassword from "./Pages/ForgotPassword";
import PrivateRoute from "./utility/PrivateRoute";
import ThemeProvider from "./utility/ThemeContext";
function App() {
  const location = useLocation();

  return (
    <ThemeProvider>
      <div className="p-6 px-8 dark:bg-gray-900 min-h-screen flex flex-col">
        <Toaster position="top-right" toastOptions={{ duration: 3000 }} />
        <Navbar />

        <main className="flex-grow">
          <Routes>
            <Route path="/mql" element={<Home />} />
            <Route path="/mql/about-us" element={<AboutUs />} />
            <Route path="/mql/contact" element={<ContactUs />} />
            <Route
              path="/mql/operation"
              element={
                <PrivateRoute>
                  <Operations />
                </PrivateRoute>
              }
            />
            <Route path="/signup" element={<SignupPage />} />
            <Route path="/signin" element={<LoginPage />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="*" element={<Navigate to="/mql" replace />} />
          </Routes>
        </main>

        {location.pathname !== "/mql/operation" && <Footer />}
      </div>
    </ThemeProvider>
  );
}

export default App;
