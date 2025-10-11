# CodeCollab: Agent Implementation Code Report

## Complete Strands Agents Implementation for Hack Midwest 2024

---

## 📋 Overview

This report contains all the code needed to implement the 5 specialized AI agents using Strands Agents SDK. Each agent has a specific role in the autonomous development pipeline.

**Agent Roles:**
1. **RequirementsAgent** - Analyzes tasks and extracts structured requirements
2. **ContextAgent** - Understands codebase structure and provides relevant context
3. **BuilderAgent** - Writes production-quality code with tests
4. **QualityAgent** - Validates code quality, runs tests, ensures requirements met
5. **EscalationAgent** - Determines when human expertise is needed

---

## 🏗️ Project Structure

```
agents/
├── __init__.py
├── base_agent.py              # Base agent configuration
├── requirements_agent.py      # Requirements analysis
├── context_agent.py          # Codebase knowledge
├── builder_agent.py          # Code generation
├── quality_agent.py          # Quality assurance
├── escalation_agent.py       # Escalation decisions
├── orchestrator.py           # Multi-agent orchestration
└── tools/
    ├── __init__.py
    ├── code_tools.py         # Code analysis tools
    ├── test_tools.py         # Testing tools
    └── complexity_tools.py   # Complexity analysis
```

---

## 1️⃣ Base Configuration

### `agents/__init__.py`

```python
"""
CodeCollab Agents Package
Strands-based multi-agent system for autonomous development
"""

from .requirements_agent import RequirementsAgent
from .context_agent import ContextAgent
from .builder_agent import BuilderAgent
from .quality_agent import QualityAgent
from .escalation_agent import EscalationAgent
from .orchestrator import CodeCollabOrchestrator

__all__ = [
    'RequirementsAgent',
    'ContextAgent',
    'BuilderAgent',
    'QualityAgent',
    'EscalationAgent',
    'CodeCollabOrchestrator'
]

__version__ = '1.0.0'
```

### `agents/base_agent.py`

```python
"""
Base agent configuration and utilities
"""

from strands import Agent
from strands.models import BedrockModel
import os
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class BaseAgentConfig:
    """Base configuration for all CodeCollab agents"""
    
    # Model configuration
    MODEL_ID = "anthropic.claude-sonnet-4-20250514-v1:0"
    REGION = "us-west-2"
    TEMPERATURE = 0.3
    MAX_TOKENS = 4096
    STREAMING = True
    
    # Agent behavior
    TIMEOUT_SECONDS = 300
    MAX_RETRIES = 3
    
    @staticmethod
    def create_model() -> BedrockModel:
        """Create configured Bedrock model"""
        return BedrockModel(
            model_id=BaseAgentConfig.MODEL_ID,
            region_name=BaseAgentConfig.REGION,
            temperature=BaseAgentConfig.TEMPERATURE,
            max_tokens=BaseAgentConfig.MAX_TOKENS,
            streaming=BaseAgentConfig.STREAMING
        )


class BaseCodeCollabAgent:
    """Base class for all CodeCollab agents"""
    
    def __init__(self, name: str, system_prompt: str, tools: list = None):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            system_prompt: System prompt defining agent behavior
            tools: List of tools available to agent
        """
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools or []
        
        # Create underlying Strands agent
        self.agent = Agent(
            name=name,
            model=BaseAgentConfig.create_model(),
            system_prompt=system_prompt,
            tools=self.tools
        )
        
        logger.info(f"Initialized {name} with {len(self.tools)} tools")
    
    def __call__(self, prompt: str) -> Dict[str, Any]:
        """
        Execute agent with given prompt
        
        Args:
            prompt: User input/task description
            
        Returns:
            Dict containing:
                - message: Agent response
                - tokens: Token usage
                - latency_ms: Response time
                - success: Boolean success indicator
        """
        try:
            result = self.agent(prompt)
            
            return {
                "message": result.message,
                "tokens": result.metrics.total_tokens,
                "latency_ms": result.metrics.total_latency_ms,
                "success": True,
                "agent_name": self.name
            }
        except Exception as e:
            logger.error(f"{self.name} execution failed: {e}")
            return {
                "message": f"Error in {self.name}: {str(e)}",
                "tokens": 0,
                "latency_ms": 0,
                "success": False,
                "agent_name": self.name,
                "error": str(e)
            }
    
    async def stream_async(self, prompt: str):
        """
        Stream agent response asynchronously
        
        Args:
            prompt: User input
            
        Yields:
            Stream events from agent execution
        """
        async for event in self.agent.stream_async(prompt):
            yield event
```

---

## 2️⃣ Custom Tools

### `agents/tools/__init__.py`

```python
"""
Custom tools for CodeCollab agents
"""

from .code_tools import (
    analyze_code_complexity,
    find_code_patterns,
    detect_security_issues
)
from .test_tools import (
    run_tests,
    calculate_coverage,
    lint_code
)
from .complexity_tools import (
    analyze_task_complexity,
    estimate_effort
)

__all__ = [
    'analyze_code_complexity',
    'find_code_patterns',
    'detect_security_issues',
    'run_tests',
    'calculate_coverage',
    'lint_code',
    'analyze_task_complexity',
    'estimate_effort'
]
```

### `agents/tools/code_tools.py`

```python
"""
Code analysis tools for agents
"""

from strands import tool
from typing import Dict, List, Any
import re


@tool
def analyze_code_complexity(code: str, language: str = "python") -> Dict[str, Any]:
    """
    Analyze code complexity and quality metrics.
    
    Args:
        code: Source code to analyze
        language: Programming language
        
    Returns:
        Dict containing complexity metrics and recommendations
    """
    # Count lines of code
    lines = code.split('\n')
    loc = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
    
    # Count functions/methods
    if language == "python":
        functions = len(re.findall(r'def\s+\w+', code))
        classes = len(re.findall(r'class\s+\w+', code))
    else:
        functions = 0
        classes = 0
    
    # Basic complexity scoring
    complexity_score = min(100, max(0, 100 - (loc / 10)))
    
    # Determine complexity level
    if loc < 50:
        complexity = "simple"
    elif loc < 200:
        complexity = "medium"
    else:
        complexity = "complex"
    
    return {
        "lines_of_code": loc,
        "functions": functions,
        "classes": classes,
        "complexity": complexity,
        "complexity_score": complexity_score,
        "language": language,
        "recommendations": [
            "Consider breaking down large functions" if loc > 200 else "Code size is manageable",
            "Add docstrings to all functions",
            "Ensure proper error handling"
        ]
    }


@tool
def find_code_patterns(code: str, language: str = "python") -> Dict[str, List[str]]:
    """
    Find common code patterns and anti-patterns.
    
    Args:
        code: Source code to analyze
        language: Programming language
        
    Returns:
        Dict of patterns found
    """
    patterns = {
        "imports": [],
        "error_handling": [],
        "testing_patterns": [],
        "anti_patterns": []
    }
    
    lines = code.split('\n')
    
    # Find imports
    for line in lines:
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            patterns["imports"].append(line.strip())
    
    # Find error handling
    if 'try:' in code and 'except' in code:
        patterns["error_handling"].append("try-except blocks found")
    
    # Find testing patterns
    if 'def test_' in code or 'class Test' in code:
        patterns["testing_patterns"].append("Unit tests present")
    
    # Check for anti-patterns
    if 'except:' in code and 'except Exception:' not in code:
        patterns["anti_patterns"].append("Bare except clause (catch-all exception)")
    
    if code.count('print(') > 5:
        patterns["anti_patterns"].append("Excessive print statements (use logging)")
    
    return patterns


@tool
def detect_security_issues(code: str) -> Dict[str, List[str]]:
    """
    Detect potential security vulnerabilities in code.
    
    Args:
        code: Source code to analyze
        
    Returns:
        Dict of security issues found
    """
    issues = {
        "high": [],
        "medium": [],
        "low": [],
        "info": []
    }
    
    # Check for common security issues
    if 'eval(' in code:
        issues["high"].append("Use of eval() - potential code injection risk")
    
    if 'exec(' in code:
        issues["high"].append("Use of exec() - potential code injection risk")
    
    if 'pickle.loads' in code:
        issues["medium"].append("Pickle deserialization - validate input source")
    
    if 'password' in code.lower() and ('=' in code or 'input(' in code):
        issues["medium"].append("Hardcoded credentials or password in plain text")
    
    if 'sql' in code.lower() and '+' in code:
        issues["medium"].append("Potential SQL injection via string concatenation")
    
    if 'os.system' in code:
        issues["medium"].append("Use of os.system() - validate all inputs")
    
    # Info level
    if not any(issues.values()):
        issues["info"].append("No obvious security issues detected")
    
    return issues
```

### `agents/tools/test_tools.py`

```python
"""
Testing and quality assurance tools
"""

from strands import tool
from typing import Dict, Any, List
import subprocess
import tempfile
import os


@tool
def run_tests(test_code: str, test_file_name: str = "test_temp.py") -> Dict[str, Any]:
    """
    Execute test code and return results.
    
    Args:
        test_code: Python test code to execute
        test_file_name: Name for temporary test file
        
    Returns:
        Test execution results
    """
    try:
        # Create temporary test file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False
        ) as f:
            f.write(test_code)
            temp_file = f.name
        
        # Run pytest on the file
        result = subprocess.run(
            ['pytest', temp_file, '-v', '--tb=short'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse output
        output = result.stdout + result.stderr
        passed = output.count(' PASSED')
        failed = output.count(' FAILED')
        
        # Cleanup
        os.unlink(temp_file)
        
        return {
            "success": result.returncode == 0,
            "passed": passed,
            "failed": failed,
            "output": output[:500],  # Truncate long output
            "return_code": result.returncode
        }
    
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "passed": 0,
            "failed": 0,
            "output": "Tests timed out after 30 seconds",
            "return_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "passed": 0,
            "failed": 0,
            "output": f"Error running tests: {str(e)}",
            "return_code": -1
        }


@tool
def calculate_coverage(source_code: str, test_code: str) -> Dict[str, Any]:
    """
    Calculate test coverage for code.
    
    Args:
        source_code: Source code to test
        test_code: Test code
        
    Returns:
        Coverage metrics
    """
    # Simplified coverage calculation
    # In production, would use coverage.py
    
    source_lines = [l for l in source_code.split('\n') if l.strip()]
    test_lines = [l for l in test_code.split('\n') if l.strip()]
    
    # Estimate coverage based on test/source ratio
    coverage_estimate = min(100, (len(test_lines) / max(len(source_lines), 1)) * 50)
    
    return {
        "coverage_percentage": round(coverage_estimate, 2),
        "source_lines": len(source_lines),
        "test_lines": len(test_lines),
        "estimated": True
    }


@tool
def lint_code(code: str, language: str = "python") -> Dict[str, List[str]]:
    """
    Run linting checks on code.
    
    Args:
        code: Source code to lint
        language: Programming language
        
    Returns:
        Linting issues found
    """
    issues = {
        "errors": [],
        "warnings": [],
        "style": []
    }
    
    lines = code.split('\n')
    
    # Basic style checks
    for i, line in enumerate(lines, 1):
        # Line length
        if len(line) > 100:
            issues["style"].append(f"Line {i}: Exceeds 100 characters")
        
        # Trailing whitespace
        if line.endswith(' ') or line.endswith('\t'):
            issues["style"].append(f"Line {i}: Trailing whitespace")
        
        # Multiple statements on one line
        if ';' in line and not line.strip().startswith('#'):
            issues["warnings"].append(f"Line {i}: Multiple statements on one line")
    
    # Check for missing docstrings
    if 'def ' in code and '"""' not in code and "'''" not in code:
        issues["warnings"].append("Functions missing docstrings")
    
    return issues
```

### `agents/tools/complexity_tools.py`

```python
"""
Task complexity analysis tools
"""

from strands import tool
from typing import Dict, Any, List


@tool
def analyze_task_complexity(description: str, requirements: Dict = None) -> Dict[str, Any]:
    """
    Analyze task complexity to determine effort and escalation needs.
    
    Args:
        description: Task description
        requirements: Structured requirements (if available)
        
    Returns:
        Complexity analysis with recommendations
    """
    # Word count analysis
    word_count = len(description.split())
    
    # Keyword analysis for complexity indicators
    complex_keywords = [
        'architecture', 'refactor', 'migration', 'scalability',
        'distributed', 'microservices', 'security', 'authentication',
        'authorization', 'performance', 'optimization', 'integration'
    ]
    
    simple_keywords = [
        'fix', 'bug', 'typo', 'update', 'change', 'add', 'remove',
        'button', 'text', 'color', 'style'
    ]
    
    description_lower = description.lower()
    
    complex_count = sum(1 for kw in complex_keywords if kw in description_lower)
    simple_count = sum(1 for kw in simple_keywords if kw in description_lower)
    
    # Determine complexity
    if word_count < 30 and simple_count > complex_count:
        complexity = "simple"
        estimated_time_minutes = 5
        ai_payment = "0.01"
        human_payment = "0"
        requires_human = False
    elif word_count < 100 and complex_count <= 2:
        complexity = "medium"
        estimated_time_minutes = 15
        ai_payment = "0.05"
        human_payment = "0"
        requires_human = False
    else:
        complexity = "complex"
        estimated_time_minutes = 60
        ai_payment = "0.10"
        human_payment = "250.00"
        requires_human = complex_count > 3
    
    return {
        "complexity": complexity,
        "word_count": word_count,
        "complex_indicators": complex_count,
        "simple_indicators": simple_count,
        "estimated_time_minutes": estimated_time_minutes,
        "estimated_ai_payment": ai_payment,
        "estimated_human_payment": human_payment,
        "requires_human": requires_human,
        "reasoning": f"Task has {word_count} words with {complex_count} complexity indicators"
    }


@tool
def estimate_effort(requirements: Dict, context: Dict = None) -> Dict[str, Any]:
    """
    Estimate effort required for implementation.
    
    Args:
        requirements: Structured requirements
        context: Codebase context
        
    Returns:
        Effort estimation
    """
    # Parse requirements
    num_features = requirements.get("feature_count", 1)
    num_tests = requirements.get("test_count", 3)
    has_integration = requirements.get("requires_integration", False)
    
    # Calculate effort points
    effort_points = num_features * 2 + num_tests * 1
    if has_integration:
        effort_points += 5
    
    # Map to time estimate
    if effort_points < 5:
        time_estimate = "15-30 minutes"
        complexity = "simple"
    elif effort_points < 15:
        time_estimate = "30-60 minutes"
        complexity = "medium"
    else:
        time_estimate = "1-3 hours"
        complexity = "complex"
    
    return {
        "effort_points": effort_points,
        "time_estimate": time_estimate,
        "complexity": complexity,
        "breakdown": {
            "features": num_features,
            "tests": num_tests,
            "integration": has_integration
        }
    }
```

---

## 3️⃣ Requirements Agent

### `agents/requirements_agent.py`

```python
"""
Requirements Agent - Analyzes tasks and extracts structured requirements
"""

from .base_agent import BaseCodeCollabAgent
from .tools.complexity_tools import analyze_task_complexity, estimate_effort
from typing import Dict, Any
import json


class RequirementsAgent(BaseCodeCollabAgent):
    """
    Agent responsible for analyzing feature requests and bug reports,
    extracting clear requirements with acceptance criteria.
    """
    
    SYSTEM_PROMPT = """You are a senior business analyst and requirements engineer for CodeCollab.

Your role is to analyze feature requests and bug reports, then extract clear, structured requirements.

For each task you receive:

1. **Extract Core Requirements**
   - What needs to be built or fixed?
   - What are the acceptance criteria?
   - What are the constraints?

2. **Identify Edge Cases**
   - What unusual scenarios should be handled?
   - What error conditions need handling?
   - What boundary conditions exist?

3. **Determine Technical Constraints**
   - What technologies are involved?
   - What performance requirements exist?
   - What security considerations apply?

4. **Assess Complexity**
   - Use analyze_task_complexity tool
   - Determine if task is simple/medium/complex
   - Identify if human expertise will be needed

5. **Output Structured Requirements**
   Return a JSON structure with:
   ```json
   {
     "task_id": "unique_id",
     "type": "bug_fix" or "feature",
     "summary": "Brief description",
     "requirements": [
       {
         "id": "REQ-1",
         "description": "Specific requirement",
         "priority": "high/medium/low",
         "acceptance_criteria": ["criterion 1", "criterion 2"]
       }
     ],
     "edge_cases": ["case 1", "case 2"],
     "constraints": ["constraint 1", "constraint 2"],
     "complexity": {
       "level": "simple/medium/complex",
       "estimated_time_minutes": 30,
       "requires_human": false,
       "estimated_ai_payment": "0.05",
       "estimated_human_payment": "0"
     }
   }
   ```

Be thorough but concise. Focus on clarity and testability."""
    
    def __init__(self):
        super().__init__(
            name="requirements_agent",
            system_prompt=self.SYSTEM_PROMPT,
            tools=[analyze_task_complexity, estimate_effort]
        )
    
    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """
        Analyze task and extract structured requirements.
        
        Args:
            task_description: Raw task description from user
            
        Returns:
            Structured requirements document
        """
        prompt = f"""Analyze this development task and provide structured requirements:

TASK:
{task_description}

Use the analyze_task_complexity tool to assess complexity, then provide complete structured requirements in JSON format."""
        
        result = self(prompt)
        
        if result["success"]:
            try:
                # Try to parse JSON from response
                message = result["message"]
                # Extract JSON from markdown code blocks if present
                if "```json" in message:
                    json_start = message.find("```json") + 7
                    json_end = message.find("```", json_start)
                    message = message[json_start:json_end].strip()
                elif "```" in message:
                    json_start = message.find("```") + 3
                    json_end = message.find("```", json_start)
                    message = message[json_start:json_end].strip()
                
                requirements = json.loads(message)
                return {
                    **result,
                    "requirements": requirements
                }
            except json.JSONDecodeError:
                # If JSON parsing fails, return raw message
                return result
        
        return result
```

---

## 4️⃣ Context Agent

### `agents/context_agent.py`

```python
"""
Context Agent - Provides codebase knowledge and context
"""

from .base_agent import BaseCodeCollabAgent
from strands_tools import file_manager
from typing import Dict, Any, List
import os


class ContextAgent(BaseCodeCollabAgent):
    """
    Agent responsible for understanding codebase structure,
    finding relevant code, and providing integration context.
    """
    
    SYSTEM_PROMPT = """You are a senior software architect and codebase expert for CodeCollab.

Your role is to understand the project structure and provide relevant context for implementation tasks.

For each task:

1. **Analyze Codebase Structure**
   - Identify relevant files and modules
   - Understand existing patterns and conventions
   - Map out dependencies

2. **Find Integration Points**
   - Where should new code be added?
   - What existing code needs modification?
   - What interfaces should be used?

3. **Identify Reusable Components**
   - What existing code can be reused?
   - What utilities are available?
   - What patterns should be followed?

4. **Assess Impact**
   - What components will be affected?
   - What tests need updating?
   - What documentation needs changes?

5. **Provide Context Document**
   Return a structured context report:
   ```json
   {
     "relevant_files": [
       {
         "path": "path/to/file.py",
         "purpose": "What this file does",
         "relevance": "Why it matters for this task"
       }
     ],
     "integration_points": [
       {
         "location": "specific location",
         "action": "what to do",
         "example": "code example if helpful"
       }
     ],
     "reusable_components": [
       {
         "name": "component name",
         "usage": "how to use it"
       }
     ],
     "patterns_to_follow": ["pattern 1", "pattern 2"],
     "affected_areas": ["area 1", "area 2"]
   }
   ```

Use file_manager tool to explore the codebase. Be specific and provide concrete examples."""
    
    def __init__(self):
        super().__init__(
            name="context_agent",
            system_prompt=self.SYSTEM_PROMPT,
            tools=[file_manager]
        )
    
    def gather_context(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gather relevant codebase context for implementation.
        
        Args:
            requirements: Structured requirements from RequirementsAgent
            
        Returns:
            Context document with relevant codebase information
        """
        task_summary = requirements.get("summary", "unknown task")
        task_type = requirements.get("type", "unknown")
        
        prompt = f"""Analyze the codebase and provide context for this task:

TASK TYPE: {task_type}
SUMMARY: {task_summary}
REQUIREMENTS: {requirements.get('requirements', [])}

Use the file_manager tool to explore relevant parts of the codebase.

Provide:
1. List of relevant files
2. Integration points
3. Reusable components
4. Patterns to follow
5. Affected areas

Return as structured JSON."""
        
        return self(prompt)
```

---

## 5️⃣ Builder Agent

### `agents/builder_agent.py`

```python
"""
Builder Agent - Writes production-quality code
"""

from .base_agent import BaseCodeCollabAgent
from strands_tools import python_repl, file_manager
from .tools.code_tools import analyze_code_complexity, find_code_patterns
from typing import Dict, Any


class BuilderAgent(BaseCodeCollabAgent):
    """
    Agent responsible for implementing features and fixing bugs
    with production-quality code.
    """
    
    SYSTEM_PROMPT = """You are a senior software engineer for CodeCollab specializing in writing production-quality code.

Your role is to implement features and fix bugs following best practices.

For each implementation task:

1. **Understand Requirements**
   - Review requirements document
   - Understand acceptance criteria
   - Consider edge cases

2. **Review Context**
   - Study relevant existing code
   - Follow project patterns
   - Use reusable components

3. **Write Quality Code**
   - Clear, readable code
   - Proper error handling
   - Comprehensive docstrings
   - Type hints where appropriate
   - Follow SOLID principles

4. **Include Tests**
   - Unit tests for all functions
   - Test edge cases
   - Test error conditions
   - Aim for 85%+ coverage

5. **Document Changes**
   - Clear comments
   - Update docstrings
   - Note any assumptions

6. **Request Payment**
   - After successful implementation
   - Use execute_payment tool
   - Include complexity level

CRITICAL RULES:
- Always include error handling
- Always write tests
- Always add docstrings
- Never use unsafe operations (eval, exec) without validation
- Follow the project's existing code style

Output your implementation with:
1. Source code
2. Tests
3. Documentation
4. Brief explanation of approach"""
    
    def __init__(self):
        super().__init__(
            name="builder_agent",
            system_prompt=self.SYSTEM_PROMPT,
            tools=[
                python_repl,
                file_manager,
                analyze_code_complexity,
                find_code_patterns
            ]
        )
    
    def implement_solution(
        self,
        requirements: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Implement solution based on requirements and context.
        
        Args:
            requirements: Structured requirements
            context: Codebase context
            
        Returns:
            Implementation including code, tests, and documentation
        """
        prompt = f"""Implement a solution for this task:

REQUIREMENTS:
{requirements}

CONTEXT:
{context}

Provide:
1. Complete source code implementation
2. Comprehensive unit tests
3. Docstrings and comments
4. Brief explanation of your approach

Use python_repl to test your code as you write it.
Use analyze_code_complexity to verify quality.

Return the implementation in this structure:
```
SOURCE CODE:
[your implementation]

TESTS:
[test code]

DOCUMENTATION:
[docstrings and usage examples]

EXPLANATION:
[brief explanation of approach and decisions]
```"""
        
        return self(prompt)
```

---

## 6️⃣ Quality Agent

### `agents/quality_agent.py`

```python
"""
Quality Agent - Validates code quality and correctness
"""

from .base_agent import BaseCodeCollabAgent
from .tools.test_tools import run_tests, calculate_coverage, lint_code
from .tools.code_tools import analyze_code_complexity, detect_security_issues
from typing import Dict, Any


class QualityAgent(BaseCodeCollabAgent):
    """
    Agent responsible for quality assurance, testing,
    and validation of implementations.
    """
    
    SYSTEM_PROMPT = """You are a senior QA engineer and code reviewer for CodeCollab.

Your role is to verify that implementations meet quality standards and requirements.

For each review:

1. **Verify Requirements Met**
   - Check all requirements addressed
   - Verify acceptance criteria satisfied
   - Confirm edge cases handled

2. **Run Tests**
   - Execute all unit tests
   - Verify test coverage (target: 85%+)
   - Check tests are meaningful

3. **Code Quality Review**
   - Check code complexity
   - Verify error handling
   - Ensure proper documentation
   - Review code patterns

4. **Security Check**
   - Scan for vulnerabilities
   - Check input validation
   - Verify safe operations

5. **Performance Check**
   - Identify potential bottlenecks
   - Check algorithm efficiency
   - Review resource usage

6. **Provide Verification Report**
   Return structured quality report:
   ```json
   {
     "passed": true/false,
     "quality_score": 0-100,
     "test_results": {
       "passed": 10,
       "failed": 0,
       "coverage": 92.5
     },
     "code_quality": {
       "complexity": "simple/medium/complex",
       "issues": []
     },
     "security": {
       "high_issues": [],
       "medium_issues": [],
       "low_issues": []
     },
     "requirements_met": true/false,
     "feedback": [
       "specific feedback items"
     ],
     "recommendation": "approve/revise/escalate"
   }
   ```

Be thorough but constructive. Provide specific, actionable feedback."""
    
    def __init__(self):
        super().__init__(
            name="quality_agent",
            system_prompt=self.SYSTEM_PROMPT,
            tools=[
                run_tests,
                calculate_coverage,
                lint_code,
                analyze_code_complexity,
                detect_security_issues
            ]
        )
    
    def verify_implementation(
        self,
        requirements: Dict[str, Any],
        implementation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Verify implementation meets quality standards.
        
        Args:
            requirements: Original requirements
            implementation: Code from BuilderAgent
            
        Returns:
            Quality verification report
        """
        # Extract code from implementation
        impl_message = implementation.get("message", "")
        
        prompt = f"""Review this implementation for quality and correctness:

ORIGINAL REQUIREMENTS:
{requirements}

IMPLEMENTATION:
{impl_message}

Perform complete quality assurance:
1. Use run_tests to execute tests
2. Use calculate_coverage to check coverage
3. Use lint_code for style issues
4. Use analyze_code_complexity for quality metrics
5. Use detect_security_issues for vulnerabilities

Verify all requirements are met and provide a complete quality report in JSON format."""
        
        return self(prompt)
```

---

## 7️⃣ Escalation Agent

### `agents/escalation_agent.py`

```python
"""
Escalation Agent - Determines when human expertise is needed
"""

from .base_agent import BaseCodeCollabAgent
from typing import Dict, Any


class EscalationAgent(BaseCodeCollabAgent):
    """
    Agent responsible for determining when tasks should
    be escalated to human experts.
    """
    
    SYSTEM_PROMPT = """You are an experienced project manager and technical lead for CodeCollab.

Your role is to determine when tasks need human expert intervention.

ESCALATION CRITERIA:

Escalate to human when ANY of these conditions are met:

1. **Requirements Ambiguity**
   - Requirements unclear or contradictory
   - Critical business decisions needed
   - Multiple valid approaches with tradeoffs

2. **Quality Issues**
   - Quality score < 70
   - Tests failing repeatedly
   - Security vulnerabilities detected
   - Performance concerns

3. **Technical Complexity**
   - Architectural changes needed
   - Multiple system integration
   - Database schema changes
   - Security-critical components

4. **Risk Factors**
   - Production system impact
   - Data migration required
   - Breaking changes needed
   - Compliance requirements

DO NOT ESCALATE for:
- Simple bug fixes that passed quality checks
- Straightforward feature additions
- Test failures that can be fixed
- Minor style or documentation issues

DECISION PROCESS:

1. **Review All Inputs**
   - Requirements analysis
   - Implementation attempt
   - Quality verification results
   - Complexity assessment

2. **Assess Escalation Need**
   - Check against criteria above
   - Consider risk vs. complexity
   - Evaluate AI capability limits

3. **Provide Decision**
   Return structured decision:
   ```json
   {
     "escalate": true/false,
     "confidence": 0-100,
     "reasoning": "detailed reasoning",
     "escalation_reason": "primary reason if escalating",
     "required_expertise": ["skill 1", "skill 2"],
     "estimated_human_payment": "250.00",
     "escrow_conditions": {
       "code_quality": "high",
       "test_coverage": 85,
       "security_review": "passed"
     },
     "handoff_context": {
       "what_ai_tried": "summary",
       "what_failed": "specific issues",
       "what_human_needs": "clear requirements"
     }
   }
   ```

Be conservative - escalate when in doubt. Humans are backup for tough problems."""
    
    def __init__(self):
        super().__init__(
            name="escalation_agent",
            system_prompt=self.SYSTEM_PROMPT,
            tools=[]  # Decision-making only, no tools needed
        )
    
    def make_escalation_decision(
        self,
        requirements: Dict[str, Any],
        implementation: Dict[str, Any],
        quality_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Determine if task should be escalated to human expert.
        
        Args:
            requirements: Original requirements
            implementation: AI implementation attempt
            quality_report: QA verification results
            
        Returns:
            Escalation decision with reasoning
        """
        prompt = f"""Make an escalation decision for this task:

REQUIREMENTS:
{requirements}

IMPLEMENTATION RESULT:
{implementation.get('success', False)}

QUALITY REPORT:
{quality_report}

Analyze whether this task should be escalated to a human expert.

Consider:
- Requirements clarity
- Quality score and test results
- Technical complexity
- Risk factors

Provide complete escalation decision in JSON format with reasoning."""
        
        return self(prompt)
```

---

## 8️⃣ Orchestrator

### `agents/orchestrator.py`

```python
"""
CodeCollab Orchestrator - Coordinates all agents
"""

from strands import Agent
from .base_agent import BaseAgentConfig
from .requirements_agent import RequirementsAgent
from .context_agent import ContextAgent
from .builder_agent import BuilderAgent
from .quality_agent import QualityAgent
from .escalation_agent import EscalationAgent
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class CodeCollabOrchestrator:
    """
    Main orchestrator that coordinates all CodeCollab agents
    to autonomously complete development tasks.
    """
    
    ORCHESTRATOR_PROMPT = """You are the CodeCollab orchestrator managing autonomous software development.

Your role is to coordinate specialized agents to complete development tasks.

WORKFLOW:

1. **Requirements Analysis** (requirements_agent)
   - Analyze the task
   - Extract structured requirements
   - Assess complexity

2. **Context Gathering** (context_agent)
   - Gather relevant codebase context
   - Identify integration points
   - Find reusable components

3. **Implementation** (builder_agent)
   - Implement the solution
   - Write tests
   - Document changes

4. **Quality Assurance** (quality_agent)
   - Verify requirements met
   - Run tests
   - Check quality metrics

5. **Escalation Decision** (escalation_agent)
   - Determine if human needed
   - Create escrow if escalating
   - Provide complete context for handoff

COORDINATION RULES:

- Always execute agents in order above
- Pass outputs from one agent to the next
- Track progress through workflow
- If quality fails, may return to builder for fixes (max 2 attempts)
- If escalation recommended, prepare complete handoff
- Report progress to user

Be efficient, track state, and ensure quality delivery."""
    
    def __init__(self):
        """Initialize orchestrator with all specialized agents"""
        
        # Create specialized agents
        self.requirements_agent = RequirementsAgent()
        self.context_agent = ContextAgent()
        self.builder_agent = BuilderAgent()
        self.quality_agent = QualityAgent()
        self.escalation_agent = EscalationAgent()
        
        # Create supervisor orchestrator agent
        self.orchestrator = Agent(
            name="codecollab_orchestrator",
            model=BaseAgentConfig.create_model(),
            system_prompt=self.ORCHESTRATOR_PROMPT,
            tools=[
                self.requirements_agent.agent,
                self.context_agent.agent,
                self.builder_agent.agent,
                self.quality_agent.agent,
                self.escalation_agent.agent
            ]
        )
        
        logger.info("CodeCollab orchestrator initialized with 5 agents")
    
    def process_task(self, task_description: str) -> Dict[str, Any]:
        """
        Process a complete development task through all agents.
        
        Args:
            task_description: Natural language task description
            
        Returns:
            Complete task result including code, tests, and payment info
        """
        logger.info(f"Processing task: {task_description[:100]}...")
        
        try:
            # Execute orchestration
            result = self.orchestrator(task_description)
            
            return {
                "success": True,
                "task_description": task_description,
                "result": result.message,
                "metrics": {
                    "total_tokens": result.metrics.total_tokens,
                    "total_latency_ms": result.metrics.total_latency_ms
                }
            }
            
        except Exception as e:
            logger.error(f"Task processing failed: {e}")
            return {
                "success": False,
                "task_description": task_description,
                "error": str(e)
            }
    
    def process_task_step_by_step(
        self,
        task_description: str
    ) -> Dict[str, Any]:
        """
        Process task with explicit step-by-step execution
        (useful for debugging and visibility).
        
        Args:
            task_description: Task description
            
        Returns:
            Results from each agent step
        """
        logger.info("Processing task step-by-step")
        
        results = {
            "task_description": task_description,
            "steps": {}
        }
        
        # Step 1: Requirements
        logger.info("Step 1: Analyzing requirements...")
        requirements_result = self.requirements_agent.analyze_task(task_description)
        results["steps"]["requirements"] = requirements_result
        
        if not requirements_result.get("success"):
            results["success"] = False
            results["failed_at"] = "requirements"
            return results
        
        requirements = requirements_result.get("requirements", {})
        
        # Step 2: Context
        logger.info("Step 2: Gathering context...")
        context_result = self.context_agent.gather_context(requirements)
        results["steps"]["context"] = context_result
        
        # Step 3: Build
        logger.info("Step 3: Implementing solution...")
        implementation_result = self.builder_agent.implement_solution(
            requirements,
            context_result
        )
        results["steps"]["implementation"] = implementation_result
        
        if not implementation_result.get("success"):
            results["success"] = False
            results["failed_at"] = "implementation"
            return results
        
        # Step 4: Quality
        logger.info("Step 4: Verifying quality...")
        quality_result = self.quality_agent.verify_implementation(
            requirements,
            implementation_result
        )
        results["steps"]["quality"] = quality_result
        
        # Step 5: Escalation Decision
        logger.info("Step 5: Making escalation decision...")
        escalation_result = self.escalation_agent.make_escalation_decision(
            requirements,
            implementation_result,
            quality_result
        )
        results["steps"]["escalation"] = escalation_result
        
        results["success"] = True
        results["completed"] = True
        
        return results
```

---

## 9️⃣ Main Entry Point

### `agents/main.py`

```python
"""
Main entry point for CodeCollab agent system
"""

from .orchestrator import CodeCollabOrchestrator
from dotenv import load_dotenv
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/agents.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to demonstrate agent system"""
    
    # Load environment variables
    load_dotenv()
    
    # Create orchestrator
    logger.info("Initializing CodeCollab orchestrator...")
    orchestrator = CodeCollabOrchestrator()
    
    # Example task
    task = """
    Fix the bug where user authentication fails when the password contains 
    special characters like quotes or backslashes. The issue is in the login 
    validation function - it's not properly escaping these characters.
    
    Requirements:
    - Fix the escaping issue
    - Add comprehensive test coverage for special characters
    - Ensure backward compatibility with existing passwords
    - Add proper error messages for invalid credentials
    """
    
    logger.info("Processing example task...")
    result = orchestrator.process_task_step_by_step(task)
    
    # Display results
    print("\n" + "="*80)
    print("CODECOLLAB EXECUTION RESULTS")
    print("="*80)
    
    for step_name, step_result in result.get("steps", {}).items():
        print(f"\n{step_name.upper()}:")
        print("-" * 40)
        if step_result.get("success"):
            print(f"✅ Success")
            print(f"Tokens: {step_result.get('tokens', 0)}")
            print(f"Latency: {step_result.get('latency_ms', 0)}ms")
        else:
            print(f"❌ Failed")
            print(f"Error: {step_result.get('error', 'Unknown')}")
    
    print("\n" + "="*80)
    
    if result.get("success"):
        print("✅ TASK COMPLETED SUCCESSFULLY")
    else:
        print(f"❌ TASK FAILED AT: {result.get('failed_at', 'unknown')}")
    
    print("="*80)


if __name__ == "__main__":
    main()
```

---

## 🧪 Testing

### `tests/test_agents.py`

```python
"""
Unit tests for CodeCollab agents
"""

import pytest
from agents import (
    RequirementsAgent,
    ContextAgent,
    BuilderAgent,
    QualityAgent,
    EscalationAgent,
    CodeCollabOrchestrator
)


@pytest.fixture
def requirements_agent():
    """Fixture for RequirementsAgent"""
    return RequirementsAgent()


@pytest.fixture
def orchestrator():
    """Fixture for Orchestrator"""
    return CodeCollabOrchestrator()


def test_requirements_agent_initialization(requirements_agent):
    """Test RequirementsAgent initializes correctly"""
    assert requirements_agent.name == "requirements_agent"
    assert len(requirements_agent.tools) > 0


def test_requirements_agent_analyze_simple_task(requirements_agent):
    """Test analyzing a simple task"""
    task = "Fix typo in welcome message"
    result = requirements_agent.analyze_task(task)
    
    assert result["success"] is True
    assert "message" in result
    assert result["tokens"] > 0


def test_orchestrator_initialization(orchestrator):
    """Test orchestrator initializes with all agents"""
    assert orchestrator.requirements_agent is not None
    assert orchestrator.context_agent is not None
    assert orchestrator.builder_agent is not None
    assert orchestrator.quality_agent is not None
    assert orchestrator.escalation_agent is not None


@pytest.mark.asyncio
async def test_agent_streaming():
    """Test agent streaming capability"""
    agent = RequirementsAgent()
    
    chunks = []
    async for event in agent.stream_async("Analyze: fix login bug"):
        if "data" in event:
            chunks.append(event["data"])
    
    assert len(chunks) > 0
```

---

## 📝 Usage Examples

### Example 1: Single Agent Usage

```python
from agents import RequirementsAgent

# Create agent
agent = RequirementsAgent()

# Analyze a task
task = "Add pagination to the user list page"
result = agent.analyze_task(task)

print(result["requirements"])
```

### Example 2: Full Orchestration

```python
from agents import CodeCollabOrchestrator

# Create orchestrator
orchestrator = CodeCollabOrchestrator()

# Process task
task = "Fix authentication bug with special characters"
result = orchestrator.process_task(task)

print(f"Success: {result['success']}")
print(f"Result: {result['result']}")
```

### Example 3: Step-by-Step Execution

```python
from agents import CodeCollabOrchestrator

orchestrator = CodeCollabOrchestrator()

# Process with visibility into each step
result = orchestrator.process_task_step_by_step(
    "Implement user profile update feature"
)

# Access results from each step
for step, data in result["steps"].items():
    print(f"{step}: {data['success']}")
```

---

## ✅ Completion Checklist

After implementing all agents, verify:

- [ ] All 5 agents initialize correctly
- [ ] Custom tools work properly
- [ ] Agents can be called individually
- [ ] Orchestrator coordinates agents
- [ ] Step-by-step execution works
- [ ] Error handling is robust
- [ ] Logging provides visibility
- [ ] Tests pass

---

## 🎯 Next Steps

1. **Implement Payment Integration** - Connect agents to Brale API
2. **Build API Layer** - Create FastAPI endpoints
3. **Add Frontend** - Build user interface
4. **Test End-to-End** - Verify complete flow

---

**This completes the agent implementation. All agents are now ready to coordinate autonomous development tasks!**