"""
Real LLM Implementation using AWS Bedrock
Bypasses mocks to use actual Claude models for code generation
"""

import boto3
import json
import time
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class RealBedrockAgent:
    """Real agent implementation using AWS Bedrock Claude models"""
    
    def __init__(self, name: str, system_prompt: str, model_id: str = None):
        self.name = name
        self.system_prompt = system_prompt
        self.model_id = model_id or "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
        
        # Initialize Bedrock client
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        logger.info(f"Initialized real Bedrock agent: {name}")
    
    def __call__(self, user_prompt: str) -> Dict[str, Any]:
        """Execute with real Claude model via Bedrock"""
        start_time = time.time()
        
        try:
            # Prepare the messages for Claude
            messages = [
                {
                    "role": "user", 
                    "content": user_prompt
                }
            ]
            
            # Prepare request body
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "temperature": 0.3,
                "system": self.system_prompt,
                "messages": messages
            }
            
            # Make the API call to Bedrock
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body),
                contentType="application/json"
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            content = response_body['content'][0]['text']
            
            # Calculate metrics
            execution_time = (time.time() - start_time) * 1000
            
            # Estimate token usage (rough approximation)
            input_tokens = len(user_prompt.split()) * 1.3
            output_tokens = len(content.split()) * 1.3
            total_tokens = int(input_tokens + output_tokens)
            
            return {
                'success': True,
                'message': content,
                'content': content,  # For compatibility
                'tokens': total_tokens,
                'latency_ms': execution_time,
                'model': self.model_id,
                'agent': self.name
            }
            
        except Exception as e:
            logger.error(f"Bedrock call failed for {self.name}: {e}")
            return {
                'success': False,
                'message': f"Error: {str(e)}",
                'content': f"Error: {str(e)}",
                'tokens': 0,
                'latency_ms': (time.time() - start_time) * 1000,
                'agent': self.name
            }


class RealLLMOrchestrator:
    """Real orchestrator using actual LLM agents via Bedrock"""
    
    def __init__(self):
        """Initialize real LLM agents"""
        
        self.requirements_agent = RealBedrockAgent(
            name="RequirementsAgent",
            system_prompt="""You are a Requirements Analyst specialized in software development.
            
Analyze development tasks and provide:
1. Clear, numbered requirements
2. Acceptance criteria 
3. Edge cases to consider
4. Technical constraints
5. Complexity assessment (Simple/Medium/Complex)

Be concise but thorough. Focus on what needs to be built."""
        )
        
        self.context_agent = RealBedrockAgent(
            name="ContextAgent",
            system_prompt="""You are a Software Architecture Consultant.
            
Based on requirements, provide:
1. Appropriate code structure and patterns
2. Dependencies and imports needed
3. Design considerations
4. Integration guidance
5. Best practices for the task type

Keep recommendations practical and implementable."""
        )
        
        self.builder_agent = RealBedrockAgent(
            name="BuilderAgent", 
            system_prompt="""You are an Expert Python Developer.
            
Write production-quality Python code that:
1. Implements requirements exactly
2. Uses proper type hints and docstrings  
3. Includes comprehensive error handling
4. Has test cases and examples
5. Follows Python best practices (PEP 8)

Always wrap code in ```python blocks. Include meaningful variable names and comments."""
        )
        
        self.quality_agent = RealBedrockAgent(
            name="QualityAgent",
            system_prompt="""You are a Code Quality Reviewer.
            
Review code for:
1. Correctness and logic errors
2. Requirement compliance
3. Code quality and readability
4. Error handling adequacy
5. Test coverage

Provide specific, actionable feedback. Highlight any issues or improvements needed."""
        )
        
        self.escalation_agent = RealBedrockAgent(
            name="EscalationAgent",
            system_prompt="""You are a Task Completion Decision Maker.
            
Determine if the task is:
- COMPLETE: Successfully implemented and tested
- ESCALATE: Too complex or has critical issues
- CLARIFICATION_NEEDED: Requirements unclear

Consider code quality, complexity, and risk. Provide clear reasoning for your decision."""
        )
    
    def process_task(self, task_description: str) -> Dict[str, Any]:
        """Process task with real LLM agents"""
        start_time = time.time()
        
        try:
            logger.info(f"Processing with REAL LLMs: {task_description[:100]}...")
            
            # Step 1: Requirements Analysis
            print("🔄 Step 1: Analyzing requirements with real LLM...")
            req_response = self.requirements_agent(task_description)
            
            if not req_response['success']:
                raise Exception(f"Requirements analysis failed: {req_response['message']}")
            
            # Step 2: Context Analysis
            print("🔄 Step 2: Analyzing context with real LLM...")
            context_input = f"Task: {task_description}\n\nRequirements Analysis:\n{req_response['content']}"
            context_response = self.context_agent(context_input)
            
            if not context_response['success']:
                raise Exception(f"Context analysis failed: {context_response['message']}")
            
            # Step 3: Code Building  
            print("🔄 Step 3: Generating code with real LLM...")
            builder_input = f"""Task: {task_description}

Requirements:
{req_response['content']}

Architecture Context:
{context_response['content']}

Please generate complete, working Python code that fulfills these requirements."""
            
            builder_response = self.builder_agent(builder_input)
            
            if not builder_response['success']:
                raise Exception(f"Code generation failed: {builder_response['message']}")
            
            # Step 4: Quality Review
            print("🔄 Step 4: Reviewing quality with real LLM...")
            quality_input = f"""Please review this implementation:

Original Task: {task_description}

Generated Code:
{builder_response['content']}

Assess code quality, correctness, and requirement compliance."""
            
            quality_response = self.quality_agent(quality_input)
            
            # Step 5: Final Decision
            print("🔄 Step 5: Making final decision with real LLM...")
            escalation_input = f"""Review this completed task:

Task: {task_description}
Generated Code: {builder_response['content'][:1000]}
Quality Review: {quality_response['content'][:500]}

Decision: COMPLETE, ESCALATE, or CLARIFICATION_NEEDED with reasoning."""
            
            escalation_response = self.escalation_agent(escalation_input)
            
            # Extract decision
            decision_text = escalation_response['content'].upper()
            if 'COMPLETE' in decision_text:
                decision = 'COMPLETE'
            elif 'ESCALATE' in decision_text:
                decision = 'ESCALATE' 
            elif 'CLARIFICATION' in decision_text:
                decision = 'CLARIFICATION_NEEDED'
            else:
                decision = 'COMPLETE'  # Default
            
            # Extract code
            code = self._extract_code(builder_response['content'])
            
            # Calculate total metrics
            total_tokens = sum([
                req_response.get('tokens', 0),
                context_response.get('tokens', 0), 
                builder_response.get('tokens', 0),
                quality_response.get('tokens', 0),
                escalation_response.get('tokens', 0)
            ])
            
            execution_time = (time.time() - start_time) * 1000
            
            return {
                'success': True,
                'task_description': task_description,
                'agent_sequence': ['RequirementsAgent', 'ContextAgent', 'BuilderAgent', 'QualityAgent', 'EscalationAgent'],
                'agent_outputs': {
                    'RequirementsAgent': req_response['content'],
                    'ContextAgent': context_response['content'],
                    'BuilderAgent': builder_response['content'], 
                    'QualityAgent': quality_response['content'],
                    'EscalationAgent': escalation_response['content']
                },
                'final_result': builder_response['content'],
                'code': code,
                'final_decision': decision,
                'decision': decision,
                'tokens_used': total_tokens,
                'execution_time_ms': execution_time,
                'handoff_count': 4,
                'implementation': 'real_llm_bedrock'
            }
            
        except Exception as e:
            logger.error(f"Real LLM processing failed: {e}")
            return {
                'success': False,
                'task_description': task_description,
                'error': str(e),
                'execution_time_ms': (time.time() - start_time) * 1000,
                'implementation': 'real_llm_bedrock'
            }
    
    def _extract_code(self, text: str) -> str:
        """Extract Python code from LLM response"""
        import re
        
        # Look for ```python code blocks
        pattern = r'```python\n(.*?)\n```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # Look for ```py blocks
        pattern = r'```py\n(.*?)\n```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # Look for ``` blocks (generic)
        pattern = r'```\n(.*?)\n```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            # Check if it looks like Python code
            code = matches[0].strip()
            if 'def ' in code or 'class ' in code or 'import ' in code:
                return code
        
        # Look for function definitions without blocks
        pattern = r'(def \w+.*?)(?=\n\n|\nclass|\n#|\Z)'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        return text