"""
Quality Agent - Validates code quality and correctness
"""

from .base_agent import BaseCodeCollabAgent
from .tools.test_tools import run_tests, calculate_coverage, lint_code
from .tools.code_tools import analyze_code_complexity, detect_security_issues
from typing import Dict, Any


class QualityAgent(BaseCodeCollabAgent):
    """
    Agent responsible for quality assurance, testing,
    and validation of implementations.
    """

    SYSTEM_PROMPT = """You are a senior QA engineer and code reviewer for CodeCollab.

Your role is to verify that implementations meet quality standards and requirements.

For each review:

1. **Verify Requirements Met**
   - Check all requirements addressed
   - Verify acceptance criteria satisfied
   - Confirm edge cases handled

2. **Run Tests**
   - Execute all unit tests
   - Verify test coverage (target: 85%+)
   - Check tests are meaningful

3. **Code Quality Review**
   - Check code complexity
   - Verify error handling
   - Ensure proper documentation
   - Review code patterns

4. **Security Check**
   - Scan for vulnerabilities
   - Check input validation
   - Verify safe operations

5. **Performance Check**
   - Identify potential bottlenecks
   - Check algorithm efficiency
   - Review resource usage

6. **Provide Verification Report**
   Return structured quality report:
   ```json
   {
     "passed": true/false,
     "quality_score": 0-100,
     "test_results": {
       "passed": 10,
       "failed": 0,
       "coverage": 92.5
     },
     "code_quality": {
       "complexity": "simple/medium/complex",
       "issues": []
     },
     "security": {
       "high_issues": [],
       "medium_issues": [],
       "low_issues": []
     },
     "requirements_met": true/false,
     "feedback": [
       "specific feedback items"
     ],
     "recommendation": "approve/revise/escalate"
   }
   ```

Be thorough but constructive. Provide specific, actionable feedback."""

    def __init__(self):
        super().__init__(
            name="quality_agent",
            system_prompt=self.SYSTEM_PROMPT,
            tools=[
                run_tests,
                calculate_coverage,
                lint_code,
                analyze_code_complexity,
                detect_security_issues
            ]
        )

    def verify_implementation(
        self,
        requirements: Dict[str, Any],
        implementation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Verify implementation meets quality standards.

        Args:
            requirements: Original requirements
            implementation: Code from BuilderAgent

        Returns:
            Quality verification report
        """
        # Extract code from implementation
        impl_message = implementation.get("message", "")

        prompt = f"""Review this implementation for quality and correctness:

ORIGINAL REQUIREMENTS:
{requirements}

IMPLEMENTATION:
{impl_message}

Perform complete quality assurance:
1. Use run_tests to execute tests
2. Use calculate_coverage to check coverage
3. Use lint_code for style issues
4. Use analyze_code_complexity for quality metrics
5. Use detect_security_issues for vulnerabilities

Verify all requirements are met and provide a complete quality report in JSON format."""

        return self(prompt)