"""
Builder Agent - Writes production-quality code
"""

from .base_agent import BaseCodeCollabAgent
from .tools.code_tools import analyze_code_complexity, find_code_patterns
from typing import Dict, Any


class BuilderAgent(BaseCodeCollabAgent):
    """
    Agent responsible for implementing features and fixing bugs
    with production-quality code.
    """

    SYSTEM_PROMPT = """You are a senior software engineer for CodeCollab specializing in writing production-quality code.

Your role is to implement features and fix bugs following best practices.

For each implementation task:

1. **Understand Requirements**
   - Review requirements document
   - Understand acceptance criteria
   - Consider edge cases

2. **Review Context**
   - Study relevant existing code
   - Follow project patterns
   - Use reusable components

3. **Write Quality Code**
   - Clear, readable code
   - Proper error handling
   - Comprehensive docstrings
   - Type hints where appropriate
   - Follow SOLID principles

4. **Include Tests**
   - Unit tests for all functions
   - Test edge cases
   - Test error conditions
   - Aim for 85%+ coverage

5. **Document Changes**
   - Clear comments
   - Update docstrings
   - Note any assumptions

6. **Request Payment**
   - After successful implementation
   - Use execute_payment tool
   - Include complexity level

CRITICAL RULES:
- Always include error handling
- Always write tests
- Always add docstrings
- Never use unsafe operations (eval, exec) without validation
- Follow the project's existing code style

Output your implementation with:
1. Source code
2. Tests
3. Documentation
4. Brief explanation of approach"""

    def __init__(self):
        super().__init__(
            name="builder_agent",
            system_prompt=self.SYSTEM_PROMPT,
            tools=[
                analyze_code_complexity,
                find_code_patterns
            ]
        )

    def implement_solution(
        self,
        requirements: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Implement solution based on requirements and context.

        Args:
            requirements: Structured requirements
            context: Codebase context

        Returns:
            Implementation including code, tests, and documentation
        """
        prompt = f"""Implement a solution for this task:

REQUIREMENTS:
{requirements}

CONTEXT:
{context}

Provide:
1. Complete source code implementation
2. Comprehensive unit tests
3. Docstrings and comments
4. Brief explanation of your approach

Use python_repl to test your code as you write it.
Use analyze_code_complexity to verify quality.

Return the implementation in this structure:
```
SOURCE CODE:
[your implementation]

TESTS:
[test code]

DOCUMENTATION:
[docstrings and usage examples]

EXPLANATION:
[brief explanation of approach and decisions]
```"""

        return self(prompt)