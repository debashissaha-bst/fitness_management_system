import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Badges.css';
import API from '../services/api';

const Badges = () => {
  const navigate = useNavigate();
  const [badges, setBadges] = useState([]);
  const [milestones, setMilestones] = useState([]);
  const [progress, setProgress] = useState({
    level: 1,
    experience: 0,
    badges_count: 0,
    milestones_count: 0
  });
  const [activeTab, setActiveTab] = useState('progress');

  useEffect(() => {
    loadUserProgress();
    loadUserBadges();
    loadUserMilestones();
  }, []);

  const loadUserProgress = async () => {
    try {
      const response = await API.get('/progress');
      if (response.data.success) {
        setProgress(response.data.progress);
      }
    } catch (error) {
      console.error('Error loading progress:', error);
    }
  };

  const loadUserBadges = async () => {
    try {
      const response = await API.get('/badges');
      if (response.data.success) {
        setBadges(response.data.badges);
      }
    } catch (error) {
      console.error('Error loading badges:', error);
    }
  };

  const loadUserMilestones = async () => {
    try {
      const response = await API.get('/milestones');
      if (response.data.success) {
        setMilestones(response.data.milestones);
      }
    } catch (error) {
      console.error('Error loading milestones:', error);
    }
  };

  const handleBack = () => {
    navigate('/home');
  };

  const calculateProgressPercentage = () => {
    const currentLevel = progress.level;
    const currentExp = progress.experience;
    // const requiredExp = currentLevel * 100;
    const progressInLevel = currentExp % 100;
    return Math.min((progressInLevel / 100) * 100, 100);
  };

  const renderProgressCard = () => (
    <div className="progress-card">
      <div className="level-info">
        <div className="level-badge">
          <span className="level-number">{progress.level}</span>
          <span className="level-label">LEVEL</span>
        </div>
        <div className="experience-info">
          <h3>Experience Points</h3>
          <div className="exp-bar-container">
            <div className="exp-bar">
              <div 
                className="exp-fill" 
                style={{ width: `${calculateProgressPercentage()}%` }}
              ></div>
            </div>
            <span className="exp-text">
              {progress.experience % 100} / 100 XP
            </span>
          </div>
          <p className="total-exp">Total: {progress.experience} XP</p>
        </div>
      </div>
      
      <div className="stats-grid">
        <div className="stat-item">
          <div className="stat-icon">🏆</div>
          <div className="stat-content">
            <span className="stat-number">{progress.badges_count}</span>
            <span className="stat-label">Badges Earned</span>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <span className="stat-number">{progress.milestones_count}</span>
            <span className="stat-label">Milestones Reached</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderBadgesGrid = () => (
    <div className="badges-grid">
      {badges.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🏆</div>
          <h3>No Badges Yet</h3>
          <p>Complete tasks and challenges to earn your first badge!</p>
        </div>
      ) : (
        badges.map((badge, index) => (
          <div key={index} className="badge-card">
            <div className="badge-icon">{badge.icon}</div>
            <div className="badge-info">
              <h4 className="badge-name">{badge.name}</h4>
              <p className="badge-description">{badge.description}</p>
              <span className="badge-category">{badge.category}</span>
            </div>
            {badge.awarded_at && (
              <div className="badge-date">
                {new Date(badge.awarded_at).toLocaleDateString()}
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );

  const renderMilestonesGrid = () => (
    <div className="milestones-grid">
      {milestones.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">⭐</div>
          <h3>No Milestones Yet</h3>
          <p>Keep working hard to reach your first milestone!</p>
        </div>
      ) : (
        milestones.map((milestone, index) => (
          <div key={index} className="milestone-card">
            <div className="milestone-icon">{milestone.icon}</div>
            <div className="milestone-info">
              <h4 className="milestone-name">{milestone.name}</h4>
              <p className="milestone-description">{milestone.description}</p>
              <span className="milestone-category">{milestone.category}</span>
            </div>
            {milestone.awarded_at && (
              <div className="milestone-date">
                {new Date(milestone.awarded_at).toLocaleDateString()}
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );

  return (
    <div className="badges-container">
      <div className="header">
        <button className="back-btn" onClick={handleBack}>
          ← Back to Home
        </button>
        <h1>Achievements & Progress</h1>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${activeTab === 'progress' ? 'active' : ''}`}
          onClick={() => setActiveTab('progress')}
        >
          Progress
        </button>
        <button 
          className={`tab ${activeTab === 'badges' ? 'active' : ''}`}
          onClick={() => setActiveTab('badges')}
        >
          Badges ({progress.badges_count})
        </button>
        <button 
          className={`tab ${activeTab === 'milestones' ? 'active' : ''}`}
          onClick={() => setActiveTab('milestones')}
        >
          Milestones ({progress.milestones_count})
        </button>
      </div>

      <div className="content">
        {activeTab === 'progress' && renderProgressCard()}
        {activeTab === 'badges' && renderBadgesGrid()}
        {activeTab === 'milestones' && renderMilestonesGrid()}
      </div>
    </div>
  );
};

export default Badges;
