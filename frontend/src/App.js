import React, { useState, useEffect } from 'react';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [currentStep, setCurrentStep] = useState('welcome');
  const [userProfile, setUserProfile] = useState({
    name: '',
    age: '',
    occupation: '',
    income: '',
    current_savings: '',
    investment_experience: 'beginner',
    risk_tolerance: 'low',
    financial_goals: [],
    investment_timeline: '1-3 years'
  });
  const [userId, setUserId] = useState('');
  const [riskAssessment, setRiskAssessment] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const goalOptions = [
    'Retirement Planning',
    'Child Education',
    'Emergency Fund',
    'Wealth Creation',
    'Tax Saving',
    'Home Purchase',
    'Travel Fund',
    'Business Investment'
  ];

  const handleInputChange = (field, value) => {
    setUserProfile(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleGoalToggle = (goal) => {
    setUserProfile(prev => ({
      ...prev,
      financial_goals: prev.financial_goals.includes(goal)
        ? prev.financial_goals.filter(g => g !== goal)
        : [...prev.financial_goals, goal]
    }));
  };

  const createUserProfile = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/user-profile`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...userProfile,
          age: parseInt(userProfile.age),
          income: parseFloat(userProfile.income),
          current_savings: parseFloat(userProfile.current_savings)
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create profile');
      }

      const data = await response.json();
      setUserId(data.user_id);
      setCurrentStep('assessment');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const performRiskAssessment = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/risk-assessment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userId),
      });

      if (!response.ok) {
        throw new Error('Failed to perform assessment');
      }

      const data = await response.json();
      setRiskAssessment(data);
      setCurrentStep('recommendations');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getRecommendations = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${BACKEND_URL}/api/investment-recommendations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userId),
      });

      if (!response.ok) {
        throw new Error('Failed to get recommendations');
      }

      const data = await response.json();
      setRecommendations(data);
      setCurrentStep('dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const WelcomeScreen = () => (
    <div className="welcome-screen">
      <div className="hero-section">
        <img 
          src="https://images.unsplash.com/photo-1649768996403-455e21e6e4ec" 
          alt="Financial Advisor" 
          className="hero-image"
        />
        <div className="hero-content">
          <h1 className="hero-title">InvestWise AI</h1>
          <p className="hero-subtitle">Your Personal Investment Psychology Coach</p>
          <p className="hero-description">
            Overcome investment fears, understand your behavioral biases, and build a portfolio that truly fits your personality and goals.
          </p>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🧠</div>
              <h3>Behavioral Analysis</h3>
              <p>Identify and overcome investment biases like the "snake-bite effect"</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Personalized Recommendations</h3>
              <p>AI-powered investment suggestions based on your psychology</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Goal-Based Planning</h3>
              <p>Align your investments with your life goals and timeline</p>
            </div>
          </div>
          <button 
            className="cta-button" 
            onClick={() => setCurrentStep('profile')}
          >
            Start Your Investment Journey
          </button>
        </div>
      </div>
    </div>
  );

  const ProfileScreen = () => (
    <div className="profile-screen">
      <div className="form-container">
        <h2>Tell Us About Yourself</h2>
        <p className="form-description">
          Help us understand your financial situation to provide personalized recommendations.
        </p>
        
        <div className="form-grid">
          <div className="form-group">
            <label>Full Name</label>
            <input
              type="text"
              value={userProfile.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              placeholder="Enter your full name"
            />
          </div>
          
          <div className="form-group">
            <label>Age</label>
            <input
              type="number"
              value={userProfile.age}
              onChange={(e) => handleInputChange('age', e.target.value)}
              placeholder="Enter your age"
            />
          </div>
          
          <div className="form-group">
            <label>Occupation</label>
            <input
              type="text"
              value={userProfile.occupation}
              onChange={(e) => handleInputChange('occupation', e.target.value)}
              placeholder="e.g., Software Engineer, Doctor, Teacher"
            />
          </div>
          
          <div className="form-group">
            <label>Annual Income (₹)</label>
            <input
              type="number"
              value={userProfile.income}
              onChange={(e) => handleInputChange('income', e.target.value)}
              placeholder="Enter your annual income"
            />
          </div>
          
          <div className="form-group">
            <label>Current Savings (₹)</label>
            <input
              type="number"
              value={userProfile.current_savings}
              onChange={(e) => handleInputChange('current_savings', e.target.value)}
              placeholder="Enter your current savings"
            />
          </div>
          
          <div className="form-group">
            <label>Investment Experience</label>
            <select
              value={userProfile.investment_experience}
              onChange={(e) => handleInputChange('investment_experience', e.target.value)}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="experienced">Experienced</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Risk Tolerance</label>
            <select
              value={userProfile.risk_tolerance}
              onChange={(e) => handleInputChange('risk_tolerance', e.target.value)}
            >
              <option value="low">Low - I prefer stable returns</option>
              <option value="moderate">Moderate - I can handle some volatility</option>
              <option value="high">High - I'm comfortable with market fluctuations</option>
            </select>
          </div>
          
          <div className="form-group">
            <label>Investment Timeline</label>
            <select
              value={userProfile.investment_timeline}
              onChange={(e) => handleInputChange('investment_timeline', e.target.value)}
            >
              <option value="1-3 years">1-3 years</option>
              <option value="3-5 years">3-5 years</option>
              <option value="5-10 years">5-10 years</option>
              <option value="10+ years">10+ years</option>
            </select>
          </div>
        </div>
        
        <div className="form-group">
          <label>Financial Goals (Select all that apply)</label>
          <div className="goals-grid">
            {goalOptions.map(goal => (
              <div
                key={goal}
                className={`goal-option ${userProfile.financial_goals.includes(goal) ? 'selected' : ''}`}
                onClick={() => handleGoalToggle(goal)}
              >
                {goal}
              </div>
            ))}
          </div>
        </div>
        
        <button 
          className="submit-button"
          onClick={createUserProfile}
          disabled={loading || !userProfile.name || !userProfile.age}
        >
          {loading ? 'Creating Profile...' : 'Continue to Assessment'}
        </button>
      </div>
    </div>
  );

  const AssessmentScreen = () => (
    <div className="assessment-screen">
      <div className="assessment-container">
        <h2>Behavioral Risk Assessment</h2>
        <p className="assessment-description">
          Let's analyze your investment psychology to identify potential behavioral biases and create a personalized strategy.
        </p>
        
        <div className="assessment-info">
          <img 
            src="https://images.unsplash.com/photo-1660020619062-70b16c44bf0f" 
            alt="Investment Analysis" 
            className="assessment-image"
          />
          <div className="assessment-content">
            <h3>What We'll Analyze:</h3>
            <ul>
              <li>📊 Your risk tolerance vs. risk capacity</li>
              <li>🎯 Behavioral patterns and potential biases</li>
              <li>💡 Investment psychology profile</li>
              <li>🔍 Confidence level assessment</li>
              <li>📈 Personalized risk score</li>
            </ul>
          </div>
        </div>
        
        <button 
          className="assessment-button"
          onClick={performRiskAssessment}
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Start Assessment'}
        </button>
      </div>
    </div>
  );

  const RecommendationsScreen = () => (
    <div className="recommendations-screen">
      <div className="recommendations-container">
        <h2>Your Investment Recommendations</h2>
        <p className="recommendations-description">
          Based on your behavioral analysis, here are your personalized investment recommendations.
        </p>
        
        {riskAssessment && (
          <div className="assessment-results">
            <div className="result-card">
              <h3>Your Profile</h3>
              <div className="profile-details">
                <div className="detail-item">
                  <span className="label">Risk Score:</span>
                  <span className="value">{riskAssessment.risk_score}/10</span>
                </div>
                <div className="detail-item">
                  <span className="label">Investor Type:</span>
                  <span className="value">{riskAssessment.behavioral_profile}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Confidence Level:</span>
                  <span className="value">{riskAssessment.confidence_level}</span>
                </div>
                {riskAssessment.behavioral_biases && riskAssessment.behavioral_biases.length > 0 && (
                  <div className="detail-item">
                    <span className="label">Behavioral Considerations:</span>
                    <span className="value">{riskAssessment.behavioral_biases.join(', ')}</span>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
        
        <button 
          className="recommendations-button"
          onClick={getRecommendations}
          disabled={loading}
        >
          {loading ? 'Generating Recommendations...' : 'Get My Investment Plan'}
        </button>
      </div>
    </div>
  );

  const DashboardScreen = () => (
    <div className="dashboard-screen">
      <div className="dashboard-container">
        <h2>Your Personalized Investment Dashboard</h2>
        
        {recommendations && (
          <div className="dashboard-content">
            <div className="portfolio-allocation">
              <h3>Recommended Portfolio Allocation</h3>
              <div className="allocation-chart">
                {Object.entries(recommendations.portfolio_allocation).map(([category, percentage]) => (
                  <div key={category} className="allocation-item">
                    <div className="allocation-bar">
                      <div 
                        className="allocation-fill" 
                        style={{width: `${percentage}%`}}
                      ></div>
                    </div>
                    <div className="allocation-label">
                      <span className="category">{category.replace('_', ' ')}</span>
                      <span className="percentage">{percentage}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="mutual-funds">
              <h3>Recommended Mutual Funds</h3>
              <div className="funds-grid">
                {recommendations.mutual_funds.map((fund, index) => (
                  <div key={index} className="fund-card">
                    <div className="fund-header">
                      <h4>{fund.fund_name}</h4>
                      <span className="fund-category">{fund.category}</span>
                    </div>
                    <div className="fund-details">
                      <div className="fund-allocation">{fund.allocation_percentage}% Allocation</div>
                      <div className="fund-risk">Risk: {fund.risk_level}</div>
                      <div className="fund-rationale">{fund.rationale}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="recommendations-details">
              <div className="detail-section">
                <h3>Why This Strategy Works for You</h3>
                <div className="rationale-text">
                  {recommendations.rationale.split('\n').map((line, index) => (
                    <p key={index}>{line}</p>
                  ))}
                </div>
              </div>
              
              <div className="detail-section">
                <h3>Risk Management Strategy</h3>
                <div className="risk-mitigation">
                  {recommendations.risk_mitigation.split('\n').map((line, index) => (
                    <p key={index}>{line}</p>
                  ))}
                </div>
              </div>
              
              <div className="detail-section">
                <h3>Expected Returns</h3>
                <div className="expected-returns">
                  {recommendations.expected_returns}
                </div>
              </div>
            </div>
            
            <div className="action-buttons">
              <button className="premium-button">
                Upgrade to Premium for AI Chat Advisory
              </button>
              <button className="secondary-button" onClick={() => setCurrentStep('welcome')}>
                Start New Assessment
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  return (
    <div className="App">
      <nav className="navbar">
        <div className="nav-brand">
          <h1>InvestWise AI</h1>
        </div>
        <div className="nav-links">
          <span className="nav-step">
            {currentStep === 'welcome' && 'Welcome'}
            {currentStep === 'profile' && 'Profile Setup'}
            {currentStep === 'assessment' && 'Risk Assessment'}
            {currentStep === 'recommendations' && 'Recommendations'}
            {currentStep === 'dashboard' && 'Your Dashboard'}
          </span>
        </div>
      </nav>
      
      <main className="main-content">
        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}
        
        {currentStep === 'welcome' && <WelcomeScreen />}
        {currentStep === 'profile' && <ProfileScreen />}
        {currentStep === 'assessment' && <AssessmentScreen />}
        {currentStep === 'recommendations' && <RecommendationsScreen />}
        {currentStep === 'dashboard' && <DashboardScreen />}
      </main>
      
      <footer className="footer">
        <p>&copy; 2025 InvestWise AI. Empowering smarter investment decisions through behavioral finance.</p>
      </footer>
    </div>
  );
}

export default App;