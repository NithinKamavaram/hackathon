"""
Requirements Agent - Analyzes tasks and extracts structured requirements
"""

from .base_agent import BaseCodeCollabAgent
from .tools.complexity_tools import analyze_task_complexity, estimate_effort
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


class RequirementsAgent(BaseCodeCollabAgent):
    """
    Agent responsible for analyzing feature requests and bug reports,
    extracting clear requirements with acceptance criteria.
    """

    SYSTEM_PROMPT = """You are a senior business analyst and requirements engineer for CodeCollab.

Your role is to analyze feature requests and bug reports, then extract clear, structured requirements.

For each task you receive:

1. **Extract Core Requirements**
   - What needs to be built or fixed?
   - What are the acceptance criteria?
   - What are the constraints?

2. **Identify Edge Cases**
   - What unusual scenarios should be handled?
   - What error conditions need handling?
   - What boundary conditions exist?

3. **Determine Technical Constraints**
   - What technologies are involved?
   - What performance requirements exist?
   - What security considerations apply?

4. **Assess Complexity**
   - Use analyze_task_complexity tool
   - Determine if task is simple/medium/complex
   - Identify if human expertise will be needed

5. **Output Structured Requirements**
   Return a JSON structure with:
   ```json
   {
     "task_id": "unique_id",
     "type": "bug_fix" or "feature",
     "summary": "Brief description",
     "requirements": [
       {
         "id": "REQ-1",
         "description": "Specific requirement",
         "priority": "high/medium/low",
         "acceptance_criteria": ["criterion 1", "criterion 2"]
       }
     ],
     "edge_cases": ["case 1", "case 2"],
     "constraints": ["constraint 1", "constraint 2"],
     "complexity": {
       "level": "simple/medium/complex",
       "estimated_time_minutes": 30,
       "requires_human": false,
       "estimated_ai_payment": "0.05",
       "estimated_human_payment": "0"
     }
   }
   ```

Be thorough but concise. Focus on clarity and testability."""

    def __init__(self):
        super().__init__(
            name="requirements_agent",
            system_prompt=self.SYSTEM_PROMPT,
            tools=[analyze_task_complexity, estimate_effort]
        )

    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """
        Analyze task and extract structured requirements.

        Args:
            task_description: Raw task description from user

        Returns:
            Structured requirements document
        """
        prompt = f"""Analyze this development task and provide structured requirements:

TASK:
{task_description}

Use the analyze_task_complexity tool to assess complexity, then provide complete structured requirements in JSON format."""

        result = self(prompt)

        if result["success"]:
            try:
                # Try to parse JSON from response
                message = result["message"]

                # Check if message contains JSON
                if "```json" in message or "```" in message or "{" in message:
                    # Extract JSON from markdown code blocks if present
                    if "```json" in message:
                        json_start = message.find("```json") + 7
                        json_end = message.find("```", json_start)
                        json_str = message[json_start:json_end].strip()
                    elif "```" in message and "{" in message:
                        # Find the JSON object within code blocks
                        json_start = message.find("```") + 3
                        json_end = message.find("```", json_start)
                        json_str = message[json_start:json_end].strip()
                        # Remove any language identifier at the start
                        if json_str.startswith(("json", "JSON")):
                            json_str = json_str[4:].strip()
                    else:
                        # Try to find raw JSON in the message
                        json_start = message.find("{")
                        json_end = message.rfind("}") + 1
                        if json_start != -1 and json_end > json_start:
                            json_str = message[json_start:json_end]
                        else:
                            json_str = message

                    # Parse the JSON string
                    if isinstance(json_str, str):
                        requirements = json.loads(json_str)
                    else:
                        requirements = json_str  # Already a dict

                    return {
                        **result,
                        "requirements": requirements
                    }
                else:
                    # No JSON found, return the raw message
                    return result

            except (json.JSONDecodeError, TypeError) as e:
                # If JSON parsing fails, return raw message
                logger.debug(f"JSON parsing failed: {e}")
                return result

        return result