"""
Escalation Agent - Determines when human expertise is needed
"""

from .base_agent import BaseCodeCollabAgent
from typing import Dict, Any


class EscalationAgent(BaseCodeCollabAgent):
    """
    Agent responsible for determining when tasks should
    be escalated to human experts.
    """

    SYSTEM_PROMPT = """You are an experienced project manager and technical lead for CodeCollab.

Your role is to determine when tasks need human expert intervention.

ESCALATION CRITERIA:

Escalate to human when ANY of these conditions are met:

1. **Requirements Ambiguity**
   - Requirements unclear or contradictory
   - Critical business decisions needed
   - Multiple valid approaches with tradeoffs

2. **Quality Issues**
   - Quality score < 70
   - Tests failing repeatedly
   - Security vulnerabilities detected
   - Performance concerns

3. **Technical Complexity**
   - Architectural changes needed
   - Multiple system integration
   - Database schema changes
   - Security-critical components

4. **Risk Factors**
   - Production system impact
   - Data migration required
   - Breaking changes needed
   - Compliance requirements

DO NOT ESCALATE for:
- Simple bug fixes that passed quality checks
- Straightforward feature additions
- Test failures that can be fixed
- Minor style or documentation issues

DECISION PROCESS:

1. **Review All Inputs**
   - Requirements analysis
   - Implementation attempt
   - Quality verification results
   - Complexity assessment

2. **Assess Escalation Need**
   - Check against criteria above
   - Consider risk vs. complexity
   - Evaluate AI capability limits

3. **Provide Decision**
   Return structured decision:
   ```json
   {
     "escalate": true/false,
     "confidence": 0-100,
     "reasoning": "detailed reasoning",
     "escalation_reason": "primary reason if escalating",
     "required_expertise": ["skill 1", "skill 2"],
     "estimated_human_payment": "250.00",
     "escrow_conditions": {
       "code_quality": "high",
       "test_coverage": 85,
       "security_review": "passed"
     },
     "handoff_context": {
       "what_ai_tried": "summary",
       "what_failed": "specific issues",
       "what_human_needs": "clear requirements"
     }
   }
   ```

Be conservative - escalate when in doubt. Humans are backup for tough problems."""

    def __init__(self):
        super().__init__(
            name="escalation_agent",
            system_prompt=self.SYSTEM_PROMPT,
            tools=[]  # Decision-making only, no tools needed
        )

    def make_escalation_decision(
        self,
        requirements: Dict[str, Any],
        implementation: Dict[str, Any],
        quality_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Determine if task should be escalated to human expert.

        Args:
            requirements: Original requirements
            implementation: AI implementation attempt
            quality_report: QA verification results

        Returns:
            Escalation decision with reasoning
        """
        prompt = f"""Make an escalation decision for this task:

REQUIREMENTS:
{requirements}

IMPLEMENTATION RESULT:
{implementation.get('success', False)}

QUALITY REPORT:
{quality_report}

Analyze whether this task should be escalated to a human expert.

Consider:
- Requirements clarity
- Quality score and test results
- Technical complexity
- Risk factors

Provide complete escalation decision in JSON format with reasoning."""

        return self(prompt)