"""
CodeCollab Swarm Orchestrator - Uses Swarm Intelligence Pattern
"""

from strands import Agent
from strands.multiagent import Swarm
from strands_tools import swarm as swarm_tool
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

        # Create the swarm with proper configuration
        self.swarm = Swarm(
            self.agents,  # Pass agents as first positional argument
            max_handoffs=20,
            max_iterations=20,
            execution_timeout=900.0,  # 15 minutes
            node_timeout=300.0,       # 5 minutes per agent
            repetitive_handoff_detection_window=8,
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
2. Analyze the codebase to find relevant files and patterns
3. Identify integration points and reusable components
4. Map dependencies and affected areas
5. Provide implementation context

When to handoff:
- After gathering context, handoff to builder_agent with context + requirements
- If no implementation is needed (documentation only), handoff to quality_agent
- If the codebase is too complex or missing, note for escalation_agent

What to analyze:
- Relevant files and their purposes
- Where new code should be added
- Existing patterns to follow
- Components that can be reused
- Areas that will be affected

Use handoff_to_agent to transfer to builder_agent after context gathering:
handoff_to_agent(
    agent_name="builder_agent",
    message="Context gathered. Please implement the solution based on requirements and context.",
    context={"requirements": <requirements>, "codebase_context": <your_context_analysis>}
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
3. Run tests and check coverage (target: 85%+)
4. Review code quality and patterns
5. Check for security vulnerabilities
6. Assess overall quality score

When to handoff:
- If quality PASSES (score >= 70), handoff to escalation_agent for final decision
- If quality FAILS but fixable, handoff back to builder_agent with specific feedback
- If security issues found, immediately handoff to escalation_agent
- Maximum 2 attempts with builder_agent before escalating

Quality criteria:
- All requirements met
- Tests passing with good coverage
- No critical security issues
- Clean, maintainable code
- Proper error handling

Output format:
Provide quality report with:
- Pass/fail status
- Quality score (0-100)
- Test results
- Security assessment
- Specific feedback

Use handoff_to_agent based on quality results:
If passed:
handoff_to_agent(
    agent_name="escalation_agent",
    message="Quality verification passed. Please make final escalation decision.",
    context={"quality_report": <your_report>, "quality_score": <score>}
)

If failed (first attempt):
handoff_to_agent(
    agent_name="builder_agent",
    message="Quality check failed. Please fix these issues.",
    context={"issues": <specific_issues>, "suggestions": <how_to_fix>}
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

Escalation criteria - Escalate if ANY are true:
- Quality score < 70
- Security vulnerabilities detected
- Architectural changes needed
- Requirements unclear after analysis
- Multiple failed quality attempts
- Task complexity marked as "complex" with risk factors

DO NOT escalate for:
- Simple bugs that passed quality
- Straightforward features with good test coverage
- Minor style issues

Decision process:
1. Review all agent contributions
2. Check quality score and test results
3. Assess technical complexity
4. Evaluate risk factors
5. Make escalation decision

If NOT escalating (AI complete):
- Mark task as complete
- Specify micropayment amount ($0.01-$0.10)
- Use complete_swarm_task with final solution

If escalating to human:
- Prepare complete handoff context
- Specify escrow amount ($10-$250)
- Detail what AI attempted
- Explain what human needs to do
- Use complete_swarm_task with escalation details

Use complete_swarm_task to finalize:
complete_swarm_task(
    result={
        "status": "completed" or "escalated",
        "payment": {"type": "micropayment" or "escrow", "amount": <amount>},
        "solution": <final_code_if_completed>,
        "escalation_context": <context_if_escalated>
    }
)"""
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
            
            # Try to parse deliverables from final result
            if "code:" in final_result_str.lower():
                # Attempt to extract code sections
                import re
                code_match = re.search(r'```python\n(.*?)```', final_result_str, re.DOTALL)
                if code_match:
                    deliverables['code'] = code_match.group(1).strip()
            
            # Extract shared knowledge if available
            shared_knowledge = self._extract_shared_knowledge(result) if hasattr(result, 'node_history') else {}

            # Build response
            return {
                "success": result.status == "success" if hasattr(result, 'status') else True,
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
                "shared_knowledge": shared_knowledge
            }

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