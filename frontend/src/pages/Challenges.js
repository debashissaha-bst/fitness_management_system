import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Challenges.css';
import API from '../services/api';

const Challenges = () => {
  const navigate = useNavigate();
  const [availableChallenges, setAvailableChallenges] = useState([]);
  const [userChallenges, setUserChallenges] = useState([]);
  const [activeTab, setActiveTab] = useState('available');

  useEffect(() => {
    loadAvailableChallenges();
    loadUserChallenges();
    // tasks removed
  }, []);

  const loadAvailableChallenges = async () => {
    try {
      const response = await API.get('/challenges');
      if (response.data.success) {
        setAvailableChallenges(response.data.challenges);
      }
    } catch (error) {
      console.error('Error loading challenges:', error);
    }
  };

  const loadUserChallenges = async () => {
    try {
      const response = await API.get('/user-challenges');
      if (response.data.success) {
        setUserChallenges(response.data.user_challenges);
      }
    } catch (error) {
      console.error('Error loading user challenges:', error);
    }
  };

  // tasks removed

  const handleJoinChallenge = async (challengeId) => {
    try {
      await API.post(`/challenges/${challengeId}/join`);
      alert('Successfully joined the challenge!');
      loadUserChallenges();
    } catch (error) {
      console.error('Error joining challenge:', error);
      alert('Error joining challenge');
    }
  };

  const handleCompleteDay = async (userChallengeId, day) => {
    try {
      await API.post(`/user-challenges/${userChallengeId}/complete-day`, { day });
      alert('Day completed successfully!');
      loadUserChallenges();
      loadAvailableChallenges();
    } catch (error) {
      console.error('Error completing day:', error);
      alert('Error completing day');
    }
  };

  // tasks removed

  // tasks removed

  const handleBack = () => {
    navigate('/home');
  };

  const renderAvailableChallenges = () => (
    <div className="challenges-grid">
      {availableChallenges.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🏃‍♂️</div>
          <h3>No Challenges Available</h3>
          <p>Check back later for new fitness challenges!</p>
        </div>
      ) : (
        availableChallenges.map((challenge) => (
          <div key={challenge._id} className="challenge-card available">
            <div className="challenge-header">
              <h3>{challenge.name}</h3>
              <span className="challenge-type">{challenge.challenge_type}</span>
            </div>
            <p className="challenge-description">{challenge.description}</p>
            <div className="challenge-details">
              <span className="duration">{challenge.duration_days} days</span>
              {challenge.difficulty && <span className="difficulty">{challenge.difficulty}</span>}
              {typeof challenge.xp_points === 'number' && <span className="xp">XP: {challenge.xp_points}</span>}
            </div>
            {challenge.completed ? (
              <button className="join-btn" disabled>
                Completed ✓
              </button>
            ) : challenge.joined ? (
              <button className="join-btn" disabled>
                Joined
              </button>
            ) : (
              <button 
                className="join-btn"
                onClick={() => handleJoinChallenge(challenge._id)}
              >
                Join Challenge
              </button>
            )}
          </div>
        ))
      )}
    </div>
  );

  const renderUserChallenges = () => (
    <div className="user-challenges-grid">
      {userChallenges.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📋</div>
          <h3>No Active Challenges</h3>
          <p>Join a challenge to get started!</p>
        </div>
      ) : (
        userChallenges.map((userChallenge) => (
          <div key={userChallenge._id} className="user-challenge-card">
            <div className="challenge-header">
              <h3>{userChallenge.challenge_name}</h3>
              <span className={`status ${userChallenge.completed ? 'completed' : 'active'}`}>
                {userChallenge.completed ? 'Completed' : 'Active'}
              </span>
            </div>
            <p className="challenge-description">{userChallenge.challenge_description}</p>
            <div className="progress-info">
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ 
                    width: `${(Object.values(userChallenge.progress).filter(Boolean).length / Object.keys(userChallenge.progress).length) * 100}%` 
                  }}
                ></div>
              </div>
              <span className="progress-text">
                {Object.values(userChallenge.progress).filter(Boolean).length} / {Object.keys(userChallenge.progress).length} days
              </span>
            </div>
            <div className="daily-progress">
              {Object.entries(userChallenge.progress).map(([day, completed]) => (
                <div 
                  key={day} 
                  className={`day-indicator ${completed ? 'completed' : ''}`}
                  onClick={() => !completed && handleCompleteDay(userChallenge._id, day)}
                  title={day}
                >
                  {completed ? '✓' : '○'}
                </div>
              ))}
            </div>
            {!userChallenge.completed && (
              <p className="challenge-tip">
                Click on the circles to mark days as completed!
              </p>
            )}
          </div>
        ))
      )}
    </div>
  );

  // tasks removed

  // tasks removed

  return (
    <div className="challenges-container">
      <div className="header">
        <button className="back-btn" onClick={handleBack}>
          ← Back to Home
        </button>
        <h1>Fitness Challenges</h1>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'available' ? 'active' : ''}`}
          onClick={() => setActiveTab('available')}
        >
          Available Challenges
        </button>
        <button 
          className={`tab ${activeTab === 'my-challenges' ? 'active' : ''}`}
          onClick={() => setActiveTab('my-challenges')}
        >
          My Challenges ({userChallenges.length})
        </button>
        {/* Tasks tab removed */}
      </div>

      <div className="content">
        {activeTab === 'available' && renderAvailableChallenges()}
        {activeTab === 'my-challenges' && renderUserChallenges()}
        {/* Tasks view removed */}
      </div>

      {/* Task form removed */}
    </div>
  );
};

export default Challenges;
