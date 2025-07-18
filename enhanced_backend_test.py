#!/usr/bin/env python3
import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get backend URL from frontend .env file
def get_backend_url():
    with open('/app/frontend/.env', 'r') as f:
        for line in f:
            if line.startswith('REACT_APP_BACKEND_URL='):
                return line.strip().split('=')[1]
    raise ValueError("REACT_APP_BACKEND_URL not found in frontend/.env")

# Set up the base URL for API requests
BASE_URL = f"{get_backend_url()}/api"
print(f"Using backend URL: {BASE_URL}")

# Test data based on the review request - Rajesh Sharma
test_user = {
    "name": "Rajesh Sharma",
    "age": 28,
    "occupation": "Software Engineer",
    "income": 800000.0,
    "current_savings": 150000.0,
    "investment_experience": "intermediate",
    "risk_tolerance": "moderate",
    "financial_goals": ["wealth", "tax"],
    "investment_timeline": "5-10 years"
}

# Store user_id for subsequent tests
user_id = None

def test_health_check():
    """Test the health check endpoint"""
    print("\n=== Testing Health Check API ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health check test passed")
    return True

def test_enhanced_user_profile_creation():
    """Test enhanced user profile creation API with realistic data"""
    global user_id
    
    print("\n=== Testing Enhanced User Profile Creation API ===")
    response = requests.post(f"{BASE_URL}/user-profile", json=test_user)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "message" in response.json()
    
    # Store user_id for subsequent tests
    user_id = response.json()["user_id"]
    print(f"✅ Enhanced user profile creation test passed. User ID: {user_id}")
    return True

def test_enhanced_risk_assessment():
    """Test enhanced behavioral risk assessment API with new comprehensive analysis"""
    global user_id
    
    if not user_id:
        print("❌ Cannot test risk assessment without a valid user_id")
        return False
    
    print("\n=== Testing Enhanced Behavioral Risk Assessment API ===")
    response = requests.post(f"{BASE_URL}/risk-assessment?user_id={user_id}")
    print(f"Status Code: {response.status_code}")
    
    response_data = response.json()
    print("Enhanced Analysis Results:")
    print(f"- Risk Score: {response_data.get('risk_score')}")
    print(f"- Behavioral Profile: {response_data.get('behavioral_profile')}")
    print(f"- Investment Personality: {response_data.get('investment_personality')}")
    print(f"- Market Sentiment: {response_data.get('market_sentiment')}")
    print(f"- Behavioral Biases: {response_data.get('behavioral_biases')}")
    print(f"- Confidence Level: {response_data.get('confidence_level')}")
    
    assert response.status_code == 200
    
    # Test enhanced fields
    required_fields = [
        "risk_score", "behavioral_biases", "behavioral_profile", 
        "confidence_level", "market_sentiment", "investment_personality"
    ]
    
    for field in required_fields:
        assert field in response_data, f"Missing enhanced field: {field}"
    
    # Verify enhanced analysis for Software Engineer with moderate risk
    biases = response_data["behavioral_biases"]
    assert "sector_bias" in biases, "Should detect sector bias for tech professional"
    assert "recency_bias" in biases, "Should detect recency bias for tech professional"
    
    # Verify risk score is appropriate for intermediate, moderate risk profile with high income
    risk_score = response_data["risk_score"]
    assert 1 <= risk_score <= 10, f"Risk score {risk_score} should be between 1-10"
    
    # For Software Engineer with ₹8L income and intermediate experience, expect higher risk score
    assert risk_score >= 6, f"Risk score {risk_score} should be higher for high-income tech professional"
    
    # Verify investment personality
    personality = response_data["investment_personality"]
    assert personality in ["Wealth Creator", "Tax-Efficient Investor", "Goal-Based Investor"], f"Unexpected personality: {personality}"
    
    print("✅ Enhanced behavioral risk assessment test passed")
    return True

def test_enhanced_investment_recommendations():
    """Test enhanced investment recommendations API with comprehensive fund database"""
    global user_id
    
    if not user_id:
        print("❌ Cannot test investment recommendations without a valid user_id")
        return False
    
    print("\n=== Testing Enhanced Investment Recommendations API ===")
    response = requests.post(f"{BASE_URL}/investment-recommendations?user_id={user_id}")
    print(f"Status Code: {response.status_code}")
    
    response_data = response.json()
    print("Enhanced Recommendations Results:")
    print(f"- Portfolio allocation: {response_data.get('portfolio_allocation', {})}")
    print(f"- Number of mutual funds: {len(response_data.get('mutual_funds', []))}")
    
    # Print detailed fund information
    mutual_funds = response_data.get('mutual_funds', [])
    for i, fund in enumerate(mutual_funds):
        print(f"  Fund {i+1}: {fund.get('name')} ({fund.get('category')})")
        print(f"    - Rating: {fund.get('rating')}")
        print(f"    - 3Y Returns: {fund.get('returns_3y')}%")
        print(f"    - 5Y Returns: {fund.get('returns_5y')}%")
        print(f"    - AUM: ₹{fund.get('aum')} Cr")
        print(f"    - Allocation: {fund.get('allocation_percentage')}%")
        print(f"    - Monthly SIP: ₹{fund.get('monthly_sip')}")
    
    assert response.status_code == 200
    
    # Test enhanced fields
    enhanced_fields = [
        "portfolio_allocation", "mutual_funds", "rationale", "risk_mitigation", 
        "expected_returns", "tax_implications", "investment_strategy", 
        "rebalancing_frequency", "sip_recommendation"
    ]
    
    for field in enhanced_fields:
        assert field in response_data, f"Missing enhanced field: {field}"
    
    # Verify mutual funds have enhanced data
    assert len(response_data["mutual_funds"]) > 0
    
    for fund in response_data["mutual_funds"]:
        # Test comprehensive fund data
        fund_fields = ["name", "category", "rating", "returns_3y", "returns_5y", "aum", "allocation_percentage", "monthly_sip"]
        for field in fund_fields:
            assert field in fund, f"Missing fund field: {field}"
        
        # Verify fund data quality
        assert fund["rating"] >= 3.0, f"Fund rating {fund['rating']} should be >= 3.0"
        assert fund["returns_3y"] > 0, f"3Y returns should be positive"
        assert fund["aum"] > 0, f"AUM should be positive"
        assert fund["monthly_sip"] >= 500, f"Monthly SIP should be at least ₹500"
    
    # Verify portfolio allocation adds up to 100%
    allocation_sum = sum(response_data["portfolio_allocation"].values())
    assert abs(allocation_sum - 100) < 0.1, f"Portfolio allocation sum {allocation_sum} should be 100%"
    
    # Test SIP recommendations
    sip_rec = response_data["sip_recommendation"]
    assert "total_monthly_sip" in sip_rec
    assert "fund_wise_sip" in sip_rec
    assert sip_rec["total_monthly_sip"] > 0
    
    # Test tax implications for tax goal
    tax_implications = response_data["tax_implications"]
    assert "ELSS" in tax_implications, "Should mention ELSS for tax goal"
    
    print("✅ Enhanced investment recommendations test passed")
    return True

def test_enhanced_dashboard():
    """Test enhanced user dashboard API with comprehensive data retrieval"""
    global user_id
    
    if not user_id:
        print("❌ Cannot test user dashboard without a valid user_id")
        return False
    
    print("\n=== Testing Enhanced User Dashboard API ===")
    response = requests.get(f"{BASE_URL}/user/{user_id}/dashboard")
    print(f"Status Code: {response.status_code}")
    
    response_data = response.json()
    print("Enhanced Dashboard Data:")
    print(f"- User profile: {response_data.get('user_profile', {}).get('name')}")
    print(f"- Risk assessment: {response_data.get('risk_assessment', {}).get('behavioral_profile')}")
    print(f"- Investment personality: {response_data.get('risk_assessment', {}).get('investment_personality')}")
    print(f"- Recommendations available: {'recommendations' in response_data and response_data['recommendations'] is not None}")
    
    assert response.status_code == 200
    assert "user_profile" in response_data
    assert "risk_assessment" in response_data
    assert "recommendations" in response_data
    
    # Verify user profile data
    user_profile = response_data["user_profile"]
    assert user_profile["name"] == test_user["name"]
    assert user_profile["age"] == test_user["age"]
    assert user_profile["occupation"] == test_user["occupation"]
    assert user_profile["income"] == test_user["income"]
    
    # Verify enhanced risk assessment data
    risk_assessment = response_data["risk_assessment"]
    enhanced_risk_fields = ["risk_score", "behavioral_profile", "investment_personality", "market_sentiment"]
    for field in enhanced_risk_fields:
        assert field in risk_assessment, f"Missing enhanced risk field: {field}"
    
    # Verify enhanced recommendations data
    recommendations = response_data["recommendations"]
    enhanced_rec_fields = ["portfolio_allocation", "mutual_funds", "tax_implications", "investment_strategy", "sip_recommendation"]
    for field in enhanced_rec_fields:
        assert field in recommendations, f"Missing enhanced recommendation field: {field}"
    
    print("✅ Enhanced user dashboard test passed")
    return True

def test_fund_database_quality():
    """Test the quality and comprehensiveness of the mutual fund database"""
    global user_id
    
    if not user_id:
        print("❌ Cannot test fund database without a valid user_id")
        return False
    
    print("\n=== Testing Mutual Fund Database Quality ===")
    
    # Get recommendations to access fund data
    response = requests.post(f"{BASE_URL}/investment-recommendations?user_id={user_id}")
    assert response.status_code == 200
    
    response_data = response.json()
    mutual_funds = response_data.get('mutual_funds', [])
    
    print(f"Testing {len(mutual_funds)} recommended funds:")
    
    for fund in mutual_funds:
        print(f"- {fund['name']} ({fund['category']})")
        
        # Test comprehensive fund data
        assert fund['rating'] >= 3.0, f"Fund {fund['name']} has low rating: {fund['rating']}"
        assert fund['returns_3y'] > 0, f"Fund {fund['name']} has non-positive 3Y returns"
        assert fund['returns_5y'] > 0, f"Fund {fund['name']} has non-positive 5Y returns"
        assert fund['aum'] > 1000, f"Fund {fund['name']} has very low AUM: {fund['aum']}"
        assert 'expense_ratio' in fund, f"Fund {fund['name']} missing expense ratio"
        assert 'fund_manager' in fund, f"Fund {fund['name']} missing fund manager"
        
        # Test realistic data ranges
        assert 0.1 <= fund['expense_ratio'] <= 3.0, f"Unrealistic expense ratio for {fund['name']}"
        assert 5.0 <= fund['returns_3y'] <= 35.0, f"Unrealistic 3Y returns for {fund['name']}"
        
        print(f"  ✓ Rating: {fund['rating']}, 3Y: {fund['returns_3y']}%, AUM: ₹{fund['aum']}Cr")
    
    print("✅ Mutual fund database quality test passed")
    return True

def test_mongodb_integration():
    """Test MongoDB integration by verifying data persistence"""
    global user_id
    
    if not user_id:
        print("❌ Cannot test MongoDB integration without a valid user_id")
        return False
    
    print("\n=== Testing MongoDB Database Integration ===")
    
    # Test data persistence by retrieving the user dashboard again
    response = requests.get(f"{BASE_URL}/user/{user_id}/dashboard")
    assert response.status_code == 200
    
    # Verify all collections have data
    response_data = response.json()
    assert response_data["user_profile"] is not None
    assert response_data["risk_assessment"] is not None
    assert response_data["recommendations"] is not None
    
    # Verify data integrity
    assert response_data["user_profile"]["user_id"] == user_id
    assert response_data["risk_assessment"]["user_id"] == user_id
    assert response_data["recommendations"]["user_id"] == user_id
    
    print("✅ MongoDB integration test passed - data persisted correctly")
    return True

def test_error_handling():
    """Test error handling and data validation"""
    print("\n=== Testing Error Handling and Data Validation ===")
    
    # Test invalid user profile
    invalid_user = {
        "name": "",  # Empty name
        "age": -5,   # Invalid age
        "income": -1000  # Negative income
    }
    
    response = requests.post(f"{BASE_URL}/user-profile", json=invalid_user)
    print(f"Invalid profile response: {response.status_code}")
    # Should handle gracefully (either 400 or create with defaults)
    
    # Test non-existent user
    response = requests.post(f"{BASE_URL}/risk-assessment?user_id=non-existent-id")
    print(f"Non-existent user response: {response.status_code}")
    assert response.status_code == 404
    
    print("✅ Error handling test passed")
    return True

def run_all_enhanced_tests():
    """Run all enhanced tests in sequence"""
    print("\n🚀 Starting Enhanced InvestWise AI Backend API Tests\n")
    print("Testing enhanced features:")
    print("- Comprehensive mutual fund database with ratings, returns, AUM")
    print("- Enhanced behavioral analysis with investment personality")
    print("- Improved AI logic with Indian market context")
    print("- Tax implications and investment strategy")
    print("- SIP recommendations and rebalancing frequency")
    
    tests = [
        ("Health Check", test_health_check),
        ("Enhanced User Profile Creation", test_enhanced_user_profile_creation),
        ("Enhanced Behavioral Risk Assessment", test_enhanced_risk_assessment),
        ("Enhanced Investment Recommendations", test_enhanced_investment_recommendations),
        ("Enhanced Dashboard", test_enhanced_dashboard),
        ("Fund Database Quality", test_fund_database_quality),
        ("MongoDB Integration", test_mongodb_integration),
        ("Error Handling", test_error_handling)
    ]
    
    results = {}
    
    for name, test_func in tests:
        try:
            success = test_func()
            results[name] = "✅ PASSED" if success else "❌ FAILED"
        except Exception as e:
            print(f"❌ Error during {name} test: {str(e)}")
            results[name] = f"❌ ERROR: {str(e)}"
    
    # Print summary
    print("\n=== Enhanced Test Results Summary ===")
    for name, result in results.items():
        print(f"{name}: {result}")
    
    # Count results
    passed = sum(1 for r in results.values() if "PASSED" in r)
    total = len(results)
    
    print(f"\n📊 Overall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All enhanced backend tests passed successfully!")
    else:
        print("⚠️ Some tests failed - please review the issues above")

if __name__ == "__main__":
    run_all_enhanced_tests()