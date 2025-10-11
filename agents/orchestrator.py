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