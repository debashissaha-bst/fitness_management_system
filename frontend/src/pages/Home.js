import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';
import main_logo from './images/fit_logo.png';
import API from '../services/api';

const Home = () => {
  const navigate = useNavigate();
  const [isLoggingOut, setIsLoggingOut] = useState(false);
  const [user] = useState({
    name: 'John Doe',
    profilePicture: null
  });

  const handleLogout = async () => {
    setIsLoggingOut(true);
    
    try {
      // Call the backend logout endpoint (Authorization header is automatically added)
      await API.post('/auth/logout');
      
      // Clear user session/token
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      // Dispatch custom logout event to notify App component
      window.dispatchEvent(new Event('logout'));
      
      // Show success message
      alert('Successfully logged out!');
      
      // Navigate to login page
      navigate('/login');
      
    } catch (error) {
      console.error('Logout error:', error);
      
      // Even if the API call fails, we should still log out locally
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      // Dispatch custom logout event to notify App component
      window.dispatchEvent(new Event('logout'));
      
      // Show message to user
      alert('Logged out successfully!');
      
      // Navigate to login page
      navigate('/login');
    } finally {
      setIsLoggingOut(false);
    }
  };

  const handleProfile = () => {
    navigate('/profile');
  };

  const handleMealPlans = () => {
    navigate('/meal-plans');
  };

  const handleBadges = () => {
    navigate('/badges');
  };

  const handleChallenges = () => {
    navigate('/challenges');
  };

  return (
    <div className="home-container">
      {/* Background Image */}
      <div className="background-image"></div>
      
      {/* Header */}
      <header className="header">
        <div className="header-content">
          {/* Logo Section */}
          <div className="logo-section">
            <div className="logo-image">
              <img src={main_logo} alt="AI Fitness" className="main-logo" />
            </div>
          </div>

          {/* Navigation Buttons */}
          <div className="nav-buttons">
            <button className="nav-button profile-btn" onClick={handleProfile}>
              Profile
            </button>
            <button 
              className={`nav-button logout-btn ${isLoggingOut ? 'loading' : ''}`} 
              onClick={handleLogout}
              disabled={isLoggingOut}
            >
              {isLoggingOut ? 'Logging out...' : 'Logout'}
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Welcome Section */}
        <div className="welcome-section">
          <div className="welcome-image">
            <div className="fitness-illustration">🏃‍♂️</div>
          </div>
        </div>

        {/* Feature Buttons */}
        <div className="feature-buttons">
          <button className="feature-btn meal-plans-btn" onClick={handleMealPlans}>
            <span className="feature-icon">🍽️</span>
            <span className="feature-text">Meal Planning</span>
          </button>
          
          <button className="feature-btn badges-btn" onClick={handleBadges}>
            <span className="feature-icon">🏆</span>
            <span className="feature-text">Badges & Progress</span>
          </button>
          
          <button className="feature-btn challenges-btn" onClick={handleChallenges}>
            <span className="feature-icon">🎯</span>
            <span className="feature-text">Fitness Challenges</span>
          </button>
        </div>
      </main>
    </div>
  );
};

export default Home; 