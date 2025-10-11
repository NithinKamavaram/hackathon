"""
Strands-based Agent Implementations for CodeCollab
Following official Strands SDK patterns and best practices
"""

from strands import Agent, tool
from strands.models import BedrockModel
from .base_agent import BaseAgentConfig
from .tools.strands_tools import (
    analyze_code_complexity, extract_code_blocks, validate_python_syntax,
    run_python_tests, generate_test_cases, assess_task_difficulty
)
import logging

# Configure logging as recommended by Strands
logging.getLogger("strands").setLevel(logging.INFO)
logger = logging.getLogger(__name__)


class RequirementsAgent:
    """Requirements analysis agent using Strands SDK"""
    
    def __init__(self):
        self.agent = Agent(
            system_prompt="""You are a Requirements Analyst specialized in software development tasks.
            
Your role:
- Analyze development requests and extract clear, structured requirements
- Identify acceptance criteria and edge cases
- Assess task complexity and feasibility
- Structure requirements for implementation teams

Always provide:
1. Clear, numbered requirements
2. Acceptance criteria for each requirement  
3. Edge cases to consider
4. Technical constraints or dependencies
5. Complexity assessment (Simple/Medium/Complex)

Use the assess_task_difficulty tool to help evaluate complexity.""",
            tools=[assess_task_difficulty],
            model=BaseAgentConfig.create_model()
        )
    
    def __call__(self, task_description: str):
        """Analyze task requirements"""
        prompt = f"""
        Analyze this development task and provide structured requirements:
        
        Task: {task_description}
        
        Please use the assess_task_difficulty tool first, then provide:
        1. Structured requirements (numbered list)
        2. Acceptance criteria for each requirement
        3. Edge cases to consider
        4. Technical constraints
        5. Overall complexity assessment
        """
        
        response = self.agent(prompt)
        logger.info("Requirements analysis completed")
        return response


class ContextAgent:
    """Code context and architecture agent using Strands SDK"""
    
    def __init__(self):
        self.agent = Agent(
            system_prompt="""You are a Software Architecture and Context Analyst.
            
Your role:
- Understand codebase context and patterns
- Suggest appropriate design patterns and architectures
- Identify integration points and dependencies
- Provide implementation guidance

Focus on:
1. Code structure and organization
2. Design patterns that fit the requirements
3. Dependencies and imports needed
4. Integration considerations
5. Best practices for the specific task type

Provide clear, actionable architectural guidance.""",
            model=BaseAgentConfig.create_model()
        )
    
    def __call__(self, requirements_and_context: str):
        """Provide architectural context and guidance"""
        response = self.agent(requirements_and_context)
        logger.info("Context analysis completed")
        return response


class BuilderAgent:
    """Code generation agent using Strands SDK"""
    
    def __init__(self):
        self.agent = Agent(
            system_prompt="""You are an Expert Python Developer and Code Builder.
            
Your role:
- Write production-quality Python code that meets exact requirements
- Include proper type hints, docstrings, and error handling
- Generate comprehensive test cases
- Follow Python best practices and PEP standards

Code Requirements:
1. Always include type hints for function parameters and return values
2. Write detailed docstrings with Args, Returns, and Examples
3. Handle edge cases and provide proper error messages
4. Include basic test assertions to verify functionality
5. Use meaningful variable and function names
6. Follow PEP 8 style guidelines

Format your code in ```python blocks for clarity.

Use available tools to validate your code before finalizing.""",
            tools=[validate_python_syntax, generate_test_cases, extract_code_blocks],
            model=BaseAgentConfig.create_model()
        )
    
    def __call__(self, requirements_and_context: str):
        """Generate Python code based on requirements"""
        prompt = f"""
        Based on the requirements and context provided, write production-quality Python code:
        
        {requirements_and_context}
        
        Requirements:
        1. Write complete, working Python code
        2. Include proper type hints and docstrings
        3. Add error handling for edge cases
        4. Include test cases to verify functionality
        5. Use the validate_python_syntax tool to check your code
        
        Provide the code in ```python blocks.
        """
        
        response = self.agent(prompt)
        logger.info("Code generation completed")
        return response


class QualityAgent:
    """Quality assurance and testing agent using Strands SDK"""
    
    def __init__(self):
        self.agent = Agent(
            system_prompt="""You are a Quality Assurance Engineer and Code Reviewer.
            
Your role:
- Review code for correctness, quality, and best practices
- Validate that code meets all requirements
- Check for potential bugs, security issues, and performance problems
- Ensure adequate test coverage
- Provide specific, actionable feedback

Review checklist:
1. Code correctness and logic
2. Requirement compliance
3. Error handling and edge cases
4. Code quality and readability
5. Security considerations
6. Performance implications
7. Test coverage adequacy

Use available tools to thoroughly analyze the code.""",
            tools=[
                analyze_code_complexity, validate_python_syntax, 
                extract_code_blocks, run_python_tests
            ],
            model=BaseAgentConfig.create_model()
        )
    
    def __call__(self, code_and_requirements: str):
        """Review code quality and compliance"""
        prompt = f"""
        Please review this code implementation for quality and compliance:
        
        {code_and_requirements}
        
        Use your tools to:
        1. Extract and validate the code syntax
        2. Analyze code complexity
        3. Run tests if present
        4. Check requirement compliance
        
        Provide a comprehensive quality assessment with specific feedback.
        """
        
        response = self.agent(prompt)
        logger.info("Quality review completed")
        return response


class EscalationAgent:
    """Decision making agent for task completion or human escalation"""
    
    def __init__(self):
        self.agent = Agent(
            system_prompt="""You are an AI Task Completion Decision Maker.
            
Your role:
- Determine if a development task has been successfully completed by AI agents
- Decide when human expert intervention is needed
- Assess the quality and completeness of delivered solutions
- Make final go/no-go decisions

Decision criteria:
- COMPLETE: Task fully implemented, tested, and meets requirements
- ESCALATE: Task too complex, has critical issues, or needs human expertise
- CLARIFICATION_NEEDED: Requirements unclear or insufficient information

Factors to consider:
1. Requirement completeness and compliance
2. Code quality and correctness
3. Test coverage and validation
4. Security and performance implications
5. Complexity vs AI capabilities
6. Risk assessment

Always provide clear reasoning for your decision.""",
            tools=[assess_task_difficulty, analyze_code_complexity],
            model=BaseAgentConfig.create_model()
        )
    
    def __call__(self, full_task_summary: str):
        """Make final decision on task completion"""
        prompt = f"""
        Review the complete task execution and make a final decision:
        
        {full_task_summary}
        
        Use your tools to assess task difficulty and code complexity.
        
        Provide your decision as one of:
        - COMPLETE: Task successfully finished
        - ESCALATE: Needs human expert
        - CLARIFICATION_NEEDED: More information required
        
        Include clear reasoning for your decision.
        """
        
        response = self.agent(prompt)
        logger.info("Escalation decision completed")
        return response