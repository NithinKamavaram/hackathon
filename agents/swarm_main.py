"""
Main entry point for CodeCollab Swarm-based agent system
"""

from .swarm_orchestrator import CodeCollabSwarm, CodeCollabSwarmTool
from dotenv import load_dotenv
import logging
import sys
import asyncio

# Configure logging with more detail for swarm coordination
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/swarm.log')
    ]
)

# Enable debug logs for swarm coordination
logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


def demo_native_swarm():
    """Demonstrate native Swarm implementation with autonomous coordination"""

    logger.info("=" * 80)
    logger.info("DEMO: Native Swarm Implementation")
    logger.info("=" * 80)

    # Create swarm orchestrator
    swarm = CodeCollabSwarm()

    # Example tasks of varying complexity
    tasks = [
        {
            "name": "Simple Bug Fix",
            "description": """
            Fix the typo in the login error message that says 'Passwrod incorrect'
            instead of 'Password incorrect'.
            """
        },
        {
            "name": "Medium Feature",
            "description": """
            Add input validation to the user registration form. Ensure email addresses
            are valid format, passwords are at least 8 characters with one uppercase,
            one lowercase, and one number. Show appropriate error messages.
            """
        },
        {
            "name": "Complex Task",
            "description": """
            Implement a real-time notification system that:
            - Supports WebSocket connections for live updates
            - Handles offline users with queuing
            - Provides different notification types (info, warning, error)
            - Includes rate limiting to prevent spam
            - Stores notification history in database
            - Has admin controls for managing notifications
            """
        }
    ]

    for task_info in tasks:
        logger.info(f"\nProcessing: {task_info['name']}")
        logger.info("-" * 40)

        result = swarm.process_task(task_info['description'])

        # Display results
        if result['success']:
            print(f"\n✅ Task: {task_info['name']}")
            print(f"Agent sequence: {' → '.join(result['agent_sequence'])}")
            print(f"Handoffs: {result['handoff_count']}")
            print(f"Execution time: {result['execution_time_ms']}ms")
            print(f"Tokens used: {result['total_tokens']}")

            # Show shared knowledge
            if result.get('shared_knowledge'):
                print("\nShared Knowledge:")
                for agent, knowledge in result['shared_knowledge'].items():
                    print(f"  • {agent}: {knowledge.get('contribution', '')[:100]}...")

            # Display final result
            print(f"\nFinal Result Preview:")
            print(result['final_result'][:500] if result['final_result'] else "No result")
        else:
            print(f"\n❌ Task Failed: {task_info['name']}")
            print(f"Error: {result.get('error', 'Unknown error')}")


def demo_swarm_tool():
    """Demonstrate the built-in swarm tool for automatic agent creation"""

    logger.info("\n" + "=" * 80)
    logger.info("DEMO: Swarm Tool (Automatic Agent Creation)")
    logger.info("=" * 80)

    # Create swarm tool orchestrator
    swarm_tool = CodeCollabSwarmTool()

    # Complex task for the swarm tool
    task = """
    Create a complete REST API for a task management system with the following requirements:
    - User authentication with JWT tokens
    - CRUD operations for tasks (create, read, update, delete)
    - Task categories and tags
    - Due dates and priority levels
    - User assignment and collaboration
    - Search and filter capabilities
    - Pagination for list endpoints
    - Proper error handling and validation
    - OpenAPI/Swagger documentation
    """

    logger.info("Processing complex API design task...")
    result = swarm_tool.process_with_auto_swarm(task)

    if result['success']:
        print("\n✅ Swarm Tool Execution Successful")
        print(f"Agents involved: {' → '.join(result['agents_involved'])}")
        print(f"Execution time: {result['execution_time']}ms")
        print(f"\nResult Preview:")
        print(result['final_result'][:1000] if result['final_result'] else "No result")
    else:
        print("\n❌ Swarm Tool Execution Failed")
        print(f"Error: {result.get('error', 'Unknown error')}")


async def demo_async_swarm():
    """Demonstrate asynchronous swarm execution"""

    logger.info("\n" + "=" * 80)
    logger.info("DEMO: Asynchronous Swarm Execution")
    logger.info("=" * 80)

    swarm = CodeCollabSwarm()

    # Multiple tasks to process in parallel
    tasks = [
        "Fix the date formatting bug in the dashboard",
        "Add dark mode toggle to the settings page",
        "Optimize database queries for the user search feature"
    ]

    # Process tasks concurrently
    logger.info("Processing multiple tasks concurrently...")
    results = await asyncio.gather(
        *[swarm.process_task_async(task) for task in tasks]
    )

    # Display results
    for i, (task, result) in enumerate(zip(tasks, results)):
        print(f"\nTask {i+1}: {task[:50]}...")
        if result['success']:
            print(f"  ✅ Success - Agents: {len(result['agent_sequence'])}")
            print(f"  Time: {result['execution_time_ms']}ms")
        else:
            print(f"  ❌ Failed: {result.get('error', 'Unknown')}")


def compare_patterns():
    """Compare different orchestration patterns"""

    print("\n" + "=" * 80)
    print("ORCHESTRATION PATTERN COMPARISON")
    print("=" * 80)

    print("""
    1. SWARM PATTERN (Current Implementation)
    ==========================================
    Pros:
    • Autonomous agent coordination
    • Shared context and working memory
    • Emergent collective intelligence
    • Flexible handoffs based on expertise
    • Built-in safety mechanisms

    Best for:
    • Complex problems requiring multiple perspectives
    • Tasks where the solution path isn't predetermined
    • Collaborative problem-solving scenarios

    2. WORKFLOW PATTERN (Alternative)
    ==================================
    Pros:
    • Clear sequential stages
    • Explicit dependency management
    • Better for audit trails
    • Predictable execution flow
    • Easy retry of specific steps

    Best for:
    • Well-defined processes
    • Tasks with clear stages
    • When tracking each step is critical

    3. HIERARCHICAL PATTERN (Original)
    ===================================
    Pros:
    • Central orchestrator control
    • Clear delegation model
    • Simple to understand
    • Direct task assignment

    Best for:
    • Simple task delegation
    • When central control is needed
    • Clear supervisor-worker relationships

    For CodeCollab, SWARM is ideal because:
    • Development tasks often require back-and-forth between agents
    • Requirements may need clarification mid-implementation
    • Quality checks might require multiple iterations
    • Agents can autonomously decide when to escalate
    """)


def main():
    """Main function demonstrating all swarm capabilities"""

    # Load environment variables
    load_dotenv()

    print("\n" + "🐝" * 40)
    print("CODECOLLAB SWARM INTELLIGENCE SYSTEM")
    print("🐝" * 40)

    # Show pattern comparison
    compare_patterns()

    # Run demonstrations
    try:
        # Demo 1: Native Swarm
        demo_native_swarm()

        # Demo 2: Swarm Tool
        demo_swarm_tool()

        # Demo 3: Async Swarm
        print("\nRunning async demonstration...")
        asyncio.run(demo_async_swarm())

    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"\n❌ Demo failed: {e}")

    print("\n" + "=" * 80)
    print("SWARM DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("""
    Key Takeaways:
    • Agents autonomously coordinate through handoffs
    • Shared context enables collective intelligence
    • Built-in safety prevents infinite loops
    • Flexible enough to handle varying complexity
    • Can process tasks in parallel for efficiency
    """)


if __name__ == "__main__":
    main()