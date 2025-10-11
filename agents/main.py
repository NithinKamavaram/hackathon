"""
Main entry point for CodeCollab agent system
"""

from .orchestrator import CodeCollabOrchestrator
from dotenv import load_dotenv
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/agents.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to demonstrate agent system"""

    # Load environment variables
    load_dotenv()

    # Create orchestrator
    logger.info("Initializing CodeCollab orchestrator...")
    orchestrator = CodeCollabOrchestrator()

    # Example task
    task = """
    Fix the bug where user authentication fails when the password contains
    special characters like quotes or backslashes. The issue is in the login
    validation function - it's not properly escaping these characters.

    Requirements:
    - Fix the escaping issue
    - Add comprehensive test coverage for special characters
    - Ensure backward compatibility with existing passwords
    - Add proper error messages for invalid credentials
    """

    logger.info("Processing example task...")
    result = orchestrator.process_task_step_by_step(task)

    # Display results
    print("\n" + "="*80)
    print("CODECOLLAB EXECUTION RESULTS")
    print("="*80)

    for step_name, step_result in result.get("steps", {}).items():
        print(f"\n{step_name.upper()}:")
        print("-" * 40)
        if step_result.get("success"):
            print(f"✅ Success")
            print(f"Tokens: {step_result.get('tokens', 0)}")
            print(f"Latency: {step_result.get('latency_ms', 0)}ms")
        else:
            print(f"❌ Failed")
            print(f"Error: {step_result.get('error', 'Unknown')}")

    print("\n" + "="*80)

    if result.get("success"):
        print("✅ TASK COMPLETED SUCCESSFULLY")
    else:
        print(f"❌ TASK FAILED AT: {result.get('failed_at', 'unknown')}")

    print("="*80)


if __name__ == "__main__":
    main()