from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from enum import Enum

class LearningFormat(str, Enum):
    VIDEO = "video"
    TEXT = "text"
    AUDIO = "audio"

class UserInput(BaseModel):
    topic: str = Field(..., description="The topic the user wants to learn")
    background: str = Field(..., description="User's current background and knowledge level")
    preferred_format: LearningFormat = Field(..., description="Preferred learning format")
    max_iterations: Optional[int] = Field(default=5, description="Maximum number of iterations")

class KnowledgeGap(BaseModel):
    identified_gaps: List[str] = Field(..., description="List of knowledge gaps identified")
    current_level: str = Field(..., description="Current knowledge level assessment")
    target_level: str = Field(..., description="Target knowledge level for the topic")
    gap_analysis: str = Field(..., description="Detailed analysis of the knowledge gap")

class TopicPlan(BaseModel):
    main_topics: List[str] = Field(..., description="Main topics to cover")
    subtopics: List[str] = Field(..., description="Subtopics for each main topic")
    learning_objectives: List[str] = Field(..., description="Learning objectives")
    estimated_duration: str = Field(..., description="Estimated time to complete")

class TopicDetail(BaseModel):
    topic_name: str = Field(..., description="Name of the topic")
    description: str = Field(..., description="Detailed description")
    resources: List[str] = Field(..., description="Recommended resources")
    exercises: List[str] = Field(..., description="Practice exercises")
    assessment_criteria: str = Field(..., description="How to assess understanding")

class CompleteLearningPlan(BaseModel):
    user_input: UserInput
    knowledge_gap: KnowledgeGap
    topic_plan: TopicPlan
    topic_details: List[TopicDetail]
    learning_path: str = Field(..., description="Step-by-step learning path")
    recommended_resources: List[str] = Field(..., description="Overall recommended resources")
    timeline: str = Field(..., description="Suggested timeline for completion")
    success_metrics: List[str] = Field(..., description="Metrics to measure progress")

class AgentState(BaseModel):
    user_input: UserInput
    knowledge_gap: Optional[KnowledgeGap] = None
    topic_plan: Optional[TopicPlan] = None
    topic_details: Optional[List[TopicDetail]] = None
    complete_plan: Optional[CompleteLearningPlan] = None
    current_step: str = "gap_analysis"
    iteration_count: int = 0
    max_iterations: int = 5 