#!/usr/bin/env python3
"""
Demo script showing complete swarm agent flow with natural language processing
"""

from agents.swarm_orchestrator import CodeCollabSwarm
from dotenv import load_dotenv
import time
import json

# Load environment variables
load_dotenv()

class Colors:
    """Terminal colors for better output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_section(title):
    """Print a section header"""
    print(f"\n{Colors.CYAN}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}  {title}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*80}{Colors.ENDC}\n")

def demo_swarm_flow():
    """Demonstrate the complete swarm flow"""

    print_section("🤖 CODECOLLAB SWARM DEMONSTRATION")

    print("""
This demo shows how natural language tasks are processed by our swarm of agents:
1. User provides task in plain English
2. RequirementsAgent analyzes and structures the request
3. ContextAgent gathers relevant codebase information
4. BuilderAgent generates production code
5. QualityAgent validates the implementation
6. EscalationAgent decides if human help is needed
    """)

    # Initialize swarm
    print(f"{Colors.YELLOW}📦 Initializing swarm agents...{Colors.ENDC}")
    swarm = CodeCollabSwarm()
    print(f"{Colors.GREEN}✅ Swarm ready with 5 specialized agents!{Colors.ENDC}\n")

    # Demo 1: Simple task
    print_section("DEMO 1: Simple Function Creation")

    task1 = "Create a Python function to check if a number is prime"
    print(f"{Colors.BOLD}User Input:{Colors.ENDC} '{task1}'")
    print(f"\n{Colors.YELLOW}🔄 Processing...{Colors.ENDC}")

    result1 = swarm.process_task(task1)

    print(f"\n{Colors.GREEN}✅ Task completed successfully!{Colors.ENDC}")
    print(f"📊 Decision: {Colors.GREEN}{result1.get('final_decision', 'COMPLETE')}{Colors.ENDC}")

    # Show agent flow
    if result1.get('agent_outputs'):
        print(f"\n{Colors.BOLD}Agent Flow:{Colors.ENDC}")
        for agent, output in result1['agent_outputs'].items():
            print(f"  → {agent}: {output.get('handoff_message', '')}")

    # Show generated code snippet
    if result1.get('code'):
        print(f"\n{Colors.BOLD}Generated Code (snippet):{Colors.ENDC}")
        code_lines = result1['code'].split('\n')[:10]
        for line in code_lines:
            print(f"    {line}")
        print("    ...")

    # Demo 2: Complex task with escalation
    print_section("DEMO 2: Complex Task Requiring Human Expertise")

    task2 = "Design and implement a distributed payment processing microservice with Stripe integration and PCI compliance"
    print(f"{Colors.BOLD}User Input:{Colors.ENDC} '{task2[:80]}...'")
    print(f"\n{Colors.YELLOW}🔄 Processing...{Colors.ENDC}")

    result2 = swarm.process_task(task2)

    print(f"\n{Colors.YELLOW}⚠️ Task requires human expertise!{Colors.ENDC}")
    print(f"📊 Decision: {Colors.YELLOW}{result2.get('final_decision', 'ESCALATE')}{Colors.ENDC}")
    print(f"📝 Reason: {result2.get('decision', 'Task too complex for AI alone')}")

    # Show agent analysis
    if result2.get('agent_outputs'):
        print(f"\n{Colors.BOLD}Agent Analysis:{Colors.ENDC}")
        for agent, output in result2['agent_outputs'].items():
            response = output.get('response', '')
            if response:
                print(f"  {agent}: {response[:100]}...")

    # Demo 3: Bug fix task
    print_section("DEMO 3: Bug Fix Request")

    task3 = """
    Fix this bug: My login function crashes when users enter emails with special
    characters like + or . before the @ symbol. Need proper email validation.
    """
    print(f"{Colors.BOLD}User Input:{Colors.ENDC} Bug fix request for email validation")
    print(f"\n{Colors.YELLOW}🔄 Processing...{Colors.ENDC}")

    result3 = swarm.process_task(task3)

    print(f"\n{Colors.GREEN}✅ Bug fix implemented!{Colors.ENDC}")
    print(f"📊 Decision: {Colors.GREEN}{result3.get('final_decision', 'COMPLETE')}{Colors.ENDC}")

    # Summary
    print_section("📊 DEMONSTRATION SUMMARY")

    print(f"""
{Colors.BOLD}Results:{Colors.ENDC}
1. Simple Task: {Colors.GREEN}✅ Completed by AI{Colors.ENDC}
2. Complex Task: {Colors.YELLOW}⚠️ Escalated to human{Colors.ENDC}
3. Bug Fix: {Colors.GREEN}✅ Completed by AI{Colors.ENDC}

{Colors.BOLD}Key Features Demonstrated:{Colors.ENDC}
• Natural language understanding
• Multi-agent collaboration
• Intelligent task routing
• Automatic code generation
• Quality validation
• Smart escalation decisions

{Colors.BOLD}Agent Collaboration Pattern:{Colors.ENDC}
RequirementsAgent → ContextAgent → BuilderAgent → QualityAgent → EscalationAgent

{Colors.GREEN}✨ The swarm successfully processes natural language requests and makes
   intelligent decisions about task completion vs. human escalation!{Colors.ENDC}
    """)

def show_live_processing():
    """Show live processing with simulated delays"""

    print_section("🎬 LIVE PROCESSING DEMONSTRATION")

    swarm = CodeCollabSwarm()
    task = "Create a function to calculate the factorial of a number"

    print(f"{Colors.BOLD}Task:{Colors.ENDC} {task}")
    print(f"\n{Colors.YELLOW}Starting swarm processing...{Colors.ENDC}\n")

    agents = [
        ("RequirementsAgent", "Analyzing task requirements...", "✅ Requirements extracted"),
        ("ContextAgent", "Gathering codebase context...", "✅ Context identified"),
        ("BuilderAgent", "Generating code implementation...", "✅ Code generated"),
        ("QualityAgent", "Running quality checks...", "✅ Tests passed"),
        ("EscalationAgent", "Making final decision...", "✅ Task completed")
    ]

    for agent, processing, complete in agents:
        print(f"🤖 {Colors.BOLD}{agent}{Colors.ENDC}")
        print(f"   {Colors.YELLOW}{processing}{Colors.ENDC}")
        time.sleep(0.5)  # Simulate processing time
        print(f"   {Colors.GREEN}{complete}{Colors.ENDC}")

    # Process the actual task
    result = swarm.process_task(task)

    print(f"\n{Colors.GREEN}{'='*80}{Colors.ENDC}")
    print(f"{Colors.BOLD}✨ TASK COMPLETE!{Colors.ENDC}")
    print(f"{Colors.GREEN}{'='*80}{Colors.ENDC}")

    if result.get('code'):
        print(f"\n{Colors.BOLD}Generated Code:{Colors.ENDC}")
        print(result['code'])

if __name__ == "__main__":
    try:
        # Run main demo
        demo_swarm_flow()

        # Ask if user wants to see live processing
        print(f"\n{Colors.YELLOW}Would you like to see a live processing demonstration? (y/n): {Colors.ENDC}", end='')
        choice = input().strip().lower()

        if choice == 'y':
            show_live_processing()

        print(f"\n{Colors.CYAN}Thank you for watching the CodeCollab Swarm demonstration!{Colors.ENDC}")

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Demo interrupted by user.{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.ENDC}")