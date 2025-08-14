from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from typing import Dict, Any
import json

from models import (
    KnowledgeGap, TopicPlan, TopicDetail, 
    UserInput, AgentState
)
from config import GOOGLE_API_KEY, MODEL_NAME, TEMPERATURE

# Initialize Gemini model (only if API key is available)
llm = None
if GOOGLE_API_KEY:
    try:
        llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            google_api_key=GOOGLE_API_KEY,
            temperature=TEMPERATURE,
            convert_system_message_to_human=True
        )
    except Exception as e:
        print(f"Warning: Could not initialize Gemini model: {e}")
        llm = None

class GapAnalysisAgent:
    """First agent: Identifies knowledge gaps between user background and target topic"""
    
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert educational consultant specializing in gap analysis.
        
        Analyze the user's current background and the topic they want to learn to identify knowledge gaps.
        
        User Input:
        - Topic to learn: {topic}
        - Current background: {background}
        - Preferred learning format: {preferred_format}
        
        Please provide a comprehensive gap analysis in the following JSON format:
        {{
            "identified_gaps": ["gap1", "gap2", "gap3"],
            "current_level": "detailed assessment of current knowledge level",
            "target_level": "what knowledge level they need to achieve",
            "gap_analysis": "detailed explanation of the knowledge gaps and why they exist"
        }}
        
        Be specific and actionable. Consider the learning format preference when analyzing gaps.
        """)
        
        # Create chain only if LLM is available
        if llm:
            self.chain = self.prompt | llm | JsonOutputParser()
        else:
            self.chain = None
    
    def analyze_gaps(self, user_input: UserInput) -> KnowledgeGap:
        """Analyze knowledge gaps between user background and target topic"""
        if not llm:
            # Return a default gap analysis when LLM is not available
            return KnowledgeGap(
                identified_gaps=["Basic understanding needed"],
                current_level="Beginner",
                target_level="Intermediate",
                gap_analysis="General knowledge gap identified (LLM not available)"
            )
        
        try:
            result = self.chain.invoke({
                "topic": user_input.topic,
                "background": user_input.background,
                "preferred_format": user_input.preferred_format.value
            })
            
            return KnowledgeGap(**result)
        except Exception as e:
            print(f"Error in gap analysis: {e}")
            # Return a default gap analysis
            return KnowledgeGap(
                identified_gaps=["Basic understanding needed"],
                current_level="Beginner",
                target_level="Intermediate",
                gap_analysis="General knowledge gap identified"
            )

class TopicPlanningAgent:
    """Second agent: Creates a comprehensive topic plan based on identified gaps"""
    
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert curriculum designer specializing in creating learning plans.
        
        Based on the identified knowledge gaps, create a comprehensive topic plan.
        
        Context:
        - Topic: {topic}
        - Knowledge gaps: {gaps}
        - Current level: {current_level}
        - Target level: {target_level}
        - Preferred format: {preferred_format}
        
        Create a structured learning plan in this JSON format:
        {{
            "main_topics": ["topic1", "topic2", "topic3"],
            "subtopics": ["subtopic1", "subtopic2", "subtopic3"],
            "learning_objectives": ["objective1", "objective2", "objective3"],
            "estimated_duration": "estimated time to complete"
        }}
        
        Ensure the plan addresses all identified gaps and is appropriate for the user's level.
        Consider the preferred learning format when structuring the plan.
        """)
        
        # Create chain only if LLM is available
        if llm:
            self.chain = self.prompt | llm | JsonOutputParser()
        else:
            self.chain = None
    
    def create_plan(self, user_input: UserInput, knowledge_gap: KnowledgeGap) -> TopicPlan:
        """Create a comprehensive topic plan"""
        if not llm:
            # Return a default topic plan when LLM is not available
            return TopicPlan(
                main_topics=["Introduction", "Core Concepts", "Advanced Topics"],
                subtopics=["Basics", "Fundamentals", "Applications"],
                learning_objectives=["Understand basics", "Master fundamentals", "Apply knowledge"],
                estimated_duration="4-6 weeks (LLM not available)"
            )
        
        try:
            result = self.chain.invoke({
                "topic": user_input.topic,
                "gaps": knowledge_gap.identified_gaps,
                "current_level": knowledge_gap.current_level,
                "target_level": knowledge_gap.target_level,
                "preferred_format": user_input.preferred_format.value
            })
            
            return TopicPlan(**result)
        except Exception as e:
            print(f"Error in topic planning: {e}")
            # Return a default topic plan
            return TopicPlan(
                main_topics=["Introduction", "Core Concepts", "Advanced Topics"],
                subtopics=["Basics", "Fundamentals", "Applications"],
                learning_objectives=["Understand basics", "Master fundamentals", "Apply knowledge"],
                estimated_duration="4-6 weeks"
            )

class TopicDetailAgent:
    """Third agent: Provides detailed breakdown of each topic with resources and exercises"""
    
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert learning content specialist who creates detailed topic breakdowns.
        
        Create detailed information for each topic in the learning plan.
        
        Context:
        - Topic name: {topic_name}
        - Main topic: {main_topic}
        - Learning objective: {objective}
        - Preferred format: {preferred_format}
        - User background: {background}
        
        Provide detailed breakdown in this JSON format:
        {{
            "topic_name": "exact topic name",
            "description": "comprehensive description of what this topic covers",
            "resources": ["resource1", "resource2", "resource3"],
            "exercises": ["exercise1", "exercise2", "exercise3"],
            "assessment_criteria": "how to assess understanding of this topic"
        }}
        
        Make resources and exercises specific to the preferred learning format.
        Ensure exercises are appropriate for the user's background level.
        """)
        
        # Create chain only if LLM is available
        if llm:
            self.chain = self.prompt | llm | JsonOutputParser()
        else:
            self.chain = None
    
    def create_topic_detail(self, topic_name: str, main_topic: str, objective: str, 
                           user_input: UserInput) -> TopicDetail:
        """Create detailed breakdown for a specific topic"""
        if not llm:
            # Return a default topic detail when LLM is not available
            return TopicDetail(
                topic_name=topic_name,
                description=f"Comprehensive coverage of {topic_name} (LLM not available)",
                resources=["Online course", "Practice exercises", "Reference materials"],
                exercises=["Multiple choice questions", "Practical projects", "Self-assessment"],
                assessment_criteria="Demonstrate understanding through practical application"
            )
        
        try:
            result = self.chain.invoke({
                "topic_name": topic_name,
                "main_topic": main_topic,
                "objective": objective,
                "preferred_format": user_input.preferred_format.value,
                "background": user_input.background
            })
            
            return TopicDetail(**result)
        except Exception as e:
            print(f"Error in topic detailing: {e}")
            # Return a default topic detail
            return TopicDetail(
                topic_name=topic_name,
                description=f"Comprehensive coverage of {topic_name}",
                resources=["Online course", "Practice exercises", "Reference materials"],
                exercises=["Multiple choice questions", "Practical projects", "Self-assessment"],
                assessment_criteria="Demonstrate understanding through practical application"
            )

class PlanCombinerAgent:
    """Agent to combine all components into a complete learning plan"""
    
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template("""
        You are an expert learning coordinator who combines all learning components into a cohesive plan.
        
        Combine the gap analysis, topic plan, and topic details into a complete learning plan.
        
        Context:
        - User input: {user_input}
        - Knowledge gaps: {gaps}
        - Topic plan: {plan}
        - Topic details: {details}
        
        Create a comprehensive learning plan in this JSON format:
        {{
            "learning_path": "step-by-step learning path with clear progression",
            "recommended_resources": ["overall resource1", "overall resource2"],
            "timeline": "suggested timeline for completion",
            "success_metrics": ["metric1", "metric2", "metric3"]
        }}
        
        Ensure the plan flows logically and addresses all identified gaps.
        Make it actionable and measurable for the user.
        """)
        
        # Create chain only if LLM is available
        if llm:
            self.chain = self.prompt | llm | JsonOutputParser()
        else:
            self.chain = None
    
    def combine_plan(self, user_input: UserInput, knowledge_gap: KnowledgeGap, 
                    topic_plan: TopicPlan, topic_details: list[TopicDetail]) -> Dict[str, Any]:
        """Combine all components into a complete learning plan"""
        if not llm:
            # Return default combined plan when LLM is not available
            return {
                "learning_path": "Follow the structured topics in order, practice regularly, and assess progress (LLM not available)",
                "recommended_resources": ["Online courses", "Practice platforms", "Community forums"],
                "timeline": "4-6 weeks with 2-3 hours per week",
                "success_metrics": ["Complete all exercises", "Pass assessments", "Apply knowledge practically"]
            }
        
        try:
            result = self.chain.invoke({
                "user_input": user_input.model_dump(),
                "gaps": knowledge_gap.model_dump(),
                "plan": topic_plan.model_dump(),
                "details": [detail.model_dump() for detail in topic_details]
            })
            
            return result
        except Exception as e:
            print(f"Error in plan combination: {e}")
            # Return default combined plan
            return {
                "learning_path": "Follow the structured topics in order, practice regularly, and assess progress",
                "recommended_resources": ["Online courses", "Practice platforms", "Community forums"],
                "timeline": "4-6 weeks with 2-3 hours per week",
                "success_metrics": ["Complete all exercises", "Pass assessments", "Apply knowledge practically"]
            } 