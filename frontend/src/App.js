import React, { useState, useEffect, useRef } from 'react';
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
  const [scrollY, setScrollY] = useState(0);
  const [isVisible, setIsVisible] = useState({});

  const goalOptions = [
    { id: 'retirement', label: 'Retirement Planning', icon: '🏖️' },
    { id: 'education', label: 'Child Education', icon: '🎓' },
    { id: 'emergency', label: 'Emergency Fund', icon: '🛡️' },
    { id: 'wealth', label: 'Wealth Creation', icon: '💰' },
    { id: 'tax', label: 'Tax Saving', icon: '📊' },
    { id: 'home', label: 'Home Purchase', icon: '🏠' },
    { id: 'travel', label: 'Travel Fund', icon: '✈️' },
    { id: 'business', label: 'Business Investment', icon: '🚀' }
  ];

  // Smooth scroll tracking
  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Intersection Observer for animations
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          setIsVisible(prev => ({
            ...prev,
            [entry.target.id]: entry.isIntersecting
          }));
        });
      },
      { threshold: 0.1 }
    );

    const elements = document.querySelectorAll('.animate-on-scroll');
    elements.forEach(el => observer.observe(el));

    return () => observer.disconnect();
  }, [currentStep]);

  const handleInputChange = (field, value) => {
    setUserProfile(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleGoalToggle = (goalId) => {
    setUserProfile(prev => ({
      ...prev,
      financial_goals: prev.financial_goals.includes(goalId)
        ? prev.financial_goals.filter(g => g !== goalId)
        : [...prev.financial_goals, goalId]
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
          age: parseInt(userProfile.age) || 0,
          income: parseFloat(userProfile.income) || 0,
          current_savings: parseFloat(userProfile.current_savings) || 0
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
      const response = await fetch(`${BACKEND_URL}/api/risk-assessment?user_id=${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
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
      const response = await fetch(`${BACKEND_URL}/api/investment-recommendations?user_id=${userId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
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
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text" style={{ transform: `translateY(${scrollY * 0.1}px)` }}>
            <h1 className="hero-title">
              Smart investing starts with
              <span className="highlight"> understanding yourself</span>
            </h1>
            <p className="hero-subtitle">
              Transform your investment fears into confidence with AI-powered behavioral finance insights
            </p>
            <div className="hero-stats">
              <div className="stat">
                <div className="stat-number">98%</div>
                <div className="stat-label">Bias Detection</div>
              </div>
              <div className="stat">
                <div className="stat-number">12.5%</div>
                <div className="stat-label">Avg. Returns</div>
              </div>
              <div className="stat">
                <div className="stat-number">10k+</div>
                <div className="stat-label">Happy Investors</div>
              </div>
            </div>
            <button 
              className="cta-button"
              onClick={() => setCurrentStep('profile')}
            >
              Start Your Journey
              <span className="arrow">→</span>
            </button>
          </div>
          <div className="hero-visual">
            <div className="floating-card card-1">
              <div className="card-content">
                <div className="card-icon">📊</div>
                <div className="card-text">Risk Score: 7/10</div>
              </div>
            </div>
            <div className="floating-card card-2">
              <div className="card-content">
                <div className="card-icon">💰</div>
                <div className="card-text">Portfolio: ₹5.2L</div>
              </div>
            </div>
            <div className="floating-card card-3">
              <div className="card-content">
                <div className="card-icon">🎯</div>
                <div className="card-text">Goal: 85% Complete</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <h2 className="section-title animate-on-scroll" id="features-title">
            Why InvestWise AI?
          </h2>
          <div className="features-grid">
            <div className={`feature-card ${isVisible['features-title'] ? 'visible' : ''}`}>
              <div className="feature-icon">🧠</div>
              <h3>Behavioral Analysis</h3>
              <p>Identify and overcome psychological barriers like the "snake-bite effect" that hold you back from investing</p>
            </div>
            <div className={`feature-card ${isVisible['features-title'] ? 'visible' : ''}`}>
              <div className="feature-icon">🎯</div>
              <h3>Personalized Strategy</h3>
              <p>Get investment recommendations tailored to your personality, not just your finances</p>
            </div>
            <div className={`feature-card ${isVisible['features-title'] ? 'visible' : ''}`}>
              <div className="feature-icon">📈</div>
              <h3>Smart Allocation</h3>
              <p>AI-powered portfolio allocation that adapts to your risk tolerance and life goals</p>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Solution Section */}
      <section className="problem-solution-section">
        <div className="container">
          <div className="problem-solution-content">
            <div className="problem-side">
              <h3>The Problem</h3>
              <div className="problem-list">
                <div className="problem-item">
                  <span className="problem-icon">❌</span>
                  <span>Fear of investing after market losses</span>
                </div>
                <div className="problem-item">
                  <span className="problem-icon">❌</span>
                  <span>Emotional decision making</span>
                </div>
                <div className="problem-item">
                  <span className="problem-icon">❌</span>
                  <span>Lack of personalized guidance</span>
                </div>
              </div>
            </div>
            <div className="solution-side">
              <h3>Our Solution</h3>
              <div className="solution-list">
                <div className="solution-item">
                  <span className="solution-icon">✅</span>
                  <span>Behavioral bias detection & correction</span>
                </div>
                <div className="solution-item">
                  <span className="solution-icon">✅</span>
                  <span>Psychology-based recommendations</span>
                </div>
                <div className="solution-item">
                  <span className="solution-icon">✅</span>
                  <span>Confidence-building journey</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );

  const ProfileScreen = () => (
    <div className="profile-screen">
      <div className="profile-container">
        <div className="profile-header">
          <h2>Tell us about yourself</h2>
          <p>We'll use this information to create your personalized investment psychology profile</p>
        </div>
        
        <div className="profile-form">
          <div className="form-section">
            <h3>Personal Information</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Full Name</label>
                <input
                  type="text"
                  value={userProfile.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  placeholder="Enter your full name"
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <label>Age</label>
                <input
                  type="number"
                  value={userProfile.age}
                  onChange={(e) => handleInputChange('age', e.target.value)}
                  placeholder="Enter your age"
                  className="form-input"
                />
              </div>
            </div>
            <div className="form-group">
              <label>Occupation</label>
              <input
                type="text"
                value={userProfile.occupation}
                onChange={(e) => handleInputChange('occupation', e.target.value)}
                placeholder="e.g., Software Engineer, Doctor, Teacher"
                className="form-input"
              />
            </div>
          </div>

          <div className="form-section">
            <h3>Financial Information</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Annual Income (₹)</label>
                <input
                  type="number"
                  value={userProfile.income}
                  onChange={(e) => handleInputChange('income', e.target.value)}
                  placeholder="Enter your annual income"
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <label>Current Savings (₹)</label>
                <input
                  type="number"
                  value={userProfile.current_savings}
                  onChange={(e) => handleInputChange('current_savings', e.target.value)}
                  placeholder="Enter your current savings"
                  className="form-input"
                />
              </div>
            </div>
          </div>

          <div className="form-section">
            <h3>Investment Profile</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Investment Experience</label>
                <select
                  value={userProfile.investment_experience}
                  onChange={(e) => handleInputChange('investment_experience', e.target.value)}
                  className="form-select"
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
                  className="form-select"
                >
                  <option value="low">Conservative</option>
                  <option value="moderate">Moderate</option>
                  <option value="high">Aggressive</option>
                </select>
              </div>
            </div>
            <div className="form-group">
              <label>Investment Timeline</label>
              <select
                value={userProfile.investment_timeline}
                onChange={(e) => handleInputChange('investment_timeline', e.target.value)}
                className="form-select"
              >
                <option value="1-3 years">1-3 years</option>
                <option value="3-5 years">3-5 years</option>
                <option value="5-10 years">5-10 years</option>
                <option value="10+ years">10+ years</option>
              </select>
            </div>
          </div>

          <div className="form-section">
            <h3>Financial Goals</h3>
            <div className="goals-grid">
              {goalOptions.map(goal => (
                <div
                  key={goal.id}
                  className={`goal-card ${userProfile.financial_goals.includes(goal.id) ? 'selected' : ''}`}
                  onClick={() => handleGoalToggle(goal.id)}
                >
                  <div className="goal-icon">{goal.icon}</div>
                  <div className="goal-label">{goal.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        <div className="form-actions">
          <button 
            className="submit-button"
            onClick={createUserProfile}
            disabled={loading || !userProfile.name || !userProfile.age}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Creating Profile...
              </>
            ) : (
              <>
                Continue to Assessment
                <span className="arrow">→</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );

  const AssessmentScreen = () => (
    <div className="assessment-screen">
      <div className="assessment-container">
        <div className="assessment-header">
          <h2>Behavioral Assessment</h2>
          <p>Let's analyze your investment psychology to create a personalized strategy</p>
        </div>
        
        <div className="assessment-content">
          <div className="assessment-visual">
            <div className="brain-icon">🧠</div>
            <div className="analysis-items">
              <div className="analysis-item">
                <div className="item-icon">🎯</div>
                <div className="item-text">Risk tolerance evaluation</div>
              </div>
              <div className="analysis-item">
                <div className="item-icon">📊</div>
                <div className="item-text">Behavioral bias detection</div>
              </div>
              <div className="analysis-item">
                <div className="item-icon">💡</div>
                <div className="item-text">Investment personality profiling</div>
              </div>
            </div>
          </div>
          
          <div className="assessment-info">
            <h3>What we'll discover:</h3>
            <ul>
              <li>Your true risk capacity vs. risk tolerance</li>
              <li>Potential behavioral biases affecting your decisions</li>
              <li>Optimal investment approach for your personality</li>
              <li>Strategies to overcome investment fears</li>
            </ul>
          </div>
        </div>
        
        <button 
          className="assessment-button"
          onClick={performRiskAssessment}
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Analyzing Your Profile...
            </>
          ) : (
            <>
              Start Assessment
              <span className="arrow">→</span>
            </>
          )}
        </button>
      </div>
    </div>
  );

  const RecommendationsScreen = () => (
    <div className="recommendations-screen">
      <div className="recommendations-container">
        <div className="recommendations-header">
          <h2>Your Investment Profile</h2>
          <p>Based on your behavioral analysis, here's what we discovered</p>
        </div>
        
        {riskAssessment && (
          <div className="profile-results">
            <div className="result-card risk-score">
              <div className="card-header">
                <h3>Risk Score</h3>
                <div className="score-value">{riskAssessment.risk_score}/10</div>
              </div>
              <div className="score-bar">
                <div 
                  className="score-fill" 
                  style={{ width: `${(riskAssessment.risk_score / 10) * 100}%` }}
                ></div>
              </div>
            </div>
            
            <div className="result-card investor-type">
              <div className="card-header">
                <h3>Investor Type</h3>
                <div className="type-badge">{riskAssessment.behavioral_profile}</div>
              </div>
            </div>
            
            {riskAssessment.behavioral_biases && riskAssessment.behavioral_biases.length > 0 && (
              <div className="result-card biases">
                <div className="card-header">
                  <h3>Behavioral Considerations</h3>
                </div>
                <div className="biases-list">
                  {riskAssessment.behavioral_biases.map((bias, index) => (
                    <div key={index} className="bias-item">
                      <span className="bias-icon">⚠️</span>
                      <span className="bias-text">{bias.replace('_', ' ')}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
        
        <button 
          className="recommendations-button"
          onClick={getRecommendations}
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Creating Your Investment Plan...
            </>
          ) : (
            <>
              Get My Recommendations
              <span className="arrow">→</span>
            </>
          )}
        </button>
      </div>
    </div>
  );

  const DashboardScreen = () => (
    <div className="dashboard-screen">
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h2>Your Personal Investment Plan</h2>
          <p>Tailored recommendations based on your behavioral profile</p>
        </div>
        
        {recommendations && (
          <div className="dashboard-content">
            <div className="portfolio-section">
              <h3>Recommended Portfolio Allocation</h3>
              <div className="allocation-grid">
                {Object.entries(recommendations.portfolio_allocation).map(([category, percentage]) => (
                  <div key={category} className="allocation-card">
                    <div className="allocation-header">
                      <span className="category-name">{category.replace('_', ' ')}</span>
                      <span className="percentage">{percentage}%</span>
                    </div>
                    <div className="allocation-bar">
                      <div 
                        className="allocation-fill" 
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="funds-section">
              <h3>Recommended Mutual Funds</h3>
              <div className="funds-grid">
                {recommendations.mutual_funds.map((fund, index) => (
                  <div key={index} className="fund-card">
                    <div className="fund-header">
                      <h4>{fund.fund_name}</h4>
                      <span className="fund-category">{fund.category}</span>
                    </div>
                    <div className="fund-body">
                      <div className="fund-allocation">{fund.allocation_percentage}%</div>
                      <div className="fund-risk">Risk: {fund.risk_level}</div>
                      <div className="fund-rationale">{fund.rationale}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="insights-section">
              <div className="insight-card">
                <h3>Why This Strategy Works for You</h3>
                <div className="insight-content">
                  {recommendations.rationale.split('\n').map((line, index) => (
                    line.trim() && <p key={index}>{line.trim()}</p>
                  ))}
                </div>
              </div>
              
              <div className="insight-card">
                <h3>Risk Management</h3>
                <div className="insight-content">
                  {recommendations.risk_mitigation.split('\n').map((line, index) => (
                    line.trim() && <p key={index}>{line.trim()}</p>
                  ))}
                </div>
              </div>
              
              <div className="insight-card returns">
                <h3>Expected Returns</h3>
                <div className="returns-content">
                  {recommendations.expected_returns}
                </div>
              </div>
            </div>
            
            <div className="action-section">
              <button className="premium-button">
                Upgrade to Premium AI Advisory
                <span className="premium-badge">₹999/month</span>
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
        <div className="nav-content">
          <div className="nav-brand">
            <h1>InvestWise</h1>
          </div>
          <div className="nav-progress">
            <div className="progress-steps">
              <div className={`step ${currentStep === 'welcome' ? 'active' : ''}`}>Welcome</div>
              <div className={`step ${currentStep === 'profile' ? 'active' : ''}`}>Profile</div>
              <div className={`step ${currentStep === 'assessment' ? 'active' : ''}`}>Assessment</div>
              <div className={`step ${currentStep === 'recommendations' ? 'active' : ''}`}>Results</div>
              <div className={`step ${currentStep === 'dashboard' ? 'active' : ''}`}>Dashboard</div>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="main-content">
        {error && (
          <div className="error-banner">
            <div className="error-content">
              <span className="error-icon">⚠️</span>
              <span className="error-text">{error}</span>
              <button className="error-close" onClick={() => setError('')}>×</button>
            </div>
          </div>
        )}
        
        {currentStep === 'welcome' && <WelcomeScreen />}
        {currentStep === 'profile' && <ProfileScreen />}
        {currentStep === 'assessment' && <AssessmentScreen />}
        {currentStep === 'recommendations' && <RecommendationsScreen />}
        {currentStep === 'dashboard' && <DashboardScreen />}
      </main>
    </div>
  );
}

export default App;