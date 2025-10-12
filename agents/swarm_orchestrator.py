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
            system_prompt="""Requirements Agent - Extract structured requirements. Be concise.

Task: Analyze request, identify requirements, assess complexity (simple/medium/complex).

Output: JSON with task_type, requirements list, acceptance_criteria, complexity, edge_cases.

IMMEDIATELY handoff to context_agent when done:
handoff_to_agent(agent_name="context_agent", message="Requirements ready", context={"requirements": {...}})"""
        )

    def _create_context_agent(self) -> Agent:
        """Create context gathering agent with swarm coordination"""
        return Agent(
            name="context_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""Context Agent - Provide implementation context. Be brief.

Task: Identify what files/structure needed, where to add code, patterns to follow.

Output: Brief context analysis (file structure, approach, dependencies).

IMMEDIATELY handoff to builder_agent:
handoff_to_agent(agent_name="builder_agent", message="Context ready", context={"requirements": {...}, "codebase_context": {...}})"""
        )

    def _create_builder_agent(self) -> Agent:
        """Create implementation agent with swarm coordination"""
        return Agent(
            name="builder_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""Builder Agent - Write code + tests. Be efficient.

Task: Write production code with type hints, docstrings, and unit tests.

Output: Code block + test block. No long explanations.

IMMEDIATELY handoff to quality_agent:
handoff_to_agent(agent_name="quality_agent", message="Code ready", context={"implementation": "...", "tests": "..."})"""
        )

    def _create_quality_agent(self) -> Agent:
        """Create quality assurance agent with swarm coordination"""
        return Agent(
            name="quality_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""Quality Agent - Quick check. BE LENIENT.

Task: Verify code works, has tests, meets requirements. Score 0-100.

Scoring (SIMPLE tasks): Working code=85, +tests=90, +docstring=95. PASS if >=70.

Output: "PASS/FAIL, Score: X/100, Brief reason"

IMMEDIATELY handoff to escalation_agent:
handoff_to_agent(agent_name="escalation_agent", message="Quality check done", context={"quality_score": X, "status": "PASS"})"""
        )

    def _create_escalation_agent(self) -> Agent:
        """Create escalation decision agent with swarm coordination"""
        return Agent(
            name="escalation_agent",
            model=BaseAgentConfig.create_model(),
            system_prompt="""Escalation Agent - Final decision. Be concise. DO NOT ESCALATE 95% of tasks.

Task: Make COMPLETE/ESCALATE decision. Check quality score, review code.

Rules:
- Quality >=70? → COMPLETE (don't escalate)
- Simple tasks (algos, basic functions)? → COMPLETE
- Only escalate if MULTIPLE critical issues (score <50, security holes, unclear requirements)

Format:
DECISION: COMPLETE

Status: AI Implementation Successful
Payment: $0.05
Quality: X/100

```python
[code here]
```

DO NOT call handoff_to_agent. End swarm by not calling any tools."""
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

            # Extract final result text from escalation agent (last agent in sequence)
            final_result_str = ""

            # Try accessing through results dictionary first
            if hasattr(result, 'results') and 'escalation_agent' in result.results:
                escalation_result = result.results['escalation_agent']
                if hasattr(escalation_result, 'result'):
                    agent_result = escalation_result.result
                    # Extract clean text from agent message
                    if hasattr(agent_result, 'message') and isinstance(agent_result.message, dict):
                        content = agent_result.message.get('content', [])
                        # Content is a list of items, each with 'text' field
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict) and 'text' in item:
                                text_parts.append(item['text'])
                        final_result_str = '\n'.join(text_parts) if text_parts else ""

            # Fallback: try node_history if results dict didn't work
            if not final_result_str and hasattr(result, 'node_history') and result.node_history:
                last_node = result.node_history[-1]
                if hasattr(last_node, 'result') and hasattr(last_node.result, 'result'):
                    agent_result = last_node.result.result
                    if hasattr(agent_result, 'message') and isinstance(agent_result.message, dict):
                        content = agent_result.message.get('content', [])
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict) and 'text' in item:
                                text_parts.append(item['text'])
                        final_result_str = '\n'.join(text_parts) if text_parts else ""

            # Final fallback to string representation if extraction failed
            if not final_result_str:
                final_result_str = str(result)[:1000]  # Truncate to avoid massive output

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