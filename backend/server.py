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
import random

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

# Enhanced Indian Market Fund Database
INDIAN_MUTUAL_FUNDS = {
    'large_cap': [
        {
            'name': 'HDFC Top 100 Fund',
            'category': 'Large Cap',
            'rating': 4.5,
            'returns_3y': 15.8,
            'returns_5y': 13.2,
            'returns_10y': 11.8,
            'aum': 25420,
            'stocks_count': 68,
            'expense_ratio': 1.45,
            'exit_load': 1.0,
            'min_investment': 500,
            'fund_manager': 'Prashant Jain'
        },
        {
            'name': 'Axis Bluechip Fund',
            'category': 'Large Cap',
            'rating': 4.3,
            'returns_3y': 14.5,
            'returns_5y': 12.8,
            'returns_10y': 11.2,
            'aum': 18750,
            'stocks_count': 45,
            'expense_ratio': 1.35,
            'exit_load': 1.0,
            'min_investment': 500,
            'fund_manager': 'Shreyash Devalkar'
        },
        {
            'name': 'Mirae Asset Large Cap Fund',
            'category': 'Large Cap',
            'rating': 4.2,
            'returns_3y': 16.2,
            'returns_5y': 14.1,
            'returns_10y': 12.5,
            'aum': 12890,
            'stocks_count': 52,
            'expense_ratio': 1.8,
            'exit_load': 1.0,
            'min_investment': 500,
            'fund_manager': 'Neelesh Surana'
        }
    ],
    'mid_cap': [
        {
            'name': 'Kotak Emerging Equity Fund',
            'category': 'Mid Cap',
            'rating': 4.6,
            'returns_3y': 22.5,
            'returns_5y': 18.9,
            'returns_10y': 16.2,
            'aum': 8450,
            'stocks_count': 42,
            'expense_ratio': 1.95,
            'exit_load': 1.0,
            'min_investment': 500,
            'fund_manager': 'Pankaj Tibrewal'
        },
        {
            'name': 'DSP Midcap Fund',
            'category': 'Mid Cap',
            'rating': 4.4,
            'returns_3y': 19.8,
            'returns_5y': 17.2,
            'returns_10y': 15.5,
            'aum': 6780,
            'stocks_count': 38,
            'expense_ratio': 2.1,
            'exit_load': 1.0,
            'min_investment': 500,
            'fund_manager': 'Vinit Sambre'
        }
    ],
    'small_cap': [
        {
            'name': 'SBI Small Cap Fund',
            'category': 'Small Cap',
            'rating': 4.1,
            'returns_3y': 28.5,
            'returns_5y': 22.8,
            'returns_10y': 18.9,
            'aum': 4250,
            'stocks_count': 65,
            'expense_ratio': 2.25,
            'exit_load': 1.0,
            'min_investment': 500,
            'fund_manager': 'R. Srinivasan'
        },
        {
            'name': 'Nippon India Small Cap Fund',
            'category': 'Small Cap',
            'rating': 4.0,
            'returns_3y': 26.2,
            'returns_5y': 21.5,
            'returns_10y': 17.8,
            'aum': 3890,
            'stocks_count': 58,
            'expense_ratio': 2.3,
            'exit_load': 1.0,
            'min_investment': 500,
            'fund_manager': 'Samir Rachh'
        }
    ],
    'debt': [
        {
            'name': 'HDFC Corporate Bond Fund',
            'category': 'Corporate Bond',
            'rating': 4.2,
            'returns_3y': 8.5,
            'returns_5y': 7.8,
            'returns_10y': 8.2,
            'aum': 15680,
            'stocks_count': 0,
            'expense_ratio': 0.45,
            'exit_load': 0.25,
            'min_investment': 500,
            'fund_manager': 'Anil Bamboli'
        },
        {
            'name': 'ICICI Prudential Corporate Bond Fund',
            'category': 'Corporate Bond',
            'rating': 4.0,
            'returns_3y': 8.2,
            'returns_5y': 7.5,
            'returns_10y': 7.9,
            'aum': 12450,
            'stocks_count': 0,
            'expense_ratio': 0.55,
            'exit_load': 0.25,
            'min_investment': 500,
            'fund_manager': 'Manish Banthia'
        }
    ],
    'hybrid': [
        {
            'name': 'ICICI Prudential Balanced Advantage Fund',
            'category': 'Balanced Advantage',
            'rating': 4.3,
            'returns_3y': 12.8,
            'returns_5y': 11.2,
            'returns_10y': 10.5,
            'aum': 22580,
            'stocks_count': 45,
            'expense_ratio': 1.65,
            'exit_load': 1.0,
            'min_investment': 500,
            'fund_manager': 'Sankaran Naren'
        },
        {
            'name': 'HDFC Balanced Advantage Fund',
            'category': 'Balanced Advantage',
            'rating': 4.1,
            'returns_3y': 12.2,
            'returns_5y': 10.8,
            'returns_10y': 10.1,
            'aum': 18960,
            'stocks_count': 52,
            'expense_ratio': 1.75,
            'exit_load': 1.0,
            'min_investment': 500,
            'fund_manager': 'Prashant Jain'
        }
    ],
    'international': [
        {
            'name': 'Motilal Oswal Nasdaq 100 Fund',
            'category': 'International',
            'rating': 4.4,
            'returns_3y': 18.9,
            'returns_5y': 16.5,
            'returns_10y': 14.8,
            'aum': 5680,
            'stocks_count': 100,
            'expense_ratio': 2.5,
            'exit_load': 1.0,
            'min_investment': 500,
            'fund_manager': 'Rakesh Singh'
        },
        {
            'name': 'Franklin India Feeder Franklin U.S. Opportunities Fund',
            'category': 'International',
            'rating': 4.2,
            'returns_3y': 17.5,
            'returns_5y': 15.2,
            'returns_10y': 13.8,
            'aum': 4250,
            'stocks_count': 85,
            'expense_ratio': 2.75,
            'exit_load': 1.0,
            'min_investment': 500,
            'fund_manager': 'Anoop Bhaskar'
        }
    ]
}

# Enhanced AI System for Financial Analysis
class EnhancedFinancialAdvisorAI:
    def __init__(self):
        self.system_message = """You are Dr. Rajesh Khanna, a leading behavioral finance expert and certified financial planner with 20 years of experience in the Indian market. Your expertise includes:

1. Deep understanding of Indian mutual fund industry and market dynamics
2. Identifying and overcoming behavioral biases in Indian investors
3. Creating personalized investment strategies based on Indian market conditions
4. Helping investors navigate market volatility and emotional decision-making
5. Expertise in Indian tax-saving instruments and regulations

Your approach:
- Always consider Indian market specifics (monsoon impact, festival seasons, budget cycles)
- Address cultural and emotional barriers to investing
- Provide detailed fund analysis with ratings, returns, and risk metrics
- Focus on long-term wealth building suitable for Indian families
- Consider inflation, currency factors, and Indian economic cycles
- Suggest tax-efficient investment strategies under Indian tax laws

Be empathetic, culturally aware, and focus on building confidence in Indian investors."""

    async def analyze_behavioral_profile(self, user_data: dict) -> dict:
        """Enhanced behavioral analysis for Indian market context"""
        
        biases = []
        confidence_level = "medium"
        age = user_data.get('age', 30)
        income = user_data.get('income', 50000)
        experience = user_data.get('investment_experience', 'beginner')
        occupation = user_data.get('occupation', '').lower()
        
        # Enhanced bias detection
        if experience == 'beginner':
            biases.append("overconfidence_bias")
            biases.append("herding_behavior")
            confidence_level = "low"
        
        if user_data.get('risk_tolerance') == 'low':
            biases.append("loss_aversion")
            biases.append("status_quo_bias")
            
        if 'tech' in occupation or 'software' in occupation or 'it' in occupation:
            biases.append("sector_bias")
            biases.append("recency_bias")
            
        if 'doctor' in occupation or 'engineer' in occupation:
            biases.append("overconfidence_bias")
            
        if age < 25:
            biases.append("overconfidence_bias")
            biases.append("fomo_bias")
        elif age > 45:
            biases.append("loss_aversion")
            biases.append("home_bias")
            
        if income < 500000:
            biases.append("small_numbers_bias")
        elif income > 2000000:
            biases.append("overconfidence_bias")
            
        # Calculate enhanced risk score
        risk_score = 5  # baseline
        
        # Age factor
        if age < 30:
            risk_score += 2
        elif age < 40:
            risk_score += 1
        elif age > 50:
            risk_score -= 1
        elif age > 60:
            risk_score -= 2
            
        # Income factor
        if income > 1000000:
            risk_score += 2
        elif income > 500000:
            risk_score += 1
        elif income < 300000:
            risk_score -= 1
            
        # Experience factor
        if experience == 'experienced':
            risk_score += 2
        elif experience == 'intermediate':
            risk_score += 1
        elif experience == 'beginner':
            risk_score -= 1
            
        # Occupation factor
        if any(term in occupation for term in ['entrepreneur', 'business', 'trader']):
            risk_score += 2
        elif any(term in occupation for term in ['government', 'teacher', 'clerk']):
            risk_score -= 1
            
        risk_score = max(1, min(10, risk_score))
        
        # Determine confidence level
        if risk_score >= 7 and experience != 'beginner':
            confidence_level = "high"
        elif risk_score <= 3 or experience == 'beginner':
            confidence_level = "low"
        
        behavioral_profile = self._get_behavioral_profile(biases, risk_score, age, income)
        
        return {
            'risk_score': risk_score,
            'behavioral_biases': biases,
            'behavioral_profile': behavioral_profile,
            'confidence_level': confidence_level,
            'market_sentiment': self._assess_market_sentiment(risk_score, biases),
            'investment_personality': self._determine_investment_personality(user_data, risk_score)
        }
    
    def _get_behavioral_profile(self, biases: List[str], risk_score: int, age: int, income: float) -> str:
        """Enhanced behavioral profiling"""
        if risk_score <= 3:
            return "Conservative Indian Investor"
        elif risk_score <= 5:
            return "Moderate Indian Investor"
        elif risk_score <= 7:
            return "Balanced Growth Investor"
        elif risk_score <= 8:
            return "Aggressive Growth Investor"
        else:
            return "High-Risk Wealth Builder"
    
    def _assess_market_sentiment(self, risk_score: int, biases: List[str]) -> str:
        """Assess investor's market sentiment"""
        if 'loss_aversion' in biases and 'status_quo_bias' in biases:
            return "Risk-averse and market-fearful"
        elif 'overconfidence_bias' in biases and 'fomo_bias' in biases:
            return "Overconfident and trend-following"
        elif risk_score >= 7:
            return "Optimistic and growth-oriented"
        else:
            return "Cautious and stability-seeking"
    
    def _determine_investment_personality(self, user_data: dict, risk_score: int) -> str:
        """Determine investment personality type"""
        age = user_data.get('age', 30)
        goals = user_data.get('financial_goals', [])
        
        if 'retirement' in goals and age > 40:
            return "Retirement Planner"
        elif 'education' in goals:
            return "Family Goal Investor"
        elif 'wealth' in goals and risk_score >= 7:
            return "Wealth Creator"
        elif 'tax' in goals:
            return "Tax-Efficient Investor"
        else:
            return "Goal-Based Investor"
    
    async def generate_investment_recommendations(self, user_data: dict, behavioral_analysis: dict) -> dict:
        """Generate enhanced investment recommendations with real fund data"""
        
        risk_score = behavioral_analysis['risk_score']
        behavioral_profile = behavioral_analysis['behavioral_profile']
        age = user_data.get('age', 30)
        income = user_data.get('income', 500000)
        goals = user_data.get('financial_goals', [])
        timeline = user_data.get('investment_timeline', '5-10 years')
        
        # Enhanced portfolio allocation based on comprehensive analysis
        allocation = self._calculate_optimal_allocation(risk_score, age, income, goals, timeline)
        
        # Select best funds based on allocation
        mutual_funds = self._select_best_funds(allocation, behavioral_analysis, user_data)
        
        # Generate comprehensive rationale
        rationale = self._generate_comprehensive_rationale(user_data, behavioral_analysis, allocation)
        
        # Enhanced risk mitigation
        risk_mitigation = self._generate_enhanced_risk_mitigation(behavioral_analysis, user_data)
        
        # Calculate expected returns with Indian market context
        expected_returns = self._calculate_indian_market_returns(allocation, risk_score, timeline)
        
        # Generate tax implications
        tax_implications = self._generate_tax_implications(allocation, goals, income)
        
        # Investment strategy
        investment_strategy = self._generate_investment_strategy(user_data, behavioral_analysis)
        
        return {
            'portfolio_allocation': allocation,
            'mutual_funds': mutual_funds,
            'rationale': rationale,
            'risk_mitigation': risk_mitigation,
            'expected_returns': expected_returns,
            'tax_implications': tax_implications,
            'investment_strategy': investment_strategy,
            'rebalancing_frequency': self._suggest_rebalancing_frequency(risk_score),
            'sip_recommendation': self._calculate_sip_recommendation(income, allocation)
        }
    
    def _calculate_optimal_allocation(self, risk_score: int, age: int, income: float, goals: List[str], timeline: str) -> dict:
        """Calculate optimal allocation based on multiple factors"""
        
        # Base allocation based on risk score
        if risk_score <= 3:  # Conservative
            base_allocation = {
                'large_cap': 35,
                'debt': 45,
                'hybrid': 20,
                'international': 0
            }
        elif risk_score <= 5:  # Moderate
            base_allocation = {
                'large_cap': 40,
                'mid_cap': 15,
                'debt': 30,
                'hybrid': 15,
                'international': 0
            }
        elif risk_score <= 7:  # Balanced
            base_allocation = {
                'large_cap': 35,
                'mid_cap': 25,
                'debt': 20,
                'hybrid': 15,
                'international': 5
            }
        else:  # Aggressive
            base_allocation = {
                'large_cap': 30,
                'mid_cap': 30,
                'small_cap': 20,
                'debt': 10,
                'international': 10
            }
        
        # Age-based adjustments
        if age < 30:
            # Young investors can take more risk
            if 'debt' in base_allocation:
                base_allocation['debt'] = max(10, base_allocation['debt'] - 10)
            if 'large_cap' in base_allocation:
                base_allocation['large_cap'] += 5
            if 'mid_cap' in base_allocation:
                base_allocation['mid_cap'] += 5
        elif age > 50:
            # Older investors need more stability
            if 'debt' in base_allocation:
                base_allocation['debt'] += 15
            if 'small_cap' in base_allocation:
                base_allocation['small_cap'] = max(0, base_allocation['small_cap'] - 10)
            if 'mid_cap' in base_allocation:
                base_allocation['mid_cap'] = max(0, base_allocation['mid_cap'] - 5)
        
        # Goal-based adjustments
        if 'retirement' in goals:
            base_allocation['debt'] = base_allocation.get('debt', 0) + 10
            base_allocation['large_cap'] = base_allocation.get('large_cap', 0) + 5
        
        if 'tax' in goals:
            # Add ELSS allocation
            base_allocation['elss'] = 15
        
        # Normalize to 100%
        total = sum(base_allocation.values())
        for key in base_allocation:
            base_allocation[key] = round((base_allocation[key] / total) * 100)
        
        return base_allocation
    
    def _select_best_funds(self, allocation: dict, behavioral_analysis: dict, user_data: dict) -> List[dict]:
        """Select best mutual funds based on allocation and user profile"""
        
        selected_funds = []
        
        for category, percentage in allocation.items():
            if percentage > 0:
                if category in INDIAN_MUTUAL_FUNDS:
                    # Select best fund from category based on rating and returns
                    funds = INDIAN_MUTUAL_FUNDS[category]
                    
                    # Sort by rating and 3-year returns
                    sorted_funds = sorted(funds, key=lambda x: (x['rating'], x['returns_3y']), reverse=True)
                    
                    # Select top fund
                    best_fund = sorted_funds[0].copy()
                    best_fund['allocation_percentage'] = percentage
                    best_fund['monthly_sip'] = self._calculate_fund_sip(user_data.get('income', 500000), percentage)
                    
                    selected_funds.append(best_fund)
        
        return selected_funds
    
    def _calculate_fund_sip(self, income: float, allocation_percentage: float) -> int:
        """Calculate recommended SIP amount for a fund"""
        # Assume 20% of income for investments
        monthly_investment = (income * 0.20) / 12
        fund_sip = (monthly_investment * allocation_percentage) / 100
        return max(500, round(fund_sip, -2))  # Minimum 500, rounded to nearest 100
    
    def _generate_comprehensive_rationale(self, user_data: dict, behavioral_analysis: dict, allocation: dict) -> str:
        """Generate comprehensive investment rationale"""
        
        age = user_data.get('age', 30)
        income = user_data.get('income', 500000)
        profile = behavioral_analysis['behavioral_profile']
        personality = behavioral_analysis['investment_personality']
        
        rationale = f"""
        **Personalized Investment Strategy for {user_data.get('name', 'You')}**

        **Your Profile Analysis:**
        - Age: {age} years ({self._get_age_advantage(age)})
        - Risk Profile: {profile}
        - Investment Personality: {personality}
        - Annual Income: ₹{income:,}

        **Why This Allocation Works:**

        🎯 **Age-Appropriate Strategy**: At {age}, you have a {"long" if age < 40 else "moderate" if age < 55 else "short"} investment horizon, allowing for {"higher growth potential" if age < 40 else "balanced growth with stability" if age < 55 else "capital preservation focus"}.

        💡 **Behavioral Considerations**: 
        """
        
        biases = behavioral_analysis.get('behavioral_biases', [])
        for bias in biases:
            if bias == 'loss_aversion':
                rationale += "- Your conservative approach is balanced with growth assets to beat inflation while preserving capital.\n"
            elif bias == 'overconfidence_bias':
                rationale += "- Diversified approach prevents over-concentration and emotional decision-making.\n"
            elif bias == 'herding_behavior':
                rationale += "- Systematic investment approach helps avoid market timing and crowd psychology.\n"
            elif bias == 'sector_bias':
                rationale += "- Multi-sector diversification reduces concentration risk in your familiar sectors.\n"
        
        rationale += f"""
        📊 **Portfolio Rationale**:
        """
        
        if allocation.get('large_cap', 0) > 0:
            rationale += f"- **Large Cap ({allocation['large_cap']}%)**: Provides stability and consistent returns from established companies.\n"
        
        if allocation.get('mid_cap', 0) > 0:
            rationale += f"- **Mid Cap ({allocation['mid_cap']}%)**: Captures growth potential of emerging companies with higher returns.\n"
        
        if allocation.get('small_cap', 0) > 0:
            rationale += f"- **Small Cap ({allocation['small_cap']}%)**: High growth potential for long-term wealth creation.\n"
        
        if allocation.get('debt', 0) > 0:
            rationale += f"- **Debt Funds ({allocation['debt']}%)**: Provides stability, regular income, and reduces overall portfolio volatility.\n"
        
        if allocation.get('hybrid', 0) > 0:
            rationale += f"- **Hybrid Funds ({allocation['hybrid']}%)**: Balanced approach with automatic rebalancing between equity and debt.\n"
        
        if allocation.get('international', 0) > 0:
            rationale += f"- **International Funds ({allocation['international']}%)**: Global diversification and currency hedging.\n"
        
        rationale += """
        🇮🇳 **Indian Market Context**: This allocation considers Indian market cycles, monsoon impact, budget announcements, and festival season volatility.
        """
        
        return rationale
    
    def _get_age_advantage(self, age: int) -> str:
        """Get age-based investment advantage"""
        if age < 25:
            return "Maximum time for compounding"
        elif age < 35:
            return "Strong compounding advantage"
        elif age < 45:
            return "Good wealth building phase"
        elif age < 55:
            return "Wealth consolidation phase"
        else:
            return "Wealth preservation phase"
    
    def _generate_enhanced_risk_mitigation(self, behavioral_analysis: dict, user_data: dict) -> str:
        """Generate enhanced risk mitigation strategies"""
        
        strategies = []
        biases = behavioral_analysis.get('behavioral_biases', [])
        risk_score = behavioral_analysis.get('risk_score', 5)
        
        # Universal strategies
        strategies.append("🎯 **SIP Strategy**: Invest through Systematic Investment Plans to average out market volatility")
        strategies.append("⏰ **Time Diversification**: Stay invested for at least 5-7 years to ride out market cycles")
        strategies.append("🔄 **Regular Rebalancing**: Review and rebalance portfolio annually or when allocation drifts by 5%")
        
        # Bias-specific strategies
        if 'loss_aversion' in biases:
            strategies.append("💪 **Confidence Building**: Start with conservative allocation and gradually increase risk as comfort grows")
            strategies.append("📈 **Focus on Long-term**: Avoid checking portfolio daily; review monthly or quarterly")
        
        if 'overconfidence_bias' in biases:
            strategies.append("🎓 **Continuous Learning**: Stay updated with market research but avoid frequent changes")
            strategies.append("📊 **Stick to Plan**: Resist urge to time the market or chase hot funds")
        
        if 'herding_behavior' in biases:
            strategies.append("🧠 **Independent Thinking**: Make decisions based on your goals, not market noise")
            strategies.append("📰 **Limit Media Exposure**: Reduce consumption of daily market news and tips")
        
        if 'sector_bias' in biases:
            strategies.append("🌐 **Diversification**: Maintain exposure across different sectors and market caps")
            strategies.append("🔍 **Fund Selection**: Choose funds with diverse holdings across sectors")
        
        # Risk score specific strategies
        if risk_score <= 3:
            strategies.append("🛡️ **Emergency Fund**: Maintain 6-12 months of expenses in liquid funds")
            strategies.append("📋 **Asset Allocation**: Maintain 60-70% in low-risk instruments initially")
        elif risk_score >= 8:
            strategies.append("⚖️ **Risk Management**: Never invest more than 10% in any single fund")
            strategies.append("💰 **Profit Booking**: Book profits when equity allocation exceeds target by 10%")
        
        # Indian market specific
        strategies.append("🇮🇳 **Indian Market Cycles**: Understand and prepare for budget, monsoon, and festival impacts")
        strategies.append("💸 **Tax Planning**: Optimize investments for tax efficiency under Indian tax laws")
        strategies.append("🏛️ **Regulatory Awareness**: Stay informed about SEBI regulations and fund changes")
        
        return "\n".join(strategies)
    
    def _calculate_indian_market_returns(self, allocation: dict, risk_score: int, timeline: str) -> str:
        """Calculate expected returns with Indian market context"""
        
        # Expected returns by asset class (post-tax, inflation-adjusted)
        returns = {
            'large_cap': 12.0,
            'mid_cap': 15.0,
            'small_cap': 18.0,
            'debt': 7.5,
            'hybrid': 10.0,
            'international': 11.0,
            'elss': 13.0
        }
        
        # Calculate weighted average return
        weighted_return = 0
        for category, percentage in allocation.items():
            if category in returns:
                weighted_return += (percentage * returns[category]) / 100
        
        # Timeline adjustments
        if '1-3 years' in timeline:
            weighted_return *= 0.9  # Lower returns for short term
        elif '10+ years' in timeline:
            weighted_return *= 1.1  # Higher returns for long term
        
        # Risk adjustments
        if risk_score <= 3:
            lower_range = weighted_return - 2
            upper_range = weighted_return + 1
        elif risk_score >= 8:
            lower_range = weighted_return - 3
            upper_range = weighted_return + 4
        else:
            lower_range = weighted_return - 2
            upper_range = weighted_return + 2
        
        return f"""
        **Expected Returns (Indian Market Context):**
        
        📊 **Annual Returns**: {lower_range:.1f}% - {upper_range:.1f}%
        📈 **Average Expected**: {weighted_return:.1f}%
        
        **Growth Projections:**
        - **5 Years**: ₹10,000 SIP → ₹{self._calculate_sip_value(10000, weighted_return, 5):,.0f}
        - **10 Years**: ₹10,000 SIP → ₹{self._calculate_sip_value(10000, weighted_return, 10):,.0f}
        - **15 Years**: ₹10,000 SIP → ₹{self._calculate_sip_value(10000, weighted_return, 15):,.0f}
        
        **Important Notes:**
        - Returns are subject to market risks and past performance doesn't guarantee future results
        - Consider inflation (avg. 6% in India) when evaluating real returns
        - Actual returns may vary based on market conditions and fund performance
        """
    
    def _calculate_sip_value(self, monthly_sip: int, annual_return: float, years: int) -> float:
        """Calculate SIP maturity value"""
        monthly_return = annual_return / 12 / 100
        months = years * 12
        
        if monthly_return == 0:
            return monthly_sip * months
        
        future_value = monthly_sip * (((1 + monthly_return) ** months - 1) / monthly_return)
        return future_value
    
    def _generate_tax_implications(self, allocation: dict, goals: List[str], income: float) -> str:
        """Generate tax implications for Indian investors"""
        
        tax_info = """
        **Tax Implications (Indian Tax Laws):**
        
        📋 **Equity Funds Taxation**:
        - **Short-term** (< 1 year): 15% tax on gains
        - **Long-term** (> 1 year): 10% tax on gains above ₹1 lakh annually
        
        📋 **Debt Funds Taxation**:
        - **Short-term** (< 3 years): Added to income, taxed as per slab
        - **Long-term** (> 3 years): 20% with indexation benefit
        
        📋 **Tax-Saving Opportunities**:
        """
        
        if 'tax' in goals:
            tax_info += "- **ELSS Funds**: ₹1.5 lakh tax deduction under Section 80C\n"
        
        if income > 1000000:
            tax_info += "- **Tax Harvesting**: Book losses to offset gains\n"
        
        tax_info += """
        - **SIP Benefits**: No TDS on SIP investments
        - **Dividend Tax**: Dividend income taxed as per income slab
        
        💡 **Tax Planning Tips**:
        - Hold equity funds for >1 year to get long-term capital gains benefit
        - Use debt funds for tax-efficient income generation
        - Plan withdrawals after retirement for lower tax brackets
        """
        
        return tax_info
    
    def _generate_investment_strategy(self, user_data: dict, behavioral_analysis: dict) -> str:
        """Generate comprehensive investment strategy"""
        
        strategy = f"""
        **Your Personalized Investment Strategy:**
        
        🎯 **Phase 1: Foundation Building (Months 1-6)**
        - Start with conservative allocation to build confidence
        - Focus on large-cap and hybrid funds
        - Establish emergency fund (6 months expenses)
        
        🚀 **Phase 2: Growth Acceleration (Months 7-24)**
        - Gradually increase mid-cap allocation
        - Add international diversification
        - Increase SIP amounts with salary increments
        
        📈 **Phase 3: Wealth Optimization (Years 2+)**
        - Fine-tune allocation based on performance
        - Add small-cap funds for higher growth
        - Regular portfolio rebalancing
        
        🔄 **Ongoing Strategy**:
        - Review portfolio quarterly
        - Rebalance annually or when allocation drifts >5%
        - Step-up SIP by 10% annually
        - Stay disciplined during market volatility
        """
        
        return strategy
    
    def _suggest_rebalancing_frequency(self, risk_score: int) -> str:
        """Suggest rebalancing frequency based on risk profile"""
        if risk_score <= 3:
            return "Semi-annually (every 6 months)"
        elif risk_score <= 6:
            return "Annually (once a year)"
        else:
            return "Quarterly (every 3 months)"
    
    def _calculate_sip_recommendation(self, income: float, allocation: dict) -> dict:
        """Calculate SIP recommendations"""
        
        # Assume 20% of income for investments
        monthly_investment = (income * 0.20) / 12
        
        sip_plan = {
            'total_monthly_sip': int(monthly_investment),
            'fund_wise_sip': {}
        }
        
        for category, percentage in allocation.items():
            if percentage > 0:
                fund_sip = (monthly_investment * percentage) / 100
                sip_plan['fund_wise_sip'][category] = max(500, round(fund_sip, -2))
        
        return sip_plan

# Initialize enhanced AI advisor
ai_advisor = EnhancedFinancialAdvisorAI()

# API Routes
@app.get("/")
async def root():
    return {"message": "InvestWise AI - Enhanced Financial Advisory Platform"}

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
    """Perform enhanced behavioral risk assessment"""
    try:
        user_data = users_collection.find_one({"user_id": user_id})
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        behavioral_analysis = await ai_advisor.analyze_behavioral_profile(user_data)
        
        assessment_data = {
            "user_id": user_id,
            "risk_score": behavioral_analysis['risk_score'],
            "behavioral_profile": behavioral_analysis['behavioral_profile'],
            "behavioral_biases": behavioral_analysis['behavioral_biases'],
            "confidence_level": behavioral_analysis['confidence_level'],
            "market_sentiment": behavioral_analysis['market_sentiment'],
            "investment_personality": behavioral_analysis['investment_personality'],
            "created_at": datetime.now()
        }
        
        assessments_collection.insert_one(assessment_data)
        return behavioral_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/investment-recommendations")
async def get_investment_recommendations(user_id: str):
    """Get enhanced investment recommendations"""
    try:
        user_data = users_collection.find_one({"user_id": user_id})
        assessment_data = assessments_collection.find_one({"user_id": user_id})
        
        if not user_data or not assessment_data:
            raise HTTPException(status_code=404, detail="User profile or assessment not found")
        
        recommendations = await ai_advisor.generate_investment_recommendations(user_data, assessment_data)
        
        recommendation_data = {
            "user_id": user_id,
            "portfolio_allocation": recommendations['portfolio_allocation'],
            "mutual_funds": recommendations['mutual_funds'],
            "rationale": recommendations['rationale'],
            "risk_mitigation": recommendations['risk_mitigation'],
            "expected_returns": recommendations['expected_returns'],
            "tax_implications": recommendations['tax_implications'],
            "investment_strategy": recommendations['investment_strategy'],
            "rebalancing_frequency": recommendations['rebalancing_frequency'],
            "sip_recommendation": recommendations['sip_recommendation'],
            "created_at": datetime.now()
        }
        
        recommendations_collection.insert_one(recommendation_data)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/{user_id}/dashboard")
async def get_user_dashboard(user_id: str):
    """Get enhanced user dashboard data"""
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

@app.get("/api/famous-quotes")
async def get_famous_quotes():
    """Get famous investment quotes for loading screens"""
    quotes = [
        {
            "quote": "The stock market is a device for transferring money from the impatient to the patient.",
            "author": "Warren Buffett"
        },
        {
            "quote": "Risk comes from not knowing what you're doing.",
            "author": "Warren Buffett"
        },
        {
            "quote": "It's not how much money you make, but how much money you keep, how hard it works for you, and how many generations you keep it for.",
            "author": "Robert Kiyosaki"
        },
        {
            "quote": "The investor's chief problem - and even his worst enemy - is likely to be himself.",
            "author": "Benjamin Graham"
        },
        {
            "quote": "Price is what you pay. Value is what you get.",
            "author": "Warren Buffett"
        },
        {
            "quote": "The four most dangerous words in investing are: 'this time it's different.'",
            "author": "Sir John Templeton"
        },
        {
            "quote": "Compound interest is the eighth wonder of the world. He who understands it, earns it; he who doesn't, pays it.",
            "author": "Albert Einstein"
        },
        {
            "quote": "The time to buy is when there's blood in the streets.",
            "author": "Baron Rothschild"
        }
    ]
    return {"quotes": quotes}

@app.get("/api/market-insights")
async def get_market_insights():
    """Get current market insights for enhanced recommendations"""
    insights = {
        "market_condition": "Moderately Bullish",
        "recommended_sectors": ["Technology", "Healthcare", "Finance"],
        "avoid_sectors": ["Real Estate", "Metals"],
        "sip_timing": "Excellent time to start SIP",
        "market_volatility": "Moderate",
        "inflation_impact": "Monitor RBI policy changes",
        "currency_outlook": "Rupee expected to stabilize"
    }
    return insights

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)