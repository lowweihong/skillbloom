# 🎓 Learning Plan Generator

A sophisticated AI-powered learning plan generator built with **LangChain AI 2** and **LangGraph**, featuring three specialized agents that work together to create personalized learning plans.

## ✨ Features

- **🤖 Three AI Agents**: Each specializing in different aspects of learning plan creation
- **⚡ Single Iteration Workflow**: Efficient single-pass learning plan creation
- **🎯 Personalized Plans**: Tailored to user background, topic, and learning preferences
- **📚 Multiple Formats**: Support for Video, Text, and Audio learning preferences
- **🔍 Gap Analysis**: Intelligent identification of knowledge gaps
- **📝 Detailed Breakdowns**: Comprehensive topic details with resources and exercises
- **⏱️ Timeline Planning**: Estimated duration and success metrics
- **💾 Export Options**: Save plans as JSON files for future reference

## 🏗️ Architecture

The system consists of three specialized agents working in sequence:

### 1. 🔍 Gap Analysis Agent
- Analyzes user's current background
- Identifies knowledge gaps between current level and target topic
- Provides detailed gap analysis and level assessment

### 2. 📚 Topic Planning Agent
- Creates comprehensive topic structure based on identified gaps
- Defines main topics, subtopics, and learning objectives
- Estimates completion duration

### 3. 📝 Topic Detail Agent
- Provides detailed breakdown of each topic
- Recommends specific resources and exercises
- Defines assessment criteria for each topic

### 4. 🔗 Plan Combiner Agent
- Combines all components into a cohesive learning plan
- Creates step-by-step learning path
- Provides overall timeline and success metrics

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd learning-plan-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GOOGLE_API_KEY=your_actual_api_key_here" > .env
   ```

### Usage

#### Interactive Mode
```bash
python main.py
```

#### Programmatic Usage
```python
from models import UserInput, LearningFormat
from workflow import LearningPlanWorkflow

# Create user input
user_input = UserInput(
    topic="Python Programming",
    background="Complete beginner with no programming experience",
    preferred_format=LearningFormat.VIDEO,
    max_iterations=1
)

# Generate learning plan
workflow = LearningPlanWorkflow()
learning_plan = workflow.create_learning_plan(user_input)

# Access plan components
print(f"Main topics: {learning_plan.topic_plan.main_topics}")
print(f"Duration: {learning_plan.topic_plan.estimated_duration}")
```

#### Example Usage
```bash
python example_usage.py
```

## 📁 Project Structure

```
learning-plan-generator/
├── models.py              # Pydantic data models
├── agents.py              # Three specialized AI agents
├── workflow.py            # LangGraph workflow orchestration
├── main.py               # Interactive CLI application
├── example_usage.py      # Programmatic usage examples
├── config.py             # Configuration and environment variables
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Your Gemini API key | Required |

### Model Configuration

- **Model**: `gemini-1.5-pro`
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Max Tokens**: 4000

## 📊 Output Structure

The system generates a complete learning plan with:

```json
{
  "user_input": {
    "topic": "Python Programming",
    "background": "Complete beginner...",
    "preferred_format": "video",
    "max_iterations": 3
  },
  "knowledge_gap": {
    "identified_gaps": ["Basic programming concepts", "Python syntax"],
    "current_level": "Complete beginner",
    "target_level": "Intermediate Python developer",
    "gap_analysis": "Detailed analysis..."
  },
  "topic_plan": {
    "main_topics": ["Introduction", "Core Concepts", "Advanced Topics"],
    "subtopics": ["Basics", "Fundamentals", "Applications"],
    "learning_objectives": ["Understand basics", "Master fundamentals"],
    "estimated_duration": "4-6 weeks"
  },
  "topic_details": [
    {
      "topic_name": "Introduction to Python",
      "description": "Comprehensive coverage...",
      "resources": ["Online course", "Practice exercises"],
      "exercises": ["Multiple choice", "Practical projects"],
      "assessment_criteria": "Demonstrate understanding..."
    }
  ],
  "learning_path": "Step-by-step progression...",
  "recommended_resources": ["Overall resources..."],
  "timeline": "Suggested timeline...",
  "success_metrics": ["Complete exercises", "Pass assessments"]
}
```

## 🎯 Use Cases

- **🎓 Students**: Create structured learning paths for academic subjects
- **💼 Professionals**: Develop skill upgrade plans for career advancement
- **🌍 Language Learners**: Design comprehensive language learning programs
- **💻 Developers**: Plan technology learning journeys
- **🎨 Creative Professionals**: Structure artistic skill development

## ⚡ Workflow Efficiency

The system uses a streamlined single-iteration workflow:

- **Single Pass**: All three agents execute once in sequence
- **Fast Execution**: Quick learning plan generation
- **Cost Effective**: Minimal API calls for maximum results
- **Consistent Quality**: Reliable output every time

## 🛠️ Customization

### Adding New Learning Formats

```python
# In models.py
class LearningFormat(str, Enum):
    VIDEO = "video"
    TEXT = "text"
    AUDIO = "audio"
    INTERACTIVE = "interactive"  # Add new format
```

### Modifying Agent Prompts

```python
# In agents.py
class GapAnalysisAgent:
    def __init__(self):
        self.prompt = ChatPromptTemplate.from_template("""
        Your custom prompt here...
        """)
```

### Extending Workflow

```python
# In workflow.py
def _custom_node(self, state: AgentState) -> AgentState:
    # Custom logic here
    return state

# Add to workflow
workflow.add_node("custom_node", self._custom_node)
```

## 🚨 Error Handling

The system includes comprehensive error handling:

- **API Failures**: Graceful fallbacks with default responses
- **Invalid Input**: Input validation and user-friendly error messages
- **Workflow Errors**: State preservation and recovery mechanisms

## 📈 Performance Considerations

- **API Rate Limits**: Respects Gemini API rate limits
- **Memory Management**: Efficient state management with LangGraph checkpoints
- **Parallel Processing**: Future enhancement for concurrent agent execution

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain Team**: For the excellent AI framework
- **LangGraph Team**: For the powerful workflow orchestration
- **Google AI**: For the Gemini API
- **Open Source Community**: For inspiration and contributions

## 📞 Support

For questions, issues, or contributions:

- Create an issue in the repository
- Check the documentation
- Review the example usage files

---

**Happy Learning! 🎉** 