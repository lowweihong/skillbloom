#!/usr/bin/env python3
"""
Frontend Client Example for Learning Plan Generator API
Demonstrates how to call the backend API from frontend applications
"""

import requests
import json
import time
from typing import Dict, Any

class LearningPlanAPIClient:
    """Client for interacting with the Learning Plan Generator API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def generate_plan(self, topic: str, background: str, preferred_format: str, 
                      user_id: str = None, session_id: str = None) -> Dict[str, Any]:
        """Generate a learning plan"""
        
        payload = {
            "topic": topic,
            "background": background,
            "preferred_format": preferred_format
        }
        
        if user_id:
            payload["user_id"] = user_id
        if session_id:
            payload["session_id"] = session_id
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/generate-plan",
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_plan(self, request_id: str) -> Dict[str, Any]:
        """Retrieve a previously generated plan"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/plan/{request_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def list_plans(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """List recent learning plans"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/plans",
                params={"limit": limit, "offset": offset}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def delete_plan(self, request_id: str) -> Dict[str, Any]:
        """Delete a learning plan"""
        try:
            response = self.session.delete(f"{self.base_url}/api/v1/plan/{request_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def batch_generate(self, requests: list) -> Dict[str, Any]:
        """Generate multiple learning plans in batch"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/batch-generate",
                json=requests
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

def demo_single_plan_generation():
    """Demonstrate single learning plan generation"""
    print("🚀 Single Learning Plan Generation Demo")
    print("=" * 50)
    
    client = LearningPlanAPIClient()
    
    # Check API health
    print("🔍 Checking API health...")
    health = client.health_check()
    if "error" in health:
        print(f"❌ API health check failed: {health['error']}")
        print("Make sure the API server is running on http://localhost:8000")
        return
    
    print(f"✅ API is healthy: {health['status']}")
    
    # Generate a learning plan
    print("\n📚 Generating learning plan...")
    result = client.generate_plan(
        topic="Machine Learning",
        background="I have intermediate Python skills and basic understanding of statistics",
        preferred_format="video",
        user_id="user123",
        session_id="session456"
    )
    
    if "error" in result:
        print(f"❌ Failed to generate plan: {result['error']}")
        return
    
    if result.get("success"):
        print(f"✅ Plan generated successfully!")
        print(f"📋 Request ID: {result['data']['request_id']}")
        print(f"📚 Topic: {result['data']['topic']}")
        print(f"🎯 Format: {result['data']['preferred_format']}")
        print(f"📝 Main topics: {len(result['data']['main_topics'])}")
        
        # Store request ID for later retrieval
        request_id = result['data']['request_id']
        
        # Retrieve the plan
        print(f"\n🔍 Retrieving plan with ID: {request_id}")
        retrieved_plan = client.get_plan(request_id)
        
        if retrieved_plan.get("success"):
            print("✅ Plan retrieved successfully!")
            print(f"📅 Generated at: {retrieved_plan['data']['timestamp']}")
        else:
            print(f"❌ Failed to retrieve plan: {retrieved_plan.get('error', 'Unknown error')}")
    else:
        print(f"❌ Plan generation failed: {result.get('message', 'Unknown error')}")

def demo_batch_generation():
    """Demonstrate batch learning plan generation"""
    print("\n🚀 Batch Learning Plan Generation Demo")
    print("=" * 50)
    
    client = LearningPlanAPIClient()
    
    # Prepare batch requests
    batch_requests = [
        {
            "topic": "Python Programming",
            "background": "Complete beginner with no programming experience",
            "preferred_format": "video"
        },
        {
            "topic": "Web Development",
            "background": "I know HTML and CSS basics, want to learn JavaScript",
            "preferred_format": "text"
        },
        {
            "topic": "Data Science",
            "background": "I have Python skills and want to learn data analysis",
            "preferred_format": "audio"
        }
    ]
    
    print(f"📚 Generating {len(batch_requests)} learning plans in batch...")
    result = client.batch_generate(batch_requests)
    
    if "error" in result:
        print(f"❌ Batch generation failed: {result['error']}")
        return
    
    if result.get("success"):
        print(f"✅ Batch generation completed!")
        print(f"📊 Results: {result['message']}")
        
        for plan_result in result['results']:
            if plan_result['success']:
                print(f"✅ {plan_result['topic']}: Generated successfully")
            else:
                print(f"❌ {plan_result['topic']}: {plan_result.get('error', 'Unknown error')}")
    else:
        print(f"❌ Batch generation failed: {result.get('message', 'Unknown error')}")

def demo_api_endpoints():
    """Demonstrate various API endpoints"""
    print("\n🚀 API Endpoints Demo")
    print("=" * 50)
    
    client = LearningPlanAPIClient()
    
    # List recent plans
    print("📋 Listing recent learning plans...")
    plans = client.list_plans(limit=5)
    
    if "error" in plans:
        print(f"❌ Failed to list plans: {plans['error']}")
    else:
        print(f"✅ Found {plans['data']['total']} total plans")
        print(f"📊 Showing {len(plans['data']['plans'])} recent plans")
        
        for plan_id, plan_data in plans['data']['plans']:
            print(f"   📚 {plan_data['user_input']['topic']} ({plan_data['timestamp'][:19]})")

def main():
    """Main demo function"""
    print("🎓 Learning Plan Generator - Frontend Client Demo")
    print("=" * 60)
    print("This demo shows how frontend applications can call the backend API")
    print("Make sure the API server is running: python api_server.py")
    print()
    
    try:
        # Run demos
        demo_single_plan_generation()
        demo_batch_generation()
        demo_api_endpoints()
        
        print("\n🎉 Demo completed successfully!")
        print("\n💡 Frontend Integration Tips:")
        print("   • Use the client class for easy API calls")
        print("   • Handle errors gracefully")
        print("   • Store request IDs for plan retrieval")
        print("   • Implement loading states during generation")
        print("   • Add retry logic for failed requests")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")

if __name__ == "__main__":
    main() 