"""
Real Swarm Orchestrator - Uses actual AI APIs instead of mocks
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv
from .real_agents import RealCodeCollabOrchestrator
import logging

# Load environment variables
load_dotenv()
load_dotenv('.env.real')  # Load real implementation env

logger = logging.getLogger(__name__)


class CodeCollabSwarmReal:
    """
    Real swarm orchestrator using OpenAI/Anthropic APIs
    """

    def __init__(self, ai_provider: str = None):
        """Initialize with real AI agents"""
        
        # Determine AI provider
        self.ai_provider = ai_provider or os.getenv('PREFERRED_AI_PROVIDER', 'openai')
        
        # Validate API keys
        if self.ai_provider == 'openai':
            if not os.getenv('OPENAI_API_KEY'):
                raise ValueError("OPENAI_API_KEY not found in environment")
        elif self.ai_provider == 'anthropic':
            if not os.getenv('ANTHROPIC_API_KEY'):
                raise ValueError("ANTHROPIC_API_KEY not found in environment")
        else:
            raise ValueError(f"Unsupported AI provider: {self.ai_provider}")
        
        # Initialize real orchestrator
        self.orchestrator = RealCodeCollabOrchestrator(model_type=self.ai_provider)
        
        logger.info(f"Real CodeCollab Swarm initialized with {self.ai_provider}")

    def process_task(self, task_description: str) -> Dict[str, Any]:
        """
        Process task using real AI agents.

        Args:
            task_description: Development task description

        Returns:
            Real AI agent execution result
        """
        logger.info(f"Processing task with real {self.ai_provider} agents: {task_description[:100]}...")

        try:
            result = self.orchestrator.process_task(task_description)
            
            # Ensure all expected fields are present
            if not isinstance(result, dict):
                result = {"success": False, "error": "Invalid result format"}
            
            # Add metadata
            result["ai_provider"] = self.ai_provider
            result["implementation"] = "real"
            
            return result

        except Exception as e:
            logger.error(f"Real swarm processing failed: {e}", exc_info=True)
            return {
                "success": False,
                "task_description": task_description,
                "error": str(e),
                "ai_provider": self.ai_provider,
                "implementation": "real"
            }


# For backwards compatibility, alias the real implementation
CodeCollabSwarm = CodeCollabSwarmReal


class SimpleSwarmOrchestratorReal:
    """
    Simplified real orchestrator for step-by-step processing
    """

    def __init__(self, ai_provider: str = None):
        """Initialize simplified real orchestrator"""
        self.ai_provider = ai_provider or os.getenv('PREFERRED_AI_PROVIDER', 'openai')
        self.orchestrator = RealCodeCollabOrchestrator(model_type=self.ai_provider)

    def process_task_simple(self, task: str) -> Dict[str, Any]:
        """Process task with step-by-step real AI execution"""
        
        steps = {}
        
        try:
            # Step 1: Requirements Analysis
            req_result = self.orchestrator.requirements_agent(task)
            steps['requirements'] = {
                'success': req_result.get('success', True),
                'output': req_result.get('message', ''),
                'tokens': req_result.get('tokens', 0),
                'latency_ms': req_result.get('latency_ms', 0)
            }
            
            # Step 2: Implementation (Builder)
            context = f"Task: {task}\nRequirements: {req_result.get('message', '')}"
            impl_result = self.orchestrator.builder_agent(context)
            steps['implementation'] = {
                'success': impl_result.get('success', True),
                'output': impl_result.get('message', ''),
                'tokens': impl_result.get('tokens', 0),
                'latency_ms': impl_result.get('latency_ms', 0)
            }
            
            # Step 3: Quality Check
            quality_context = f"Review this implementation:\n{impl_result.get('message', '')}"
            quality_result = self.orchestrator.quality_agent(quality_context)
            steps['quality'] = {
                'success': quality_result.get('success', True),
                'output': quality_result.get('message', ''),
                'tokens': quality_result.get('tokens', 0),
                'latency_ms': quality_result.get('latency_ms', 0)
            }
            
            return {
                'success': True,
                'steps': steps,
                'ai_provider': self.ai_provider,
                'implementation': 'real'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'steps': steps,
                'ai_provider': self.ai_provider,
                'implementation': 'real'
            }


# Alias for compatibility
SimpleSwarmOrchestrator = SimpleSwarmOrchestratorReal