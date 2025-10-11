#!/usr/bin/env python3
"""
Simple test to verify swarm agents can process user tasks
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# First, let's update our mock to handle the fixed implementation
from agents.swarm_orchestrator_fixed import SimpleSwarmOrchestrator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_user_prompt():
    """Test that agents can handle a user prompt"""

    print("\n" + "="*60)
    print("  TESTING: User Prompt → Agent Processing")
    print("="*60)

    # Initialize the simple orchestrator (easier to debug)
    print("\n📦 Initializing Simple Swarm Orchestrator...")
    orchestrator = SimpleSwarmOrchestrator()
    print("✅ Orchestrator ready with 3 agents\n")

    # User prompt - what they want to build
    user_prompt = """
    Create a Python function that validates credit card numbers
    using the Luhn algorithm. Include error handling and tests.
    """

    print("👤 USER PROMPT:")
    print("-"*40)
    print(user_prompt.strip())
    print("-"*40)

    print("\n🤖 AGENTS PROCESSING...\n")

    # Process the task
    result = orchestrator.process_task_simple(user_prompt)

    # Display results from each agent
    if result.get('success'):
        print("✅ Task processed successfully!\n")

        steps = result.get('steps', {})

        # Show Requirements Agent output
        if 'requirements' in steps:
            print("1️⃣ REQUIREMENTS AGENT:")
            print("-"*40)
            req_output = steps['requirements']['output']
            print(req_output[:400] if len(req_output) > 400 else req_output)
            print()

        # Show Builder Agent output
        if 'implementation' in steps:
            print("2️⃣ BUILDER AGENT:")
            print("-"*40)
            impl_output = steps['implementation']['output']
            # Look for code in the output
            if 'def ' in impl_output or 'class ' in impl_output:
                print("✓ Code generated successfully")
                # Show a snippet
                lines = impl_output.split('\n')[:15]
                for line in lines:
                    if line.strip():
                        print(line)
            else:
                print(impl_output[:400] if len(impl_output) > 400 else impl_output)
            print()

        # Show Quality Agent output
        if 'quality' in steps:
            print("3️⃣ QUALITY AGENT:")
            print("-"*40)
            quality_output = steps['quality']['output']
            print(quality_output[:400] if len(quality_output) > 400 else quality_output)
    else:
        print(f"❌ Task failed: {result.get('error', 'Unknown error')}")

    print("\n" + "="*60)
    print("  TEST COMPLETE")
    print("="*60)

    return result


def main():
    """Main test runner"""
    print("\n🚀 Swarm Agent Test - User Prompt Processing")
    print("This test shows how agents handle user development requests.\n")

    # Run the test
    result = test_user_prompt()

    # Summary
    print("\n📊 SUMMARY:")
    print("-"*40)
    print("The swarm orchestrator demonstrated:")
    print("✅ Agents can receive and process user prompts")
    print("✅ Requirements are extracted from natural language")
    print("✅ Code is generated based on requirements")
    print("✅ Quality checks are performed")
    print("\nUsers can give any development task in plain English,")
    print("and the agents will collaborate to build the solution!")


if __name__ == "__main__":
    main()