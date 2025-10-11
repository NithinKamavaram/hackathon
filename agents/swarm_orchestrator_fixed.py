"""
CodeCollab Swarm Orchestrator - Fixed Implementation
Properly uses Strands SDK patterns for agent coordination
"""

from strands import Agent
from strands.multiagent import Swarm
from .base_agent import BaseAgentConfig
from typing import Dict, Any, List, Optional
import logging
import json

logger = logging.getLogger(__name__)


class CodeCollabSwarm:
    """
    Swarm orchestrator with proper Strands SDK implementation.
    Agents communicate through their responses, not function calls.
    """

    def __init__(self):
        """Initialize swarm with specialized agents"""

        # Create agents with proper handoff patterns
        self.agents = [
            self._create_requirements_agent(),
            self._create_context_agent(),
            self._create_builder_agent(),
            self._create_quality_agent(),
            self._create_escalation_agent()
        ]

        # Create swarm configuration
        self.swarm = Swarm(
            agents=self.agents,
            max_handoffs=20,
            max_iterations=20,
            execution_timeout=900.0,
            node_timeout=300.0
        )

        logger.info("CodeCollab Swarm initialized with 5 specialized agents")

    def _create_requirements_agent(self) -> Agent:
        """Requirements analysis agent"""
        return Agent(
            name="requirements_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""You are the Requirements Agent analyzing development tasks.

Your job:
1. Extract clear requirements from task descriptions
2. Identify acceptance criteria and edge cases
3. Assess complexity (simple/medium/complex)
4. Structure the requirements for the next agent

Output a JSON-like structure:
{
  "task_type": "bug_fix" or "feature",
  "requirements": [
    {"id": "REQ-1", "description": "...", "priority": "high/medium/low"}
  ],
  "acceptance_criteria": ["criterion 1", "criterion 2"],
  "edge_cases": ["case 1", "case 2"],
  "complexity": "simple/medium/complex",
  "estimated_effort": "15min/1hr/3hr",
  "next_agent": "context_agent",
  "handoff_message": "Requirements analyzed. Context agent should gather codebase information."
}

ALWAYS include "next_agent": "context_agent" to trigger handoff."""
        )

    def _create_context_agent(self) -> Agent:
        """Context gathering agent"""
        return Agent(
            name="context_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""You are the Context Agent understanding codebases.

Your job:
1. Analyze the codebase structure based on requirements
2. Identify where code should be added/modified
3. Find reusable components and patterns
4. Map integration points

Output structure:
{
  "relevant_files": [
    {"path": "file.py", "purpose": "...", "modifications_needed": "..."}
  ],
  "integration_points": [
    {"location": "module.function", "action": "add/modify/extend"}
  ],
  "patterns_to_follow": ["pattern 1", "pattern 2"],
  "reusable_components": ["component 1", "component 2"],
  "next_agent": "builder_agent",
  "handoff_message": "Context gathered. Builder agent should implement the solution.",
  "context_for_builder": {
    "requirements": "<from previous agent>",
    "implementation_guidance": "..."
  }
}

ALWAYS include "next_agent": "builder_agent" to continue the flow."""
        )

    def _create_builder_agent(self) -> Agent:
        """Code implementation agent"""
        return Agent(
            name="builder_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""You are the Builder Agent writing production code.

Your job:
1. Implement the solution based on requirements and context
2. Write clean, tested code following best practices
3. Include error handling and documentation
4. Create unit tests

Output format:
{
  "implementation": {
    "code": "```python\\n<your code here>\\n```",
    "tests": "```python\\n<test code here>\\n```",
    "documentation": "Usage instructions and examples"
  },
  "approach_explanation": "Brief explanation of implementation approach",
  "test_coverage_estimate": "85%",
  "next_agent": "quality_agent",
  "handoff_message": "Implementation complete. Quality agent should verify."
}

Write actual Python code in the code and tests sections.
ALWAYS include "next_agent": "quality_agent" for quality check."""
        )

    def _create_quality_agent(self) -> Agent:
        """Quality assurance agent"""
        return Agent(
            name="quality_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""You are the Quality Agent verifying implementations.

Your job:
1. Check if requirements are met
2. Verify code quality and test coverage
3. Check for security issues
4. Assess overall quality

Output structure:
{
  "quality_check": {
    "requirements_met": true/false,
    "code_quality_score": 0-100,
    "test_coverage": "estimated %",
    "security_issues": [],
    "suggestions": []
  },
  "verdict": "pass" or "fail" or "needs_revision",
  "next_agent": "escalation_agent" (if pass) or "builder_agent" (if fail),
  "handoff_message": "Quality check complete. <next steps>"
}

If quality passes (score >= 70), send to escalation_agent.
If quality fails but fixable, send back to builder_agent with feedback.
Include specific feedback for improvements."""
        )

    def _create_escalation_agent(self) -> Agent:
        """Escalation decision agent"""
        return Agent(
            name="escalation_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""You are the Escalation Agent making final decisions.

Your job:
1. Review the complete task flow
2. Decide if AI completed successfully or needs human help
3. Prepare final deliverables or escalation context

For AI-completed tasks, output:
{
  "decision": "ai_complete",
  "confidence": 0-100,
  "final_code": "<the working code>",
  "final_tests": "<the test code>",
  "summary": "Task completed successfully",
  "estimated_payment": "$0.01-$0.10"
}

For human escalation, output:
{
  "decision": "escalate_to_human",
  "reason": "Why escalation is needed",
  "ai_attempt_summary": "What AI tried",
  "human_requirements": "What human needs to do",
  "estimated_payment": "$10-$250",
  "handoff_context": {
    "partial_solution": "...",
    "blockers": "...",
    "recommendations": "..."
  }
}

This agent is the FINAL agent - no "next_agent" field needed."""
        )

    def process_task(self, task_description: str) -> Dict[str, Any]:
        """
        Process a development task through the swarm.

        Args:
            task_description: Natural language task description

        Returns:
            Complete task result with code, tests, and decision
        """
        logger.info(f"Processing task: {task_description[:100]}...")

        try:
            # Execute swarm with the task
            result = self.swarm(task_description)

            # Parse the result
            return self._parse_swarm_result(result, task_description)

        except Exception as e:
            logger.error(f"Swarm processing failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "task_description": task_description
            }

    def _parse_swarm_result(self, result: Any, task_description: str) -> Dict[str, Any]:
        """Parse swarm execution result into structured output"""

        # If result is already a dict (from mock), use it directly with enhancements
        if isinstance(result, dict):
            response = result.copy()
            response["task_description"] = task_description
            response["agent_count"] = len(response.get("agent_sequence", []))
            
            # Ensure final_decision is set
            if "final_decision" not in response:
                response["final_decision"] = response.get("decision", "COMPLETE")
            
            # Ensure code is extracted from final_result if not present
            if "code" not in response and "final_result" in response:
                response["code"] = response["final_result"]
            
            return response

        # Extract agent sequence
        agent_sequence = []
        agent_outputs = {}

        if hasattr(result, 'node_history'):
            for node in result.node_history:
                agent_name = getattr(node, 'node_id', 'unknown')
                agent_sequence.append(agent_name)

                # Capture agent output
                if hasattr(node, 'response'):
                    agent_outputs[agent_name] = str(node.response)[:500]

        # Extract final result
        final_result = getattr(result, 'result', str(result))

        # Try to extract code and tests from final result
        code = None
        tests = None
        decision = None

        if isinstance(final_result, str):
            # Try to parse JSON-like structure
            try:
                import re
                # Extract code blocks
                code_match = re.search(r'```python\n(.*?)```', final_result, re.DOTALL)
                if code_match:
                    code = code_match.group(1).strip()

                # Look for test code
                test_match = re.search(r'tests["\']:\s*["\']```python\n(.*?)```', final_result, re.DOTALL)
                if test_match:
                    tests = test_match.group(1).strip()

                # Look for decision
                if '"ai_complete"' in final_result or 'COMPLETE' in final_result:
                    decision = "COMPLETE"
                elif '"escalate_to_human"' in final_result or 'ESCALATE' in final_result:
                    decision = "ESCALATE"
            except:
                pass

        return {
            "success": True,
            "task_description": task_description,
            "agent_sequence": agent_sequence,
            "agent_count": len(agent_sequence),
            "final_decision": decision or "COMPLETE",
            "code": code or final_result,
            "tests": tests,
            "agent_outputs": agent_outputs,
            "raw_result": str(final_result)[:1000]  # Truncate for readability
        }


class SimpleSwarmOrchestrator:
    """
    Simplified orchestrator that processes tasks step by step.
    Easier to debug and understand the flow.
    """

    def __init__(self):
        """Initialize individual agents"""
        self.requirements_agent = self._create_simple_requirements_agent()
        self.builder_agent = self._create_simple_builder_agent()
        self.quality_agent = self._create_simple_quality_agent()

    def _create_simple_requirements_agent(self) -> Agent:
        """Simple requirements agent"""
        return Agent(
            name="requirements",
            model=BaseAgentConfig.create_model(),
            system_prompt="""Analyze the task and extract requirements.
Output: Clear requirements list with acceptance criteria."""
        )

    def _create_simple_builder_agent(self) -> Agent:
        """Simple builder agent"""
        return Agent(
            name="builder",
            model=BaseAgentConfig.create_model(),
            system_prompt="""Write Python code to solve the task.
Include: 1) Implementation 2) Tests 3) Documentation.
Use proper error handling and type hints."""
        )

    def _create_simple_quality_agent(self) -> Agent:
        """Simple quality agent"""
        return Agent(
            name="quality",
            model=BaseAgentConfig.create_model(),
            system_prompt="""Review the code for quality.
Check: Requirements met, tests included, clean code.
Output: Pass/Fail with specific feedback."""
        )

    def process_task_simple(self, task: str) -> Dict[str, Any]:
        """Process task through agents sequentially"""

        results = {"task": task, "steps": {}}

        try:
            # Step 1: Requirements
            req_result = self.requirements_agent(f"Task: {task}")
            results["steps"]["requirements"] = {
                "output": getattr(req_result, 'message', str(req_result))
            }

            # Step 2: Build
            build_prompt = f"""Task: {task}
Requirements: {results['steps']['requirements']['output']}
Write the implementation."""

            build_result = self.builder_agent(build_prompt)
            results["steps"]["implementation"] = {
                "output": getattr(build_result, 'message', str(build_result))
            }

            # Step 3: Quality check
            quality_prompt = f"""Review this implementation:
{results['steps']['implementation']['output']}
Does it meet the requirements?"""

            quality_result = self.quality_agent(quality_prompt)
            results["steps"]["quality"] = {
                "output": getattr(quality_result, 'message', str(quality_result))
            }

            results["success"] = True

        except Exception as e:
            results["success"] = False
            results["error"] = str(e)

        return results