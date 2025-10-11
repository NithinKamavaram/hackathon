#!/usr/bin/env python3
"""
Simple test to demonstrate agent flow for addition function
"""

from agents.swarm_orchestrator import CodeCollabSwarm
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

print("\n" + "="*80)
print("TESTING: Create a function to do addition of two numbers")
print("="*80)

# Initialize swarm
print("\n📦 Initializing CodeCollab Swarm...")
swarm = CodeCollabSwarm()
print("✅ Swarm ready with 5 specialized agents\n")

# Define task
task = "Create a Python function to do addition of two numbers with proper type hints and docstring"

print("📝 TASK:", task)
print("\n" + "─"*80)
print("🔄 WATCHING AGENT FLOW...")
print("─"*80 + "\n")

# Process task and time it
start = time.time()
result = swarm.process_task(task)
elapsed = time.time() - start

print("\n" + "─"*80)
print("📊 EXECUTION SUMMARY")
print("─"*80)
print(f"⏱️  Time: {elapsed:.2f} seconds")
print(f"🎯 Success: {result.get('success', False)}")

# Show agent sequence
agents = result.get('agent_sequence', [])
if agents:
    print(f"\n🔀 AGENT HANDOFF CHAIN ({len(agents)} agents):")
    for i, agent in enumerate(agents, 1):
        print(f"   {i}. {agent}")

# Show final result
print(f"\n📋 FINAL RESULT:")
print("─"*80)
final_result = result.get('final_result', 'No result available')
# Truncate if too long
if len(final_result) > 1500:
    print(final_result[:1500] + "\n... (truncated)")
else:
    print(final_result)

print("\n" + "="*80)
print("✅ TEST COMPLETE")
print("="*80 + "\n")
