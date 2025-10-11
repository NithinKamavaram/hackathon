# CodeCollab Configuration Guide

## Using Real Implementation Instead of Mock Data

Currently, the system is using mock implementations for testing. To use real AI agents with AWS Bedrock, follow these steps:

### 1. Environment Setup

First, create your environment file:
```bash
cp .env.example .env
```

Then edit `.env` with your real credentials:

```bash
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=your_actual_aws_key
AWS_SECRET_ACCESS_KEY=your_actual_aws_secret
AWS_DEFAULT_REGION=us-west-2
BEDROCK_MODEL_ID=anthropic.claude-sonnet-4-20250514-v1:0

# Enable real mode
USE_REAL_AGENTS=true
```

### 2. Install Real Strands SDK

The Strands SDK needs to be installed from source since it's not available on PyPI:

```bash
# Option 1: Install from GitHub (if available)
pip install git+https://github.com/strands-ai/strands-sdk.git

# Option 2: Install from local source
# Contact Strands team for SDK access
```

### 3. Switch Implementation

To switch between mock and real implementations, update the imports in the orchestrator files:

**Current (Mock):**
```python
# In agents/swarm_orchestrator.py
from strands.multiagent import Swarm  # This uses mock
```

**Real Implementation:**
```python
# Install real strands SDK first
from strands_agents import Swarm, Agent
from strands_agents.models import BedrockModel
```

### 4. AWS Bedrock Access

Ensure you have:
- AWS account with Bedrock access enabled
- Claude Sonnet model access approved
- Proper IAM permissions for Bedrock

### 5. Testing Real vs Mock

You can create a flag-based system:

```python
import os

USE_REAL_AGENTS = os.getenv('USE_REAL_AGENTS', 'false').lower() == 'true'

if USE_REAL_AGENTS:
    from strands_agents import Agent, Swarm
    print("Using real Strands agents with AWS Bedrock")
else:
    from strands.multiagent import Swarm  # Mock implementation
    print("Using mock agents for testing")
```

### 6. Current Status

- ✅ Mock implementation working perfectly
- ✅ Task-specific code generation working
- ✅ All 5 agents collaborating properly  
- ⚠️ Real Strands SDK not available in public PyPI
- ⚠️ AWS credentials need to be configured

### 7. Next Steps for Real Implementation

1. **Contact Strands Team**: Get access to the real SDK
2. **AWS Setup**: Configure Bedrock access and credentials
3. **Update Imports**: Switch from mock to real implementations
4. **Test Incrementally**: Start with one agent, then expand

The architecture is solid - we just need the real SDK and AWS access to make it production-ready!