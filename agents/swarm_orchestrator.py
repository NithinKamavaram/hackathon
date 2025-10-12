"""
CodeCollab Swarm Orchestrator - Uses Swarm Intelligence Pattern
"""

from strands import Agent
from strands.multiagent import Swarm
from .base_agent import BaseAgentConfig
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class CodeCollabSwarm:
    """
    Swarm-based orchestrator using autonomous agent coordination
    with shared context and collective intelligence.
    """

    def __init__(self):
        """Initialize swarm with specialized agents"""

        # Create specialized agents with swarm-aware prompts
        self.requirements_agent = self._create_requirements_agent()
        self.context_agent = self._create_context_agent()
        self.builder_agent = self._create_builder_agent()
        self.quality_agent = self._create_quality_agent()
        self.escalation_agent = self._create_escalation_agent()

        # Store agents list for swarm execution
        self.agents = [
            self.requirements_agent,
            self.context_agent,
            self.builder_agent,
            self.quality_agent,
            self.escalation_agent
        ]

        # Create the swarm with optimized configuration
        self.swarm = Swarm(
            self.agents,  # Pass agents as first positional argument
            max_handoffs=10,  # Reduced from 20
            max_iterations=10,  # Reduced from 20
            execution_timeout=120.0,  # 2 minutes (reduced from 15 min)
            node_timeout=30.0,  # 30 seconds per agent (reduced from 5 min)
            repetitive_handoff_detection_window=5,  # Reduced from 8
            repetitive_handoff_min_unique_agents=3
        )

        logger.info("CodeCollab Swarm initialized with 5 specialized agents")

    def _create_requirements_agent(self) -> Agent:
        """Create requirements analysis agent with swarm coordination"""
        return Agent(
            name="requirements_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""You are the Requirements Agent in the CodeCollab swarm specializing in task analysis.

Your role in the swarm:
1. You are typically the FIRST agent to analyze new development tasks
2. Extract structured requirements from natural language descriptions
3. Identify acceptance criteria, edge cases, and constraints
4. Assess task complexity (simple/medium/complex)
5. Estimate AI payment requirements

When to handoff:
- After completing requirements analysis, handoff to context_agent with the structured requirements
- If the task description is unclear, gather what you can then handoff to context_agent
- If you identify this as a complex architectural task, note this for escalation_agent

Output format:
Provide structured requirements including:
- Task type (bug_fix/feature)
- Clear requirements list with acceptance criteria
- Edge cases to consider
- Complexity assessment
- Estimated payments

Use handoff_to_agent to transfer to context_agent after analysis:
handoff_to_agent(
    agent_name="context_agent",
    message="Requirements analysis complete. Please gather codebase context for implementation.",
    context={"requirements": <your_structured_requirements>}
)"""
        )

    def _create_context_agent(self) -> Agent:
        """Create context gathering agent with swarm coordination"""
        return Agent(
            name="context_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""You are the Context Agent in the CodeCollab swarm specializing in codebase analysis.

Your role in the swarm:
1. Receive requirements from requirements_agent
2. Analyze what context is needed for implementation
3. Identify integration points and reusable components
4. Map dependencies and affected areas
5. Provide implementation context

When to handoff:
- After gathering context, handoff to builder_agent with context + requirements
- If no implementation is needed (documentation only), handoff to quality_agent
- If requirements are unclear, note this for builder_agent

What to analyze:
- What files or code structure is needed
- Where new code should be added
- Existing patterns to follow (if applicable)
- Components that can be reused
- Areas that will be affected
- Technology stack considerations

Use handoff_to_agent to transfer to builder_agent after context gathering:
handoff_to_agent(
    agent_name="builder_agent",
    message="Context analysis complete. Please implement the solution based on requirements and context.",
    context={
        "requirements": <requirements>,
        "codebase_context": <your_context_analysis>
    }
)"""
        )

    def _create_builder_agent(self) -> Agent:
        """Create implementation agent with swarm coordination"""
        return Agent(
            name="builder_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""You are the Builder Agent in the CodeCollab swarm specializing in code implementation.

Your role in the swarm:
1. Receive requirements and context from previous agents
2. Write production-quality code following best practices
3. Include comprehensive error handling
4. Create unit tests with 85%+ coverage target
5. Add proper documentation and docstrings

When to handoff:
- After implementation, handoff to quality_agent for verification
- If requirements are ambiguous, handoff back to requirements_agent
- If missing critical context, handoff to context_agent
- If the implementation is too complex, note for escalation_agent

Implementation standards:
- Follow SOLID principles
- Include type hints
- Write comprehensive tests
- Add clear docstrings
- Handle edge cases
- Never use unsafe operations (eval, exec) without validation

Output format:
Provide:
1. Complete source code
2. Unit tests
3. Documentation
4. Brief explanation of approach

Use handoff_to_agent to transfer to quality_agent after implementation:
handoff_to_agent(
    agent_name="quality_agent",
    message="Implementation complete. Please verify quality and run tests.",
    context={"implementation": <your_code>, "tests": <your_tests>}
)"""
        )

    def _create_quality_agent(self) -> Agent:
        """Create quality assurance agent with swarm coordination"""
        return Agent(
            name="quality_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""You are the Quality Agent in the CodeCollab swarm specializing in quality assurance.

Your role in the swarm:
1. Receive implementation from builder_agent
2. Verify all requirements are met
3. Evaluate tests and implementation quality
4. Review code quality and patterns
5. Check for security vulnerabilities
6. Assess overall quality score

BE VERY LENIENT for simple tasks. If the code works and has ANY tests, PASS it.

Quality scoring guidelines for SIMPLE tasks (algorithms, basic functions):
- Has working code that meets the requirement? → Score 85 (PASS)
- Has any test at all? → Add +5 points
- Has docstring? → Add +5 points
- Use this formula: base 85 + bonuses = usually 90-95 for simple tasks

Quality scoring guidelines for COMPLEX tasks (only):
- 90-100: Excellent - comprehensive tests, clean code, all best practices
- 75-89: Good - working implementation, reasonable tests, meets requirements
- 70-74: Acceptable - works correctly, basic tests, minor improvements possible
- Below 70: Needs work - missing requirements, failing tests, or security issues

DEFAULT: For simple tasks with working code → Score 85-90 (ALWAYS PASS)

When to handoff:
- If quality PASSES (score >= 70), ALWAYS handoff to escalation_agent
- If quality FAILS (score < 70) on FIRST check, handoff to builder_agent with feedback
- If quality FAILS on SECOND check, handoff to escalation_agent (let them decide)
- Maximum 1 round trip with builder_agent before escalating decision

Quality criteria (prioritized):
1. Code works correctly and meets requirements (MOST IMPORTANT)
2. Has tests that verify functionality
3. No critical security vulnerabilities
4. Reasonable code quality
5. Proper error handling

Output format:
Provide quality report with:
- Pass/fail status
- Quality score (0-100)
- Test results summary
- Requirements verification
- Specific feedback (only if failing)

Use handoff_to_agent based on quality results:
If passed (score >= 70):
handoff_to_agent(
    agent_name="escalation_agent",
    message="Quality verification passed with score X/100. Please make final decision.",
    context={"quality_report": <your_report>, "quality_score": <score>, "status": "PASS"}
)

If failed on first check (score < 70):
handoff_to_agent(
    agent_name="builder_agent",
    message="Quality check failed (score X/100). Please fix these specific issues.",
    context={"issues": <specific_issues>, "suggestions": <how_to_fix>, "attempt": 1}
)

If failed on second check:
handoff_to_agent(
    agent_name="escalation_agent",
    message="Quality still below threshold after revision. Escalation decision needed.",
    context={"quality_report": <your_report>, "quality_score": <score>, "attempt": 2}
)"""
        )

    def _create_escalation_agent(self) -> Agent:
        """Create escalation decision agent with swarm coordination"""
        return Agent(
            name="escalation_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""You are the Escalation Agent in the CodeCollab swarm making final decisions.

Your role in the swarm:
1. Review the complete task history from all agents
2. Make the final decision on task completion or human escalation
3. Prepare payment information (AI micropayment or human escrow)
4. Create handoff context if escalating to human

CRITICAL DEFAULT: For 95% of tasks, DO NOT ESCALATE. Only escalate if MULTIPLE critical issues exist.

Escalation criteria - Escalate to human ONLY if MULTIPLE of these are true:
- Quality score < 50 (severely broken)
- Critical security vulnerabilities with data exposure
- Major architectural changes affecting multiple systems
- Requirements completely unclear after multiple attempts
- Failed quality checks 3+ times with no improvement
- Distributed systems or microservices architecture needed

ALWAYS COMPLETE (DO NOT ESCALATE) for:
- Any task that has working code (quality score >= 70)
- Simple algorithms: Fibonacci, factorial, sorting, prime numbers, etc.
- Basic functions: add, subtract, check even/odd, string operations
- CRUD operations, data transformations, utility functions
- Any code that passes tests and meets requirements
- Minor improvements or style issues
- Straightforward features with good test coverage

DEFAULT DECISION: If quality score >= 70 → COMPLETE (not escalate)

Decision process:
1. Review all agent contributions
2. Check quality score and test results
3. Assess technical complexity
4. Evaluate risk factors
5. Make escalation decision

CRITICAL: To complete the swarm (STOP the loop):
- DO NOT call handoff_to_agent after making your final decision
- Simply provide your final response with the decision
- The swarm will automatically end when you don't call handoff_to_agent

If NOT escalating (AI complete - DEFAULT FOR MOST CASES):
You MUST start your response with exactly this line:
"DECISION: COMPLETE"

Then provide details:
"DECISION: COMPLETE

Status: AI Implementation Successful
Payment: Micropayment $0.05
Quality Score: 85/100

The task has been completed by the AI agents. The implementation includes working code,
tests, and meets all requirements.

Final implementation:
[Include the final code here]"

If escalating to human (RARE - < 5% OF CASES):
You MUST start your response with exactly this line:
"DECISION: ESCALATE"

Then provide details:
"DECISION: ESCALATE

Status: Requires Human Expertise
Payment: Escrow $50
Reason: [Specific reason - must be multiple critical issues]

Context for human developer:
- What AI attempted: [Summary]
- Critical issues: [List multiple issues]
- Why human expertise needed: [Specific guidance]

Current implementation:
[Include partial code if any]"

REMEMBER: DO NOT use handoff_to_agent after making your decision. Just provide your final response."""
        )

    def process_task(self, task_description: str) -> Dict[str, Any]:
        """
        Process task using swarm intelligence.

        Args:
            task_description: Development task description

        Returns:
            Swarm execution result
        """
        logger.info(f"Processing task with swarm: {task_description[:100]}...")

        try:
            # Execute task using the swarm
            result = self.swarm(task_description)

            # Extract agent sequence from node history
            agent_sequence = [node.node_id for node in result.node_history] if hasattr(result, 'node_history') else []

            # Count handoffs (transitions between agents)
            handoff_count = len(agent_sequence) - 1 if len(agent_sequence) > 1 else 0

            # Extract execution metrics
            execution_time_ms = result.execution_time if hasattr(result, 'execution_time') else 0

            # Extract detailed agent outputs and context
            agent_outputs = {}
            deliverables = {}
            quality_metrics = {}
            
            if hasattr(result, 'node_history'):
                for node in result.node_history:
                    agent_name = node.node_id
                    
                    # Capture agent output/response
                    agent_output = {}
                    if hasattr(node, 'response') and node.response:
                        agent_output['response'] = str(node.response)[:500]  # First 500 chars
                    
                    # Capture context passed to next agent
                    if hasattr(node, 'context') and node.context:
                        agent_output['context'] = node.context
                    
                    # Capture handoff message
                    if hasattr(node, 'handoff_message') and node.handoff_message:
                        agent_output['handoff_message'] = node.handoff_message
                    
                    agent_outputs[agent_name] = agent_output

            # Extract final result details
            final_result_str = result.result if hasattr(result, 'result') else str(result)

            # Extract code from markdown blocks
            import re
            # Find all Python code blocks in the final result
            code_blocks = re.findall(r'```python\n(.*?)```', final_result_str, re.DOTALL)
            if code_blocks:
                # Use the first substantial code block (skip test code usually comes later)
                # Look for the main implementation (not just tests)
                main_code = None
                for block in code_blocks:
                    # Skip blocks that are primarily imports or tests
                    if 'def test_' not in block and 'import pytest' not in block:
                        if 'def ' in block or 'class ' in block:  # Has actual implementation
                            main_code = block.strip()
                            break

                # If we found main code, use it; otherwise use the first block
                deliverables['code'] = main_code if main_code else code_blocks[0].strip()
            
            # Extract shared knowledge if available
            shared_knowledge = self._extract_shared_knowledge(result) if hasattr(result, 'node_history') else {}

            # Determine success status
            success_status = result.status == "success" if hasattr(result, 'status') else (result.get('success', True) if isinstance(result, dict) else True)

            # Extract decision from escalation agent's response
            final_decision = "COMPLETE"  # Default to complete
            if "DECISION: ESCALATE" in final_result_str:
                final_decision = "ESCALATE"
            elif "DECISION: COMPLETE" in final_result_str:
                final_decision = "COMPLETE"
            elif "ESCALATE" in final_result_str.upper() and "DO NOT ESCALATE" not in final_result_str.upper():
                # Fallback: if ESCALATE appears without "DO NOT ESCALATE"
                final_decision = "ESCALATE"
            # Otherwise keep default of COMPLETE

            # Build response
            response = {
                "success": success_status and final_decision == "COMPLETE",  # Only success if completed
                "task_description": task_description,
                "final_result": final_result_str,
                "final_message": final_result_str[:300] if len(final_result_str) > 300 else final_result_str,
                "agent_sequence": agent_sequence,
                "agent_outputs": agent_outputs,
                "deliverables": deliverables,
                "quality_metrics": quality_metrics,
                "handoff_count": handoff_count,
                "execution_time_ms": execution_time_ms,
                "total_tokens": 0,  # Token counting would need additional implementation
                "shared_knowledge": shared_knowledge,
                "code": deliverables.get('code'),  # Add extracted code to response
                "final_decision": final_decision
            }

            # Pass through additional fields from mock (for testing)
            if isinstance(result, dict):
                for key in ['decision', 'final_decision', 'code', 'tests', 'tokens_used', 'latency_ms']:
                    if key in result:
                        response[key] = result[key]

            return response

        except Exception as e:
            logger.error(f"Swarm processing failed: {e}", exc_info=True)
            return {
                "success": False,
                "task_description": task_description,
                "error": str(e)
            }

    def _extract_shared_knowledge(self, result) -> Dict[str, Any]:
        """Extract shared knowledge from swarm execution"""
        knowledge = {}
        for node in result.node_history:
            if hasattr(node, 'context') and node.context:
                knowledge[node.node_id] = {
                    "contribution": str(node.context)[:200],  # Truncate for readability
                    "handoff_message": getattr(node, 'handoff_message', None)
                }
        return knowledge

    async def process_task_async(self, task_description: str) -> Dict[str, Any]:
        """
        Process task asynchronously using swarm.

        Args:
            task_description: Development task description

        Returns:
            Swarm execution result
        """
        logger.info(f"Processing task asynchronously: {task_description[:100]}...")

        try:
            result = await self.swarm.invoke_async(task_description)

            # Extract agent sequence
            agent_sequence = [node.node_id for node in result.node_history] if hasattr(result, 'node_history') else []

            # Count handoffs
            handoff_count = len(agent_sequence) - 1 if len(agent_sequence) > 1 else 0

            return {
                "success": result.status == "success" if hasattr(result, 'status') else True,
                "task_description": task_description,
                "final_result": result.result if hasattr(result, 'result') else str(result),
                "agent_sequence": agent_sequence,
                "handoff_count": handoff_count,
                "execution_time_ms": result.execution_time if hasattr(result, 'execution_time') else 0,
                "shared_knowledge": self._extract_shared_knowledge(result) if hasattr(result, 'node_history') else {}
            }
        except Exception as e:
            logger.error(f"Async swarm processing failed: {e}")
            return {
                "success": False,
                "task_description": task_description,
                "error": str(e)
            }


class CodeCollabSwarmTool:
    """
    Alternative implementation using the built-in swarm tool
    for quick setup and automated agent creation.
    """

    def __init__(self):
        """Initialize agent with swarm tool"""
        self.agent = Agent(
            tools=[swarm_tool],
            system_prompt="You orchestrate a swarm of specialized agents for software development tasks."
        )
        logger.info("CodeCollab Swarm Tool initialized")

    def process_with_auto_swarm(self, task_description: str) -> Dict[str, Any]:
        """
        Process task using the swarm tool with automatic agent creation.

        Args:
            task_description: Development task description

        Returns:
            Execution result
        """
        result = self.agent.tool.swarm(
            task=f"Development task: {task_description}",
            agents=[
                {
                    "name": "requirements_analyst",
                    "system_prompt": "You analyze requirements and create structured specifications. Focus on extracting clear acceptance criteria and identifying edge cases."
                },
                {
                    "name": "architect",
                    "system_prompt": "You understand codebases and design solutions. Identify the best architecture patterns and integration points."
                },
                {
                    "name": "developer",
                    "system_prompt": "You write production-quality code with tests. Follow best practices and ensure 85%+ test coverage."
                },
                {
                    "name": "qa_engineer",
                    "system_prompt": "You verify quality and run tests. Check for bugs, security issues, and ensure requirements are met."
                },
                {
                    "name": "tech_lead",
                    "system_prompt": "You make final decisions on completion or escalation. Determine if AI can handle it or if human expertise is needed."
                }
            ],
            max_handoffs=15,
            execution_timeout=600.0,
            repetitive_handoff_detection_window=6,
            repetitive_handoff_min_unique_agents=3
        )

        return {
            "success": result.status == "success",
            "final_result": result.result,
            "agents_involved": [node.node_id for node in result.node_history],
            "execution_time": result.execution_time
        }