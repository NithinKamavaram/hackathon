# CodeCollab - AI-First Development Platform

## Hack Midwest 2024 Project

CodeCollab is an AI-first development platform that autonomously builds features and fixes bugs using multiple specialized AI agents, escalating to human developers only for complex decisions.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials:
# - AWS credentials for Bedrock access
# - Brale API credentials for payments
```

### 3. Run the Agent System

```bash
# Run the main agent orchestrator
python -m agents.main

# Or run tests
pytest tests/
```

## 📁 Project Structure

```
hackathon/
├── agents/              # AI agents implementation
│   ├── tools/          # Custom tools for agents
│   ├── base_agent.py   # Base agent configuration
│   ├── requirements_agent.py
│   ├── context_agent.py
│   ├── builder_agent.py
│   ├── quality_agent.py
│   ├── escalation_agent.py
│   └── orchestrator.py # Agent coordinator
├── payments/           # Brale payment integration
├── api/               # FastAPI backend
├── scripts/           # Utility scripts
├── tests/            # Test files
└── logs/             # Application logs
```

## 🤖 The 5 Specialized Agents

1. **RequirementsAgent** - Analyzes tasks and extracts structured requirements
2. **ContextAgent** - Understands codebase structure and provides relevant context
3. **BuilderAgent** - Writes production-quality code with tests
4. **QualityAgent** - Validates code quality, runs tests, ensures requirements met
5. **EscalationAgent** - Determines when human expertise is needed

## 🔧 Agent Workflow

```
Task Request → RequirementsAgent → ContextAgent → BuilderAgent → QualityAgent → EscalationAgent
                     ↓                   ↓             ↓              ↓              ↓
               Requirements        Context      Implementation    Verification   Decision
                                                                                   ↓
                                                                         AI Complete OR Human Expert
```

## 💰 Payment System

- **AI Tasks**: $0.01-$0.10 (micropayments via Brale)
- **Human Tasks**: $10-$250 (escrowed payments)

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents

# Run specific test file
pytest tests/test_agents.py
```

## 📝 Example Usage

```python
from agents import CodeCollabOrchestrator

# Initialize orchestrator
orchestrator = CodeCollabOrchestrator()

# Process a development task
task = "Fix authentication bug with special characters in passwords"
result = orchestrator.process_task(task)

print(f"Success: {result['success']}")
print(f"Result: {result['result']}")
```

## 🔐 Environment Variables

Required environment variables (see .env.example):
- AWS credentials for Bedrock
- Brale API credentials
- Application settings

## 📚 Documentation

See the following reports for detailed information:
- `project_architecture_and_overview.md` - Full project architecture
- `setup_installation.md` - Detailed setup instructions
- `agent_implementation.md` - Agent implementation details

## 🏆 Hack Midwest 2024

This project was built for Hack Midwest 2024, combining:
- **Strands Agents SDK** for multi-agent orchestration
- **Brale Stablecoin API** for instant micropayments and escrow

## 📄 License

MIT License - See LICENSE file for details