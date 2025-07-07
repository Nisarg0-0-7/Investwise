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

# Test data based on Ajit from the case study (30 years old, actor, risk-averse)
test_user = {
    "name": "Ajit Kumar",
    "age": 30,
    "occupation": "Actor",
    "income": 75000.0,
    "current_savings": 25000.0,
    "investment_experience": "beginner",
    "risk_tolerance": "low",
    "financial_goals": ["retirement", "emergency_fund", "wealth_creation"],
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

def test_user_profile_creation():
    """Test user profile creation API"""
    global user_id
    
    print("\n=== Testing User Profile Creation API ===")
    response = requests.post(f"{BASE_URL}/user-profile", json=test_user)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "message" in response.json()
    
    # Store user_id for subsequent tests
    user_id = response.json()["user_id"]
    print(f"✅ User profile creation test passed. User ID: {user_id}")
    return True

def test_risk_assessment():
    """Test behavioral risk assessment API"""
    global user_id
    
    if not user_id:
        print("❌ Cannot test risk assessment without a valid user_id")
        return False
    
    print("\n=== Testing Behavioral Risk Assessment API ===")
    response = requests.post(f"{BASE_URL}/risk-assessment?user_id={user_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    assert "risk_score" in response.json()
    assert "behavioral_biases" in response.json()
    assert "behavioral_profile" in response.json()
    assert "confidence_level" in response.json()
    
    # Verify expected biases for our test user (low risk tolerance, beginner)
    biases = response.json()["behavioral_biases"]
    assert "loss_aversion" in biases
    assert "overconfidence_bias" in biases
    
    print("✅ Behavioral risk assessment test passed")
    return True

def test_investment_recommendations():
    """Test investment recommendations API"""
    global user_id
    
    if not user_id:
        print("❌ Cannot test investment recommendations without a valid user_id")
        return False
    
    print("\n=== Testing Investment Recommendations API ===")
    response = requests.post(f"{BASE_URL}/investment-recommendations?user_id={user_id}")
    print(f"Status Code: {response.status_code}")
    
    # Print a truncated version of the response for readability
    response_data = response.json()
    print("Response (truncated):")
    print(f"- Portfolio allocation: {response_data.get('portfolio_allocation', {})}")
    print(f"- Number of mutual funds: {len(response_data.get('mutual_funds', []))}")
    print(f"- Expected returns: {response_data.get('expected_returns', '')}")
    
    assert response.status_code == 200
    assert "portfolio_allocation" in response_data
    assert "mutual_funds" in response_data
    assert "rationale" in response_data
    assert "risk_mitigation" in response_data
    assert "expected_returns" in response_data
    
    # Verify mutual funds are recommended
    assert len(response_data["mutual_funds"]) > 0
    
    # Verify portfolio allocation adds up to 100%
    allocation_sum = sum(response_data["portfolio_allocation"].values())
    assert abs(allocation_sum - 100) < 0.1  # Allow for small floating point differences
    
    print("✅ Investment recommendations test passed")
    return True

def test_user_dashboard():
    """Test user dashboard API"""
    global user_id
    
    if not user_id:
        print("❌ Cannot test user dashboard without a valid user_id")
        return False
    
    print("\n=== Testing User Dashboard API ===")
    response = requests.get(f"{BASE_URL}/user/{user_id}/dashboard")
    print(f"Status Code: {response.status_code}")
    
    # Print a truncated version of the response for readability
    response_data = response.json()
    print("Response (truncated):")
    print(f"- User profile: {response_data.get('user_profile', {}).get('name')}")
    print(f"- Risk assessment: {response_data.get('risk_assessment', {}).get('behavioral_profile')}")
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
    
    # Verify risk assessment data
    risk_assessment = response_data["risk_assessment"]
    assert "risk_score" in risk_assessment
    assert "behavioral_profile" in risk_assessment
    
    # Verify recommendations data
    recommendations = response_data["recommendations"]
    assert "portfolio_allocation" in recommendations
    assert "mutual_funds" in recommendations
    
    print("✅ User dashboard test passed")
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
    
    print("✅ MongoDB integration test passed - data persisted correctly")
    return True

def run_all_tests():
    """Run all tests in sequence"""
    print("\n🚀 Starting InvestWise AI Backend API Tests\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("User Profile Creation", test_user_profile_creation),
        ("Behavioral Risk Assessment", test_risk_assessment),
        ("Investment Recommendations", test_investment_recommendations),
        ("User Dashboard", test_user_dashboard),
        ("MongoDB Integration", test_mongodb_integration)
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
    print("\n=== Test Results Summary ===")
    for name, result in results.items():
        print(f"{name}: {result}")

if __name__ == "__main__":
    run_all_tests()