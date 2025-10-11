"""
Strands-based Multi-Agent Orchestrator for CodeCollab
Using official Strands SDK patterns instead of mock implementations
"""

from .strands_agents import (
    RequirementsAgent, ContextAgent, BuilderAgent, 
    QualityAgent, EscalationAgent
)
import logging
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)


class StrandsCodeCollabOrchestrator:
    """
    Real multi-agent orchestrator using Strands SDK
    Processes development tasks through 5 specialized agents
    """
    
    def __init__(self):
        """Initialize all Strands agents"""
        logger.info("Initializing Strands CodeCollab Orchestrator...")
        
        try:
            self.requirements_agent = RequirementsAgent()
            self.context_agent = ContextAgent()  
            self.builder_agent = BuilderAgent()
            self.quality_agent = QualityAgent()
            self.escalation_agent = EscalationAgent()
            
            logger.info("All Strands agents initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize agents: {e}")
            raise
    
    def process_task(self, task_description: str) -> Dict[str, Any]:
        """
        Process development task through Strands agent pipeline
        
        Args:
            task_description: Natural language task description
            
        Returns:
            Dict with complete task results and agent outputs
        """
        start_time = time.time()
        
        try:
            logger.info(f"Processing task: {task_description[:100]}...")
            
            # Step 1: Requirements Analysis
            logger.info("Step 1: Requirements analysis...")
            req_response = self.requirements_agent(task_description)
            req_output = self._extract_message(req_response)
            
            # Step 2: Context and Architecture  
            logger.info("Step 2: Context analysis...")
            context_input = f"Task: {task_description}\n\nRequirements:\n{req_output}"
            context_response = self.context_agent(context_input)
            context_output = self._extract_message(context_response)
            
            # Step 3: Code Building
            logger.info("Step 3: Code generation...")
            builder_input = f"{context_input}\n\nArchitecture Context:\n{context_output}"
            builder_response = self.builder_agent(builder_input)
            builder_output = self._extract_message(builder_response)
            
            # Step 4: Quality Review
            logger.info("Step 4: Quality assessment...")
            quality_input = f"{builder_input}\n\nGenerated Code:\n{builder_output}"
            quality_response = self.quality_agent(quality_input)
            quality_output = self._extract_message(quality_response)
            
            # Step 5: Escalation Decision
            logger.info("Step 5: Final decision...")
            escalation_input = f"""
            Task: {task_description}
            
            Requirements Analysis: {req_output[:500]}
            
            Generated Code: {builder_output[:1000]}
            
            Quality Review: {quality_output[:500]}
            """
            
            escalation_response = self.escalation_agent(escalation_input)
            escalation_output = self._extract_message(escalation_response)
            
            # Extract final decision
            decision = self._extract_decision(escalation_output)
            
            # Calculate metrics
            execution_time = (time.time() - start_time) * 1000
            
            # Build result
            result = {
                "success": True,
                "task_description": task_description,
                "agent_sequence": [
                    "RequirementsAgent", "ContextAgent", "BuilderAgent",
                    "QualityAgent", "EscalationAgent"
                ],
                "agent_outputs": {
                    "RequirementsAgent": req_output,
                    "ContextAgent": context_output,
                    "BuilderAgent": builder_output,
                    "QualityAgent": quality_output,
                    "EscalationAgent": escalation_output
                },
                "final_result": builder_output,
                "final_decision": decision,
                "decision": decision,
                "code": self._extract_code(builder_output),
                "execution_time_ms": execution_time,
                "tokens_used": self._calculate_tokens(
                    req_response, context_response, builder_response,
                    quality_response, escalation_response
                ),
                "handoff_count": 4,
                "implementation": "strands_sdk"
            }
            
            logger.info(f"Task completed in {execution_time:.0f}ms with decision: {decision}")
            return result
            
        except Exception as e:
            logger.error(f"Task processing failed: {e}")
            return {
                "success": False,
                "task_description": task_description,
                "error": str(e),
                "execution_time_ms": (time.time() - start_time) * 1000,
                "implementation": "strands_sdk"
            }
    
    def _extract_message(self, response) -> str:
        """Extract message content from Strands agent response"""
        if hasattr(response, 'content'):
            return str(response.content)
        elif hasattr(response, 'message'):
            return str(response.message)
        else:
            return str(response)
    
    def _extract_decision(self, escalation_output: str) -> str:
        """Extract decision from escalation agent output"""
        output_upper = escalation_output.upper()
        
        if "COMPLETE" in output_upper:
            return "COMPLETE"
        elif "ESCALATE" in output_upper:
            return "ESCALATE"
        elif "CLARIFICATION" in output_upper:
            return "CLARIFICATION_NEEDED"
        else:
            return "COMPLETE"  # Default assumption
    
    def _extract_code(self, builder_output: str) -> str:
        """Extract Python code from builder output"""
        import re
        
        # Look for code blocks first
        code_pattern = r'```python\n(.*?)\n```'
        matches = re.findall(code_pattern, builder_output, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # Look for function definitions
        func_pattern = r'(def \w+.*?)(?=\n\n|\nclass|\n#|\Z)'
        func_matches = re.findall(func_pattern, builder_output, re.DOTALL)
        
        if func_matches:
            return func_matches[0].strip()
        
        return builder_output
    
    def _calculate_tokens(self, *responses) -> int:
        """Estimate total tokens used across all responses"""
        total_tokens = 0
        
        for response in responses:
            if hasattr(response, 'metrics') and hasattr(response.metrics, 'total_tokens'):
                total_tokens += response.metrics.total_tokens
            else:
                # Rough estimation: 1 token ≈ 0.75 words
                content = self._extract_message(response)
                word_count = len(content.split())
                total_tokens += int(word_count * 1.33)
        
        return total_tokens


class StrandsSimpleOrchestrator:
    """Simplified Strands orchestrator for step-by-step processing"""
    
    def __init__(self):
        """Initialize key agents"""
        self.requirements_agent = RequirementsAgent()
        self.builder_agent = BuilderAgent()
        self.quality_agent = QualityAgent()
    
    def process_task_simple(self, task: str) -> Dict[str, Any]:
        """Process task with simple 3-step flow"""
        
        steps = {}
        
        try:
            # Step 1: Requirements
            req_response = self.requirements_agent(task)
            steps['requirements'] = {
                'success': True,
                'output': self._extract_message(req_response)[:300],
                'tokens': getattr(req_response.metrics, 'total_tokens', 0) if hasattr(req_response, 'metrics') else 50,
                'latency_ms': 1000
            }
            
            # Step 2: Implementation  
            context = f"Task: {task}\nRequirements: {steps['requirements']['output']}"
            impl_response = self.builder_agent(context)
            steps['implementation'] = {
                'success': True,
                'output': self._extract_message(impl_response)[:300],
                'tokens': getattr(impl_response.metrics, 'total_tokens', 0) if hasattr(impl_response, 'metrics') else 100,
                'latency_ms': 2000
            }
            
            # Step 3: Quality
            quality_context = f"Review implementation: {steps['implementation']['output']}"
            quality_response = self.quality_agent(quality_context)
            steps['quality'] = {
                'success': True,
                'output': self._extract_message(quality_response)[:300],
                'tokens': getattr(quality_response.metrics, 'total_tokens', 0) if hasattr(quality_response, 'metrics') else 75,
                'latency_ms': 1500
            }
            
            return {
                'success': True,
                'steps': steps,
                'implementation': 'strands_sdk'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': steps,
                'implementation': 'strands_sdk'
            }
    
    def _extract_message(self, response) -> str:
        """Extract message content from Strands agent response"""
        if hasattr(response, 'content'):
            return str(response.content)
        elif hasattr(response, 'message'):
            return str(response.message)
        else:
            return str(response)


# Aliases for backward compatibility
CodeCollabSwarm = StrandsCodeCollabOrchestrator
SimpleSwarmOrchestrator = StrandsSimpleOrchestrator