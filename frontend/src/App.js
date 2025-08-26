import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import Profile from './pages/Profile';
import MealPlans from './pages/MealPlans';
import Badges from './pages/Badges';
import Challenges from './pages/Challenges';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is authenticated (has token)
    const checkAuth = () => {
      const token = localStorage.getItem('token');
      setIsAuthenticated(!!token);
    };

    // Check authentication on mount
    checkAuth();

    // Listen for storage changes (when token is removed during logout)
    const handleStorageChange = (e) => {
      if (e.key === 'token') {
        checkAuth();
      }
    };

    window.addEventListener('storage', handleStorageChange);
    
    // Also listen for custom logout event
    const handleLogout = () => {
      setIsAuthenticated(false);
    };

    window.addEventListener('logout', handleLogout);

    return () => {
      window.removeEventListener('storage', handleStorageChange);
      window.removeEventListener('logout', handleLogout);
    };
  }, []);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={
            isAuthenticated ? <Navigate to="/home" replace /> : <Navigate to="/login" replace />
          } />
          <Route path="/login" element={
            isAuthenticated ? <Navigate to="/home" replace /> : <Login />
          } />
          <Route path="/register" element={
            isAuthenticated ? <Navigate to="/register" replace /> : <Register />
          } />
          <Route path="/home" element={
            isAuthenticated ? <Home /> : <Navigate to="/login" replace />
          } />
          <Route path="/profile" element={
            isAuthenticated ? <Profile /> : <Navigate to="/login" replace />
          } />
          <Route path="/meal-plans" element={
            isAuthenticated ? <MealPlans /> : <Navigate to="/login" replace />
          } />
          <Route path="/badges" element={
            isAuthenticated ? <Badges /> : <Navigate to="/login" replace />
          } />
          <Route path="/challenges" element={
            isAuthenticated ? <Challenges /> : <Navigate to="/login" replace />
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
