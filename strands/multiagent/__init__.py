"""Mock multiagent module for strands"""

class Swarm:
    def __init__(self, agents=None, handoff_config=None, max_iterations=5, **kwargs):
        self.agents = agents or []
        self.handoff_config = handoff_config
        self.max_iterations = max_iterations
        self.iteration_count = 0

    def __call__(self, task, context=None):
        """Make Swarm callable - redirects to run method"""
        return self.run(task, context)

    def run(self, task, context=None):
        """Mock swarm execution with simulated agent outputs"""
        self.iteration_count += 1

        # Simulate agent sequence
        agent_sequence = [
            "RequirementsAgent",
            "ContextAgent",
            "BuilderAgent",
            "QualityAgent",
            "EscalationAgent"
        ]

        # Generate appropriate mock code based on task
        code_result = self._generate_mock_code(task)

        # Simulate agent outputs
        agent_outputs = {
            "RequirementsAgent": {
                "response": f"Analyzed task: {task[:50]}... Extracted requirements: 1) Create function 2) Add error handling 3) Include tests",
                "handoff_message": "Requirements extracted, passing to context agent"
            },
            "ContextAgent": {
                "response": "Analyzed codebase context. No conflicts found. Following Python best practices.",
                "handoff_message": "Context gathered, ready for implementation"
            },
            "BuilderAgent": {
                "response": f"Generated code with type hints and docstrings. Tests included.",
                "handoff_message": "Code implementation complete, ready for quality check"
            },
            "QualityAgent": {
                "response": "Quality check passed. Tests run successfully. Code coverage: 100%",
                "handoff_message": "Quality verified, passing to escalation agent"
            },
            "EscalationAgent": {
                "response": "Task completed successfully by AI. No human escalation needed.",
                "handoff_message": "Task complete"
            }
        }

        # Determine if task is complex (for escalation simulation)
        complex_keywords = ['microservice', 'architecture', 'refactor', 'security', 'payment', 'api integration']
        is_complex = any(keyword in task.lower() for keyword in complex_keywords)

        final_decision = 'ESCALATE' if is_complex else 'COMPLETE'
        decision_msg = 'Task requires human expertise' if is_complex else 'Task completed successfully'

        # Mock successful execution
        return {
            'success': True,
            'agent_sequence': agent_sequence,
            'agent_outputs': agent_outputs,
            'final_result': code_result,
            'final_decision': final_decision,
            'decision': decision_msg,
            'code': code_result,
            'iterations': self.iteration_count,
            'tokens_used': 500 + len(task) * 2,
            'latency_ms': 2500 + len(agent_sequence) * 300,
            'handoff_count': len(agent_sequence) - 1
        }

    def _generate_mock_code(self, task):
        """Generate contextual mock code based on task"""
        task_lower = task.lower()
        
        if 'multiply' in task_lower or 'multiplication' in task_lower or 'product' in task_lower:
            return '''def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers together.

    Args:
        a: The first number to multiply
        b: The second number to multiply

    Returns:
        The product of a and b

    Examples:
        >>> multiply(2, 3)
        6
        >>> multiply(5, 4)
        20
        >>> multiply(-2, 3)
        -6
        >>> multiply(2.5, 4)
        10.0
    """
    return a * b

# Test the function
assert multiply(2, 3) == 6
assert multiply(5, 4) == 20
assert multiply(-2, 3) == -6
assert multiply(2.5, 4) == 10.0
assert multiply(0, 100) == 0
print("✅ All tests passed!")'''
        
        elif 'fibonacci' in task_lower:
            return '''def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.

    Args:
        n: The position in Fibonacci sequence (0-indexed)

    Returns:
        The nth Fibonacci number

    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(10)
        55
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Test the function
assert fibonacci(0) == 0
assert fibonacci(1) == 1
assert fibonacci(10) == 55
print("✅ All tests passed!")'''
        
        elif 'credit' in task_lower or 'luhn' in task_lower:
            return '''def validate_credit_card(card_number: str) -> bool:
    """
    Validate credit card number using Luhn algorithm.

    Args:
        card_number: Credit card number as string

    Returns:
        True if valid, False otherwise
    """
    # Remove spaces and hyphens
    card_number = card_number.replace(' ', '').replace('-', '')
    
    if not card_number.isdigit():
        return False
    
    # Luhn algorithm
    digits = [int(d) for d in card_number]
    checksum = 0
    
    for i in range(len(digits) - 2, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    
    return sum(digits) % 10 == 0

# Tests
assert validate_credit_card("4532015112830366")
assert not validate_credit_card("1234567812345678")
print("✅ All tests passed!")'''
        
        else:
            # Default example
            return '''def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together.

    Args:
        a: The first number to add
        b: The second number to add

    Returns:
        The sum of a and b

    Examples:
        >>> add_numbers(2, 3)
        5
        >>> add_numbers(-1, 1)
        0
    """
    return a + b

# Test the function
assert add_numbers(2, 3) == 5
assert add_numbers(-1, 1) == 0
assert add_numbers(0, 0) == 0
print("✅ All tests passed!")'''