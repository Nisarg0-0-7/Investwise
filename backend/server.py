from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import uuid
from datetime import datetime
import asyncio

# Load environment variables
load_dotenv()

app = FastAPI(title="InvestWise AI", description="AI-Powered Financial Advisory Platform")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGO_URL = os.getenv('MONGO_URL')
client = MongoClient(MONGO_URL)
db = client.investwise_ai

# Collections
users_collection = db.users
assessments_collection = db.assessments
recommendations_collection = db.recommendations
chat_sessions_collection = db.chat_sessions

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Pydantic models
class UserProfile(BaseModel):
    name: str
    age: int
    occupation: str
    income: float
    current_savings: float
    investment_experience: str
    risk_tolerance: str
    financial_goals: List[str]
    investment_timeline: str
    behavioral_biases: List[str] = []

class RiskAssessment(BaseModel):
    user_id: str
    risk_score: int
    behavioral_profile: str
    recommendations: List[str]
    confidence_level: str

class ChatMessage(BaseModel):
    user_id: str
    message: str
    session_id: str

class InvestmentRecommendation(BaseModel):
    user_id: str
    portfolio_allocation: dict
    mutual_funds: List[dict]
    rationale: str
    risk_mitigation: str
    expected_returns: str

# AI System for Financial Analysis
class FinancialAdvisorAI:
    def __init__(self):
        self.system_message = """You are Dr. Sarah Chen, a leading behavioral finance expert and certified financial planner with 15 years of experience. Your expertise includes:

1. Identifying and overcoming behavioral biases in investing (loss aversion, recency bias, overconfidence, etc.)
2. Creating personalized investment strategies based on psychological profiles
3. Helping investors like Ajit overcome "snake-bite effect" and investment fears
4. Explaining complex financial concepts in simple terms
5. Providing evidence-based recommendations for mutual funds and equity investments

Your approach:
- Always assess psychological factors before making recommendations
- Address emotional barriers to investing
- Provide clear rationale for each recommendation
- Focus on long-term wealth building
- Help users understand risk vs. reward
- Suggest specific mutual fund categories and equity allocation strategies

Be empathetic, professional, and focus on building confidence in hesitant investors."""

    async def analyze_behavioral_profile(self, user_data: dict) -> dict:
        """Analyze user's behavioral profile and investment psychology"""
        
        # Behavioral bias detection based on user responses
        biases = []
        confidence_level = "medium"
        
        if user_data.get('investment_experience') == 'beginner':
            biases.append("overconfidence_bias")
            confidence_level = "low"
        
        if user_data.get('risk_tolerance') == 'low':
            biases.append("loss_aversion")
            
        if 'technology' in user_data.get('occupation', '').lower():
            biases.append("sector_bias")
            
        # Calculate risk score (1-10 scale)
        age = user_data.get('age', 30)
        income = user_data.get('income', 50000)
        experience = user_data.get('investment_experience', 'beginner')
        
        risk_score = 5  # baseline
        
        if age < 35:
            risk_score += 2
        elif age > 50:
            risk_score -= 1
            
        if experience == 'experienced':
            risk_score += 2
        elif experience == 'beginner':
            risk_score -= 1
            
        if income > 100000:
            risk_score += 1
            
        risk_score = max(1, min(10, risk_score))
        
        behavioral_profile = self._get_behavioral_profile(biases, risk_score)
        
        return {
            'risk_score': risk_score,
            'behavioral_biases': biases,
            'behavioral_profile': behavioral_profile,
            'confidence_level': confidence_level
        }
    
    def _get_behavioral_profile(self, biases: List[str], risk_score: int) -> str:
        """Determine behavioral profile based on biases and risk score"""
        if risk_score <= 3:
            return "Conservative Investor"
        elif risk_score <= 6:
            return "Moderate Investor"
        elif risk_score <= 8:
            return "Balanced Investor"
        else:
            return "Growth Investor"
    
    async def generate_investment_recommendations(self, user_data: dict, behavioral_analysis: dict) -> dict:
        """Generate personalized investment recommendations"""
        
        risk_score = behavioral_analysis['risk_score']
        behavioral_profile = behavioral_analysis['behavioral_profile']
        age = user_data.get('age', 30)
        goals = user_data.get('financial_goals', [])
        
        # Portfolio allocation based on risk profile
        if risk_score <= 3:  # Conservative
            allocation = {
                'large_cap_funds': 40,
                'debt_funds': 35,
                'hybrid_funds': 20,
                'international_funds': 5
            }
        elif risk_score <= 6:  # Moderate
            allocation = {
                'large_cap_funds': 30,
                'mid_cap_funds': 25,
                'debt_funds': 25,
                'hybrid_funds': 15,
                'international_funds': 5
            }
        else:  # Growth
            allocation = {
                'large_cap_funds': 25,
                'mid_cap_funds': 30,
                'small_cap_funds': 20,
                'debt_funds': 15,
                'international_funds': 10
            }
        
        # Mutual fund recommendations
        mutual_funds = self._get_mutual_fund_recommendations(allocation, behavioral_profile)
        
        # Generate rationale
        rationale = self._generate_rationale(user_data, behavioral_analysis, allocation)
        
        # Risk mitigation strategies
        risk_mitigation = self._generate_risk_mitigation(behavioral_analysis['behavioral_biases'])
        
        # Expected returns
        expected_returns = self._calculate_expected_returns(allocation, risk_score)
        
        return {
            'portfolio_allocation': allocation,
            'mutual_funds': mutual_funds,
            'rationale': rationale,
            'risk_mitigation': risk_mitigation,
            'expected_returns': expected_returns
        }
    
    def _get_mutual_fund_recommendations(self, allocation: dict, profile: str) -> List[dict]:
        """Get specific mutual fund recommendations based on allocation"""
        funds = []
        
        if allocation.get('large_cap_funds', 0) > 0:
            funds.append({
                'category': 'Large Cap Equity',
                'fund_name': 'Axis Bluechip Fund',
                'allocation_percentage': allocation['large_cap_funds'],
                'risk_level': 'Moderate',
                'rationale': 'Stable large-cap companies with consistent performance'
            })
        
        if allocation.get('mid_cap_funds', 0) > 0:
            funds.append({
                'category': 'Mid Cap Equity',
                'fund_name': 'Kotak Emerging Equity Fund',
                'allocation_percentage': allocation['mid_cap_funds'],
                'risk_level': 'High',
                'rationale': 'Growth potential in emerging mid-cap companies'
            })
        
        if allocation.get('small_cap_funds', 0) > 0:
            funds.append({
                'category': 'Small Cap Equity',
                'fund_name': 'SBI Small Cap Fund',
                'allocation_percentage': allocation['small_cap_funds'],
                'risk_level': 'Very High',
                'rationale': 'High growth potential with higher volatility'
            })
        
        if allocation.get('debt_funds', 0) > 0:
            funds.append({
                'category': 'Debt Fund',
                'fund_name': 'HDFC Corporate Bond Fund',
                'allocation_percentage': allocation['debt_funds'],
                'risk_level': 'Low',
                'rationale': 'Stable returns with capital preservation'
            })
        
        if allocation.get('hybrid_funds', 0) > 0:
            funds.append({
                'category': 'Hybrid Fund',
                'fund_name': 'ICICI Prudential Balanced Advantage Fund',
                'allocation_percentage': allocation['hybrid_funds'],
                'risk_level': 'Moderate',
                'rationale': 'Balanced approach with dynamic asset allocation'
            })
        
        if allocation.get('international_funds', 0) > 0:
            funds.append({
                'category': 'International Fund',
                'fund_name': 'Motilal Oswal Nasdaq 100 Fund',
                'allocation_percentage': allocation['international_funds'],
                'risk_level': 'High',
                'rationale': 'Global diversification with technology exposure'
            })
        
        return funds
    
    def _generate_rationale(self, user_data: dict, behavioral_analysis: dict, allocation: dict) -> str:
        """Generate detailed rationale for recommendations"""
        age = user_data.get('age', 30)
        profile = behavioral_analysis['behavioral_profile']
        biases = behavioral_analysis['behavioral_biases']
        
        rationale = f"""
        Based on your profile as a {age}-year-old {profile}, here's why this allocation works for you:

        1. **Age-Appropriate Strategy**: At {age}, you have a {"long" if age < 40 else "moderate"} investment horizon, allowing for {"higher" if age < 40 else "balanced"} equity exposure.

        2. **Behavioral Considerations**: 
        """
        
        if 'loss_aversion' in biases:
            rationale += "- Your risk-averse nature is balanced with debt funds for stability while still capturing equity growth.\n"
        
        if 'sector_bias' in biases:
            rationale += "- Diversified allocation prevents over-concentration in any single sector.\n"
        
        if 'overconfidence_bias' in biases:
            rationale += "- Conservative approach initially to build confidence before increasing risk exposure.\n"
        
        rationale += f"""
        3. **Risk Management**: {allocation.get('debt_funds', 0)}% in debt funds provides stability and reduces portfolio volatility.

        4. **Growth Potential**: {allocation.get('large_cap_funds', 0) + allocation.get('mid_cap_funds', 0)}% in equity funds for long-term wealth creation.

        5. **Diversification**: International exposure provides geographic diversification and reduces country-specific risks.
        """
        
        return rationale
    
    def _generate_risk_mitigation(self, biases: List[str]) -> str:
        """Generate risk mitigation strategies based on behavioral biases"""
        strategies = []
        
        if 'loss_aversion' in biases:
            strategies.append("• Start with SIP (Systematic Investment Plan) to average out market volatility")
            strategies.append("• Focus on long-term goals rather than short-term market movements")
        
        if 'overconfidence_bias' in biases:
            strategies.append("• Regular portfolio review and rebalancing")
            strategies.append("• Avoid frequent trading and stick to the plan")
        
        if 'sector_bias' in biases:
            strategies.append("• Diversify across sectors and asset classes")
            strategies.append("• Avoid concentration in familiar sectors")
        
        strategies.append("• Regular monitoring and annual review")
        strategies.append("• Emergency fund equivalent to 6-8 months of expenses")
        
        return "\n".join(strategies)
    
    def _calculate_expected_returns(self, allocation: dict, risk_score: int) -> str:
        """Calculate expected returns based on allocation"""
        equity_percentage = allocation.get('large_cap_funds', 0) + allocation.get('mid_cap_funds', 0) + allocation.get('small_cap_funds', 0)
        debt_percentage = allocation.get('debt_funds', 0)
        
        # Expected returns (simplified calculation)
        equity_return = 12  # 12% for equity
        debt_return = 7     # 7% for debt
        
        weighted_return = (equity_percentage * equity_return + debt_percentage * debt_return + 
                          allocation.get('hybrid_funds', 0) * 10 + allocation.get('international_funds', 0) * 11) / 100
        
        return f"Expected annual returns: {weighted_return:.1f}% - {weighted_return + 2:.1f}% (based on historical data and current market conditions)"

# Initialize AI advisor
ai_advisor = FinancialAdvisorAI()

# API Routes
@app.get("/")
async def root():
    return {"message": "InvestWise AI - Your Personal Financial Advisory Platform"}

@app.post("/api/user-profile")
async def create_user_profile(profile: UserProfile):
    """Create or update user profile"""
    try:
        user_id = str(uuid.uuid4())
        user_data = {
            "user_id": user_id,
            "name": profile.name,
            "age": profile.age,
            "occupation": profile.occupation,
            "income": profile.income,
            "current_savings": profile.current_savings,
            "investment_experience": profile.investment_experience,
            "risk_tolerance": profile.risk_tolerance,
            "financial_goals": profile.financial_goals,
            "investment_timeline": profile.investment_timeline,
            "created_at": datetime.now()
        }
        
        users_collection.insert_one(user_data)
        return {"user_id": user_id, "message": "Profile created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/risk-assessment")
async def perform_risk_assessment(user_id: str):
    """Perform behavioral risk assessment"""
    try:
        # Get user data
        user_data = users_collection.find_one({"user_id": user_id})
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Perform behavioral analysis
        behavioral_analysis = await ai_advisor.analyze_behavioral_profile(user_data)
        
        # Store assessment
        assessment_data = {
            "user_id": user_id,
            "risk_score": behavioral_analysis['risk_score'],
            "behavioral_profile": behavioral_analysis['behavioral_profile'],
            "behavioral_biases": behavioral_analysis['behavioral_biases'],
            "confidence_level": behavioral_analysis['confidence_level'],
            "created_at": datetime.now()
        }
        
        assessments_collection.insert_one(assessment_data)
        
        return behavioral_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/investment-recommendations")
async def get_investment_recommendations(user_id: str):
    """Get personalized investment recommendations"""
    try:
        # Get user data and assessment
        user_data = users_collection.find_one({"user_id": user_id})
        assessment_data = assessments_collection.find_one({"user_id": user_id})
        
        if not user_data or not assessment_data:
            raise HTTPException(status_code=404, detail="User profile or assessment not found")
        
        # Generate recommendations
        recommendations = await ai_advisor.generate_investment_recommendations(user_data, assessment_data)
        
        # Store recommendations
        recommendation_data = {
            "user_id": user_id,
            "portfolio_allocation": recommendations['portfolio_allocation'],
            "mutual_funds": recommendations['mutual_funds'],
            "rationale": recommendations['rationale'],
            "risk_mitigation": recommendations['risk_mitigation'],
            "expected_returns": recommendations['expected_returns'],
            "created_at": datetime.now()
        }
        
        recommendations_collection.insert_one(recommendation_data)
        
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/{user_id}/dashboard")
async def get_user_dashboard(user_id: str):
    """Get user dashboard data"""
    try:
        user_data = users_collection.find_one({"user_id": user_id})
        assessment_data = assessments_collection.find_one({"user_id": user_id})
        recommendations_data = recommendations_collection.find_one({"user_id": user_id})
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Remove MongoDB _id from results
        for data in [user_data, assessment_data, recommendations_data]:
            if data and '_id' in data:
                del data['_id']
        
        return {
            "user_profile": user_data,
            "risk_assessment": assessment_data,
            "recommendations": recommendations_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)