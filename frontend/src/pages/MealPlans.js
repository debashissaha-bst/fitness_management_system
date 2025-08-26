import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './MealPlans.css';
import API from '../services/api';

const MealPlans = () => {
  const navigate = useNavigate();
  const [userPreferences, setUserPreferences] = useState(null);
  const [currentMealPlan, setCurrentMealPlan] = useState(null);
  const [mealHistory, setMealHistory] = useState([]);
  const [showPreferencesForm, setShowPreferencesForm] = useState(false);
  const [showMealPlan, setShowMealPlan] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [preferencesForm, setPreferencesForm] = useState({
    age_group: 'adult',
    dietary_preference: 'vegetarian',
    fitness_goal: 'stay_fit'
  });

  useEffect(() => {
    loadUserPreferences();
    loadMealHistory();
  }, []);

  const loadUserPreferences = async () => {
    try {
      const response = await API.get('/preferences');
      if (response.data.success) {
        setUserPreferences(response.data.preferences);
        setPreferencesForm({
          age_group: response.data.preferences.age_group,
          dietary_preference: response.data.preferences.dietary_preference,
          fitness_goal: response.data.preferences.fitness_goal
        });
      }
    } catch (error) {
      console.error('Error loading preferences:', error);
      // User doesn't have preferences yet
    }
  };

  const loadMealHistory = async () => {
    try {
      const response = await API.get('/meal-plans/history');
      if (response.data.success) {
        setMealHistory(response.data.meal_plans);
      }
    } catch (error) {
      console.error('Error loading meal history:', error);
    }
  };

  const handlePreferencesChange = (e) => {
    setPreferencesForm({
      ...preferencesForm,
      [e.target.name]: e.target.value
    });
  };

  const savePreferences = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await API.post('/preferences', preferencesForm);
      if (response.data.success) {
        setUserPreferences(response.data.preferences);
        setShowPreferencesForm(false);
        // Auto-generate meal plan after saving preferences
        await generateMealPlan();
      }
    } catch (error) {
      setError('Error saving preferences: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const generateMealPlan = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await API.post('/generate-meal-plan', {});
      if (response.data.success) {
        setCurrentMealPlan(response.data.meal_plan);
        setShowMealPlan(true);
        await loadMealHistory(); // Refresh history
      }
    } catch (error) {
      setError('Error generating meal plan: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    navigate('/home');
  };

  const renderPreferencesForm = () => (
    <div className="modal-overlay">
      <div className="modal preferences-modal">
        <h2>Set Your Preferences</h2>
        <p className="form-description">
          Tell us about yourself to get personalized meal recommendations
        </p>
        
        <form onSubmit={savePreferences}>
          <div className="form-group">
            <label>Age Group:</label>
            <select
              name="age_group"
              value={preferencesForm.age_group}
              onChange={handlePreferencesChange}
              required
            >
              <option value="young">Young (18-30)</option>
              <option value="adult">Adult (31-50)</option>
              <option value="older">Older (51+)</option>
            </select>
          </div>

          <div className="form-group">
            <label>Dietary Preference:</label>
            <select
              name="dietary_preference"
              value={preferencesForm.dietary_preference}
              onChange={handlePreferencesChange}
              required
            >
              <option value="vegetarian">Vegetarian</option>
              <option value="non_vegetarian">Non-Vegetarian</option>
              <option value="no_sugar">No Sugar</option>
            </select>
          </div>

          <div className="form-group">
            <label>Fitness Goal:</label>
            <select
              name="fitness_goal"
              value={preferencesForm.fitness_goal}
              onChange={handlePreferencesChange}
              required
            >
              <option value="weight_loss">Weight Loss</option>
              <option value="weight_gain">Weight Gain</option>
              <option value="stay_fit">Stay Fit</option>
            </select>
          </div>

          {error && <div className="error-message">{error}</div>}

          <div className="form-actions">
            <button type="button" onClick={() => setShowPreferencesForm(false)}>
              Cancel
            </button>
            <button type="submit" disabled={loading}>
              {loading ? 'Saving...' : 'Save Preferences'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  const renderMealPlan = () => {
    if (!currentMealPlan) return null;

    const { breakfast, lunch, dinner } = currentMealPlan;

    return (
      <div className="modal-overlay">
        <div className="modal meal-plan-modal">
          <h2>Your Personalized Meal Plan</h2>
          <p className="meal-plan-description">
            Generated using AI-powered genetic algorithm based on your preferences
          </p>

          {/* Removed calories summary */}

          <div className="meal-plan-grid">
            <div className="meal-card">
              <h3>🌅 Breakfast</h3>
              <div className="meal-details">
                <h4>{breakfast.name}</h4>
                {/* Removed nutrition info */}
              </div>
            </div>

            <div className="meal-card">
              <h3>☀️ Lunch</h3>
              <div className="meal-details">
                <h4>{lunch.name}</h4>
                {/* Removed nutrition info */}
              </div>
            </div>

            <div className="meal-card">
              <h3>🌙 Dinner</h3>
              <div className="meal-details">
                <h4>{dinner.name}</h4>
                {/* Removed nutrition info */}
              </div>
            </div>
          </div>

          <div className="meal-plan-actions">
            <button onClick={() => setShowMealPlan(false)}>Close</button>
            <button onClick={generateMealPlan} className="regenerate-btn">
              🔄 Generate New Plan
            </button>
          </div>
        </div>
      </div>
    );
  };

  const renderMealHistory = () => {
    if (mealHistory.length === 0) return null;

    return (
      <div className="meal-history-section">
        <h3>Recent Meal Plans</h3>
        <div className="history-grid">
          {mealHistory.slice(0, 3).map((plan, index) => (
            <div key={plan._id || index} className="history-card">
              <div className="history-date">
                {new Date(plan.date).toLocaleDateString()}
              </div>
              <div className="history-meals">
                <div className="history-meal">
                  <span className="meal-type">B:</span> {plan.breakfast?.name || 'N/A'}
                </div>
                <div className="history-meal">
                  <span className="meal-type">L:</span> {plan.lunch?.name || 'N/A'}
                </div>
                <div className="history-meal">
                  <span className="meal-type">D:</span> {plan.dinner?.name || 'N/A'}
                </div>
              </div>
              {/* Removed history calories */}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="meal-plans-container">
      <div className="header">
        <button className="back-btn" onClick={handleBack}>
          ← Back to Home
        </button>
        <h1>AI Meal Planning</h1>
      </div>

      <div className="main-content">
        {!userPreferences ? (
          <div className="welcome-section">
            <h2>Welcome to AI-Powered Meal Planning!</h2>
            <p>
              Get personalized meal recommendations based on your age, dietary preferences, and fitness goals.
              Our genetic algorithm creates optimal meal combinations for breakfast, lunch, and dinner.
            </p>
            <button 
              className="cta-button"
              onClick={() => setShowPreferencesForm(true)}
            >
              Get Started
            </button>
          </div>
        ) : (
          <div className="preferences-section">
            <div className="current-preferences">
              <h3>Your Current Preferences</h3>
              <div className="preferences-display">
                <span className="preference-tag">{userPreferences.age_group}</span>
                <span className="preference-tag">{userPreferences.dietary_preference}</span>
                <span className="preference-tag">{userPreferences.fitness_goal}</span>
              </div>
              <button 
                className="edit-preferences-btn"
                onClick={() => setShowPreferencesForm(true)}
              >
                Edit Preferences
              </button>
            </div>

            <div className="action-buttons">
              <button 
                className="generate-btn"
                onClick={generateMealPlan}
                disabled={loading}
              >
                {loading ? 'Generating...' : '🎯 Generate New Meal Plan'}
              </button>
            </div>

            {currentMealPlan && (
              <div className="current-plan-preview">
                <h3>Today's Plan</h3>
                <div className="plan-preview">
                  <div className="preview-meal">
                    <span className="meal-type">B:</span> {currentMealPlan.breakfast?.name}
                  </div>
                  <div className="preview-meal">
                    <span className="meal-type">L:</span> {currentMealPlan.lunch?.name}
                  </div>
                  <div className="preview-meal">
                    <span className="meal-type">D:</span> {currentMealPlan.dinner?.name}
                  </div>
                  {/* Removed preview calories */}
                </div>
                <button 
                  className="view-full-plan-btn"
                  onClick={() => setShowMealPlan(true)}
                >
                  View Full Plan
                </button>
              </div>
            )}
          </div>
        )}

        {renderMealHistory()}
      </div>

      {showPreferencesForm && renderPreferencesForm()}
      {showMealPlan && renderMealPlan()}
    </div>
  );
};

export default MealPlans;
