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
from .swarm_orchestrator import CodeCollabSwarm, CodeCollabSwarmTool

__all__ = [
    'RequirementsAgent',
    'ContextAgent',
    'BuilderAgent',
    'QualityAgent',
    'EscalationAgent',
    'CodeCollabOrchestrator',
    'CodeCollabSwarm',
    'CodeCollabSwarmTool'
]

__version__ = '2.0.0'  # Updated to reflect Swarm pattern implementation