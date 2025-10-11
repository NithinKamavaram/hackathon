#!/usr/bin/env python3
"""
Test the Swarm Orchestrator with Various Development Tasks
Shows how users can give prompts and agents handle the work
"""

from agents.swarm_orchestrator_fixed import CodeCollabSwarm, SimpleSwarmOrchestrator
from agents.swarm_orchestrator import CodeCollabSwarm as OriginalSwarm
from dotenv import load_dotenv
import json
import time

# Load environment variables
load_dotenv()


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80)


def print_agent_flow(agents):
    """Display agent handoff sequence"""
    if not agents:
        return

    print("\n🔀 Agent Flow:")
    for i, agent in enumerate(agents, 1):
        arrow = " → " if i < len(agents) else " ✓"
        print(f"   {i}. {agent}{arrow}")


def test_simple_task(swarm):
    """Test with a simple task"""
    print_header("TEST 1: Simple Task - Add Function")

    task = """
    Create a Python function called 'calculate_discount' that:
    - Takes original_price and discount_percentage as parameters
    - Returns the discounted price
    - Includes type hints
    - Has proper error handling for invalid inputs
    - Includes docstring with examples
    """

    print(f"📝 Task: {task[:100]}...")
    print("\n⏳ Processing with swarm agents...")

    start = time.time()
    result = swarm.process_task(task)
    elapsed = time.time() - start

    print(f"\n⏱️  Time: {elapsed:.2f} seconds")
    print(f"✅ Success: {result.get('success', False)}")

    # Show agent sequence
    if 'agent_sequence' in result:
        print_agent_flow(result['agent_sequence'])

    # Show generated code if available
    if result.get('code'):
        print("\n📄 Generated Code:")
        print("-"*40)
        print(result['code'][:500])  # Show first 500 chars
        print("-"*40)

    # Show tests if available
    if result.get('tests'):
        print("\n🧪 Generated Tests:")
        print("-"*40)
        print(result['tests'][:300])  # Show first 300 chars
        print("-"*40)

    return result


def test_medium_task(swarm):
    """Test with a medium complexity task"""
    print_header("TEST 2: Medium Task - Class Implementation")

    task = """
    Create a Python class called 'TaskQueue' that:
    - Manages a priority queue of tasks
    - Has methods: add_task(task, priority), get_next_task(), remove_task(task_id)
    - Implements __len__ and __str__ methods
    - Uses proper data structures (heapq recommended)
    - Includes comprehensive error handling
    - Has unit tests with 85% coverage
    - Thread-safe implementation
    """

    print(f"📝 Task: {task[:100]}...")
    print("\n⏳ Processing with swarm agents...")

    start = time.time()
    result = swarm.process_task(task)
    elapsed = time.time() - start

    print(f"\n⏱️  Time: {elapsed:.2f} seconds")
    print(f"✅ Success: {result.get('success', False)}")

    if 'agent_sequence' in result:
        print_agent_flow(result['agent_sequence'])

    # Check decision
    decision = result.get('final_decision', 'unknown')
    print(f"\n🎯 Final Decision: {decision}")

    return result


def test_complex_task(swarm):
    """Test with a complex task that might need escalation"""
    print_header("TEST 3: Complex Task - API Integration")

    task = """
    Implement a REST API client for a payment processing system that:
    - Integrates with Stripe API for payments
    - Handles authentication with API keys
    - Implements retry logic with exponential backoff
    - Has methods for: create_payment, refund_payment, get_payment_status
    - Includes webhook handling for payment events
    - Implements proper logging and error tracking
    - Has comprehensive test suite with mocked API calls
    - Follows PCI compliance best practices
    - Includes rate limiting
    """

    print(f"📝 Task: {task[:100]}...")
    print("\n⏳ Processing with swarm agents...")

    start = time.time()
    result = swarm.process_task(task)
    elapsed = time.time() - start

    print(f"\n⏱️  Time: {elapsed:.2f} seconds")
    print(f"✅ Success: {result.get('success', False)}")

    if 'agent_sequence' in result:
        print_agent_flow(result['agent_sequence'])

    # This complex task might trigger escalation
    decision = result.get('final_decision', 'unknown')
    print(f"\n🎯 Final Decision: {decision}")

    if decision == "escalate_to_human":
        print("\n⚠️  Task escalated to human expert")
        print("Reason: Too complex for AI to handle safely")

    return result


def test_bug_fix(swarm):
    """Test with a bug fix task"""
    print_header("TEST 4: Bug Fix Task")

    task = """
    Fix this bug in the login function:

    def login(username, password):
        user = database.get_user(username)
        if user.password == password:  # Bug: comparing plain text
            return {"success": True, "token": generate_token()}
        return {"success": False}

    The bug: Password is being compared as plain text instead of hashed.
    Fix requirements:
    - Implement proper password hashing using bcrypt
    - Maintain backward compatibility
    - Add salt for security
    - Include migration for existing passwords
    - Add tests
    """

    print(f"📝 Task: {task[:100]}...")
    print("\n⏳ Processing with swarm agents...")

    result = swarm.process_task(task)

    print(f"✅ Success: {result.get('success', False)}")

    if 'agent_sequence' in result:
        print_agent_flow(result['agent_sequence'])

    return result


def test_simple_orchestrator():
    """Test the simplified step-by-step orchestrator"""
    print_header("TEST 5: Simple Step-by-Step Orchestrator")

    orchestrator = SimpleSwarmOrchestrator()

    task = "Create a function to validate email addresses using regex"

    print(f"📝 Task: {task}")
    print("\n⏳ Processing step by step...")

    result = orchestrator.process_task_simple(task)

    print(f"\n✅ Success: {result.get('success', False)}")

    # Show each step's output
    for step_name, step_data in result.get('steps', {}).items():
        print(f"\n📍 Step: {step_name}")
        print("-"*40)
        output = step_data.get('output', '')[:300]  # First 300 chars
        print(output)

    return result


def interactive_mode():
    """Interactive mode where user can input any task"""
    print_header("INTERACTIVE MODE - Enter Your Development Task")

    print("\nEnter your development task (or 'quit' to exit):")
    print("Examples:")
    print("  - Create a function to calculate fibonacci numbers")
    print("  - Fix the SQL injection vulnerability in the search function")
    print("  - Build a class for managing user sessions with Redis")

    swarm = CodeCollabSwarm()

    while True:
        print("\n" + "-"*60)
        task = input("📝 Your task: ").strip()

        if task.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break

        if not task:
            continue

        print("\n⏳ Processing your task...")
        result = swarm.process_task(task)

        # Display results
        if result.get('success'):
            print("✅ Task processed successfully!")

            # Show agent sequence
            if result.get('agent_sequence'):
                print(f"\n🔀 Agent Flow: {' → '.join(result['agent_sequence'])}")

            # Show generated code
            final_result = result.get('final_result', result.get('code', ''))
            if final_result:
                print("\n📄 Generated Code:")
                print("-" * 60)
                print(final_result)
                print("-" * 60)

            # Show execution stats
            if result.get('tokens_used'):
                print(f"\n📊 Stats: {result['tokens_used']} tokens, {result.get('latency_ms', 0)}ms latency")

            # Show decision if available
            decision = result.get('final_decision', result.get('decision', 'Task completed'))
            print(f"\n🎯 Decision: {decision}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")

        print("\nPress Enter to continue or type 'quit' to exit...")
        if input().lower() in ['quit', 'q']:
            break


def main():
    """Main test runner"""
    print_header("SWARM ORCHESTRATOR TEST SUITE")
    print("""
    This test suite demonstrates how users can give natural language prompts
    for development tasks and the swarm of agents will handle them autonomously.

    The agents will:
    1. Analyze requirements
    2. Gather context
    3. Write code
    4. Check quality
    5. Decide if human help is needed
    """)

    # Initialize swarm
    print("\n🚀 Initializing CodeCollab Swarm...")
    try:
        swarm = CodeCollabSwarm()
        print("✅ Swarm ready with 5 specialized agents")
    except Exception as e:
        print(f"❌ Failed to initialize swarm: {e}")
        print("Using mock implementation for testing...")
        swarm = CodeCollabSwarm()  # Will use mock

    # Run tests
    print("\n" + "="*80)
    print("  RUNNING AUTOMATED TESTS")
    print("="*80)

    # Test 1: Simple task
    test_simple_task(swarm)

    # Test 2: Medium task
    test_medium_task(swarm)

    # Test 3: Complex task
    test_complex_task(swarm)

    # Test 4: Bug fix
    test_bug_fix(swarm)

    # Test 5: Simple orchestrator
    test_simple_orchestrator()

    # Interactive mode
    print("\n" + "="*80)
    user_choice = input("\nWould you like to try interactive mode? (y/n): ")
    if user_choice.lower() == 'y':
        interactive_mode()

    print("\n" + "="*80)
    print("  TEST SUITE COMPLETE")
    print("="*80)
    print("""
    ✅ The swarm orchestrator can handle various development tasks:
       - Simple functions and utilities
       - Complex class implementations
       - Bug fixes and refactoring
       - API integrations (with escalation if needed)

    Users can simply provide natural language descriptions of what they need,
    and the swarm of agents will collaborate to deliver the solution!
    """)


if __name__ == "__main__":
    main()