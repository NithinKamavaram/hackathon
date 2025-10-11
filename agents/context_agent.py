"""
Context Agent - Provides codebase knowledge and context
"""

from .base_agent import BaseCodeCollabAgent
from typing import Dict, Any, List
import os


class ContextAgent(BaseCodeCollabAgent):
    """
    Agent responsible for understanding codebase structure,
    finding relevant code, and providing integration context.
    """

    SYSTEM_PROMPT = """You are a senior software architect and codebase expert for CodeCollab.

Your role is to understand the project structure and provide relevant context for implementation tasks.

For each task:

1. **Analyze Codebase Structure**
   - Identify relevant files and modules
   - Understand existing patterns and conventions
   - Map out dependencies

2. **Find Integration Points**
   - Where should new code be added?
   - What existing code needs modification?
   - What interfaces should be used?

3. **Identify Reusable Components**
   - What existing code can be reused?
   - What utilities are available?
   - What patterns should be followed?

4. **Assess Impact**
   - What components will be affected?
   - What tests need updating?
   - What documentation needs changes?

5. **Provide Context Document**
   Return a structured context report:
   ```json
   {
     "relevant_files": [
       {
         "path": "path/to/file.py",
         "purpose": "What this file does",
         "relevance": "Why it matters for this task"
       }
     ],
     "integration_points": [
       {
         "location": "specific location",
         "action": "what to do",
         "example": "code example if helpful"
       }
     ],
     "reusable_components": [
       {
         "name": "component name",
         "usage": "how to use it"
       }
     ],
     "patterns_to_follow": ["pattern 1", "pattern 2"],
     "affected_areas": ["area 1", "area 2"]
   }
   ```

Use file_manager tool to explore the codebase. Be specific and provide concrete examples."""

    def __init__(self):
        super().__init__(
            name="context_agent",
            system_prompt=self.SYSTEM_PROMPT,
            tools=[]
        )

    def gather_context(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gather relevant codebase context for implementation.

        Args:
            requirements: Structured requirements from RequirementsAgent

        Returns:
            Context document with relevant codebase information
        """
        task_summary = requirements.get("summary", "unknown task")
        task_type = requirements.get("type", "unknown")

        prompt = f"""Analyze the codebase and provide context for this task:

TASK TYPE: {task_type}
SUMMARY: {task_summary}
REQUIREMENTS: {requirements.get('requirements', [])}

Use the file_manager tool to explore relevant parts of the codebase.

Provide:
1. List of relevant files
2. Integration points
3. Reusable components
4. Patterns to follow
5. Affected areas

Return as structured JSON."""

        return self(prompt)