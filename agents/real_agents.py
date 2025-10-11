"""
Real AI Agent Implementation using OpenAI/Anthropic APIs
Replaces the mock implementation with actual AI calls
"""

import openai
import anthropic
import os
import json
import time
from typing import Dict, Any, List
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class RealAgent:
    """Real AI agent using OpenAI or Anthropic API"""
    
    def __init__(self, name: str, system_prompt: str, model_type: str = "openai"):
        self.name = name
        self.system_prompt = system_prompt
        self.model_type = model_type
        
        # Initialize API clients
        if model_type == "openai":
            openai.api_key = os.getenv("OPENAI_API_KEY")
            self.model = "gpt-4"
        elif model_type == "anthropic":
            self.client = anthropic.Anthropic(
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
            self.model = "claude-3-sonnet-20240229"
    
    def __call__(self, prompt: str) -> Dict[str, Any]:
        """Execute agent with real AI API call"""
        start_time = time.time()
        
        try:
            if self.model_type == "openai":
                response = self._call_openai(prompt)
            else:
                response = self._call_anthropic(prompt)
                
            latency_ms = (time.time() - start_time) * 1000
            
            return {
                'message': response,
                'success': True,
                'tokens': len(response.split()) * 1.3,  # Rough estimate
                'latency_ms': latency_ms
            }
            
        except Exception as e:
            logger.error(f"Agent {self.name} failed: {e}")
            return {
                'message': f"Error: {str(e)}",
                'success': False,
                'tokens': 0,
                'latency_ms': 0
            }
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4000
        )
        return response.choices[0].message.content
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            temperature=0.3,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text


class RealSwarm:
    """Real swarm implementation with actual AI agents"""
    
    def __init__(self, agents: List[RealAgent] = None):
        self.agents = agents or []
        self.conversation_history = []
    
    def __call__(self, task: str, context: Dict = None) -> Dict[str, Any]:
        """Execute swarm with real agents"""
        return self.run(task, context)
    
    def run(self, task: str, context: Dict = None) -> Dict[str, Any]:
        """Run task through real agent sequence"""
        
        agent_sequence = []
        agent_outputs = {}
        current_context = f"Task: {task}"
        
        if context:
            current_context += f"\nContext: {json.dumps(context, indent=2)}"
        
        # Process through each agent
        for agent in self.agents:
            agent_sequence.append(agent.name)
            
            # Add conversation history to context
            if self.conversation_history:
                history_text = "\n".join([
                    f"{entry['agent']}: {entry['output'][:200]}..." 
                    for entry in self.conversation_history[-3:]  # Last 3 interactions
                ])
                current_context += f"\n\nPrevious agents output:\n{history_text}"
            
            # Execute agent
            result = agent(current_context)
            agent_outputs[agent.name] = result
            
            # Update conversation history
            self.conversation_history.append({
                'agent': agent.name,
                'output': result['message'],
                'success': result['success']
            })
            
            # Update context with agent output for next agent
            if result['success']:
                current_context += f"\n\n{agent.name} output:\n{result['message']}"
        
        # Get final result from last agent (typically BuilderAgent or QualityAgent)
        final_agent = self.agents[-1] if self.agents else None
        final_result = agent_outputs.get(final_agent.name if final_agent else 'unknown', {})
        
        # Determine if task is complete or needs escalation
        decision = self._make_decision(agent_outputs, task)
        
        return {
            'success': True,
            'agent_sequence': agent_sequence,
            'agent_outputs': agent_outputs,
            'final_result': final_result.get('message', ''),
            'final_decision': decision,
            'decision': decision,
            'code': self._extract_code(final_result.get('message', '')),
            'tokens_used': sum(output.get('tokens', 0) for output in agent_outputs.values()),
            'latency_ms': sum(output.get('latency_ms', 0) for output in agent_outputs.values()),
            'handoff_count': len(agent_sequence) - 1
        }
    
    def _extract_code(self, text: str) -> str:
        """Extract Python code from agent response"""
        import re
        
        # Look for code blocks
        code_pattern = r'```python\n(.*?)\n```'
        matches = re.findall(code_pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # If no code blocks, look for function definitions
        func_pattern = r'(def \w+.*?)(?=\n\n|\n#|\nclass|\Z)'
        func_matches = re.findall(func_pattern, text, re.DOTALL)
        
        if func_matches:
            return func_matches[0].strip()
        
        return text
    
    def _make_decision(self, agent_outputs: Dict, task: str) -> str:
        """Determine if task is complete or needs escalation"""
        
        # Check if any agent failed
        failed_agents = [name for name, output in agent_outputs.items() 
                        if not output.get('success', True)]
        
        if failed_agents:
            return "ESCALATE - Agent failures"
        
        # Check task complexity indicators
        complexity_indicators = [
            'database', 'microservice', 'kubernetes', 'distributed',
            'security audit', 'performance optimization', 'architecture'
        ]
        
        if any(indicator in task.lower() for indicator in complexity_indicators):
            return "ESCALATE - High complexity"
        
        return "COMPLETE"


class RealCodeCollabOrchestrator:
    """Real implementation of CodeCollab orchestrator"""
    
    def __init__(self, model_type: str = "openai"):
        """Initialize with real AI agents"""
        
        # Create real agents with specific prompts
        self.requirements_agent = RealAgent(
            name="RequirementsAgent",
            system_prompt="""You are a Requirements Analyst. Analyze development tasks and extract:
            1. Clear, structured requirements
            2. Acceptance criteria
            3. Edge cases to consider
            4. Technical constraints
            5. Complexity assessment (simple/medium/complex)
            
            Output should be structured and clear for the next agent.""",
            model_type=model_type
        )
        
        self.context_agent = RealAgent(
            name="ContextAgent", 
            system_prompt="""You are a Code Context Analyst. Based on requirements:
            1. Identify what type of code structure is needed
            2. Suggest appropriate design patterns
            3. Consider integration points
            4. Identify dependencies and imports needed
            5. Provide architectural guidance
            
            Focus on providing context for implementation.""",
            model_type=model_type
        )
        
        self.builder_agent = RealAgent(
            name="BuilderAgent",
            system_prompt="""You are a Code Builder. Write production-quality Python code that:
            1. Implements the requirements exactly
            2. Follows the architectural guidance from context
            3. Includes proper type hints
            4. Has comprehensive docstrings
            5. Includes example usage and basic tests
            6. Handles edge cases and errors
            
            Always wrap code in ```python blocks.""",
            model_type=model_type
        )
        
        self.quality_agent = RealAgent(
            name="QualityAgent",
            system_prompt="""You are a Quality Assurance Analyst. Review code for:
            1. Correctness and logic errors
            2. Code quality and best practices
            3. Test coverage adequacy
            4. Security considerations
            5. Performance implications
            
            Provide specific feedback and suggestions.""",
            model_type=model_type
        )
        
        self.escalation_agent = RealAgent(
            name="EscalationAgent",
            system_prompt="""You are an Escalation Decision Maker. Determine if:
            1. Task is completed successfully by AI agents
            2. Task needs human expert intervention
            3. More information is needed
            
            Respond with: COMPLETE, ESCALATE, or CLARIFICATION_NEEDED with reasoning.""",
            model_type=model_type
        )
        
        # Create swarm
        self.swarm = RealSwarm([
            self.requirements_agent,
            self.context_agent, 
            self.builder_agent,
            self.quality_agent,
            self.escalation_agent
        ])
    
    def process_task(self, task_description: str) -> Dict[str, Any]:
        """Process task with real AI agents"""
        logger.info(f"Processing task with real AI agents: {task_description[:100]}...")
        
        try:
            result = self.swarm(task_description)
            result["task_description"] = task_description
            return result
            
        except Exception as e:
            logger.error(f"Real agent processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "task_description": task_description
            }