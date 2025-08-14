#!/usr/bin/env python3
"""
Simple test file to verify system components work correctly
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported correctly"""
    print("🧪 Testing module imports...")
    
    try:
        from models import UserInput, LearningFormat, KnowledgeGap, TopicPlan, TopicDetail
        print("✅ Models imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import models: {e}")
        return False
    
    try:
        from config import GOOGLE_API_KEY, MODEL_NAME
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import config: {e}")
        return False
    
    try:
        from agents import GapAnalysisAgent, TopicPlanningAgent, TopicDetailAgent, PlanCombinerAgent
        print("✅ Agents imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import agents: {e}")
        return False
    
    try:
        from workflow import LearningPlanWorkflow
        print("✅ Workflow imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import workflow: {e}")
        return False
    
    return True

def test_models():
    """Test that data models work correctly"""
    print("\n🧪 Testing data models...")
    
    try:
        from models import UserInput, LearningFormat, KnowledgeGap, TopicPlan, TopicDetail
        
        # Test UserInput creation
        user_input = UserInput(
            topic="Test Topic",
            background="Test background",
            preferred_format=LearningFormat.VIDEO,
            max_iterations=3
        )
        print("✅ UserInput model works correctly")
        
        # Test KnowledgeGap creation
        knowledge_gap = KnowledgeGap(
            identified_gaps=["Test gap 1", "Test gap 2"],
            current_level="Beginner",
            target_level="Intermediate",
            gap_analysis="Test analysis"
        )
        print("✅ KnowledgeGap model works correctly")
        
        # Test TopicPlan creation
        topic_plan = TopicPlan(
            main_topics=["Topic 1", "Topic 2"],
            subtopics=["Subtopic 1", "Subtopic 2"],
            learning_objectives=["Objective 1", "Objective 2"],
            estimated_duration="2 weeks"
        )
        print("✅ TopicPlan model works correctly")
        
        # Test TopicDetail creation
        topic_detail = TopicDetail(
            topic_name="Test Topic",
            description="Test description",
            resources=["Resource 1", "Resource 2"],
            exercises=["Exercise 1", "Exercise 2"],
            assessment_criteria="Test assessment"
        )
        print("✅ TopicDetail model works correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_agent_initialization():
    """Test that agents can be initialized (without API calls)"""
    print("\n🧪 Testing agent initialization...")
    
    try:
        from agents import GapAnalysisAgent, TopicPlanningAgent, TopicDetailAgent, PlanCombinerAgent
        
        # Test agent initialization
        gap_agent = GapAnalysisAgent()
        print("✅ GapAnalysisAgent initialized")
        
        planning_agent = TopicPlanningAgent()
        print("✅ TopicPlanningAgent initialized")
        
        detail_agent = TopicDetailAgent()
        print("✅ TopicDetailAgent initialized")
        
        combiner_agent = PlanCombinerAgent()
        print("✅ PlanCombinerAgent initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization test failed: {e}")
        return False

def test_workflow_creation():
    """Test that workflow can be created (without execution)"""
    print("\n🧪 Testing workflow creation...")
    
    try:
        from workflow import LearningPlanWorkflow
        
        # Test workflow creation
        workflow = LearningPlanWorkflow()
        print("✅ LearningPlanWorkflow created successfully")
        
        # Test workflow properties
        print(f"   Workflow object type: {type(workflow.workflow)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow creation test failed: {e}")
        return False

def test_configuration():
    """Test configuration values"""
    print("\n🧪 Testing configuration...")
    
    try:
        from config import GOOGLE_API_KEY, MODEL_NAME, TEMPERATURE
        
        print(f"✅ Configuration loaded:")
        print(f"   Model: {MODEL_NAME}")
        print(f"   Temperature: {TEMPERATURE}")
        print(f"   Workflow: Single iteration")
        print(f"   API key set: {'Yes' if GOOGLE_API_KEY else 'No'}")
        
        if not GOOGLE_API_KEY:
            print("⚠️  Warning: GOOGLE_API_KEY not set")
            print("   This is expected for testing without API access")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Learning Plan Generator - System Test")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Data Models", test_models),
        ("Agent Initialization", test_agent_initialization),
        ("Workflow Creation", test_workflow_creation),
        ("Configuration", test_configuration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Set your GOOGLE_API_KEY in a .env file")
        print("2. Run: python main.py")
        print("3. Or run: python example_usage.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 