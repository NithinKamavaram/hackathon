#!/usr/bin/env python3
"""
Test Real Strands Implementation
Uses actual Strands SDK patterns instead of mocks
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.strands_orchestrator import StrandsCodeCollabOrchestrator, StrandsSimpleOrchestrator
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def test_strands_orchestrator():
    """Test the real Strands-based orchestrator"""
    
    print("="*70)
    print("  TESTING REAL STRANDS CODECOLLAB ORCHESTRATOR")
    print("="*70)
    
    try:
        # Initialize the real orchestrator
        print("\n🤖 Initializing Strands CodeCollab Orchestrator...")
        orchestrator = StrandsCodeCollabOrchestrator()
        print("✅ Real Strands orchestrator initialized successfully!")
        
        # Test with a development task
        task = "Create a Python function that calculates the factorial of a number using recursion"
        
        print(f"\n📝 Test Task:")
        print(f"   {task}")
        
        print(f"\n🔄 Processing with REAL Strands agents...")
        print("   This will use actual AI models via AWS Bedrock...")
        
        start_time = time.time()
        result = orchestrator.process_task(task)
        execution_time = time.time() - start_time
        
        # Display results
        print("\n" + "="*70)
        print("  REAL STRANDS EXECUTION RESULTS")
        print("="*70)
        
        if result.get('success'):
            print("✅ Task completed successfully with REAL AI!")
            
            # Show agent sequence
            if result.get('agent_sequence'):
                agents = result['agent_sequence']
                print(f"\n🔀 Agent Flow ({len(agents)} agents):")
                for i, agent in enumerate(agents, 1):
                    arrow = " → " if i < len(agents) else " ✓"
                    print(f"   {i}. {agent}{arrow}")
            
            # Show generated code
            if result.get('code'):
                print(f"\n📄 AI-Generated Code:")
                print("-" * 60)
                print(result['code'])
                print("-" * 60)
            elif result.get('final_result'):
                print(f"\n📄 Final Result:")
                print("-" * 60)
                print(result['final_result'][:1500])  # Show first 1500 chars
                if len(result['final_result']) > 1500:
                    print("... (truncated)")
                print("-" * 60)
            
            # Show decision
            decision = result.get('final_decision', result.get('decision', 'Unknown'))
            print(f"\n🎯 Final Decision: {decision}")
            
            # Show metrics
            print(f"\n📊 Execution Metrics:")
            print(f"   • Implementation: {result.get('implementation', 'unknown')}")
            print(f"   • Execution Time: {execution_time:.2f}s")
            print(f"   • Tokens Used: {result.get('tokens_used', 0)}")
            print(f"   • Agent Handoffs: {result.get('handoff_count', 0)}")
            
            # Show agent outputs (summary)
            agent_outputs = result.get('agent_outputs', {})
            if agent_outputs:
                print(f"\n🔍 Agent Output Summary:")
                for agent_name, output in agent_outputs.items():
                    output_preview = str(output)[:100].replace('\n', ' ')
                    print(f"   • {agent_name}: {output_preview}...")
            
        else:
            print("❌ Task failed!")
            error = result.get('error', 'Unknown error')
            print(f"   Error: {error}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_simple_strands_orchestrator():
    """Test the simplified Strands orchestrator"""
    
    print("\n" + "="*70)
    print("  TESTING SIMPLIFIED STRANDS ORCHESTRATOR")
    print("="*70)
    
    try:
        orchestrator = StrandsSimpleOrchestrator()
        
        task = "Create a function to validate email addresses using regex"
        
        print(f"\n📝 Simple Test Task: {task}")
        print("\n🔄 Processing with 3-step Strands flow...")
        
        result = orchestrator.process_task_simple(task)
        
        if result.get('success'):
            print("✅ Simple orchestration completed!")
            
            steps = result.get('steps', {})
            for step_name, step_data in steps.items():
                print(f"\n📍 {step_name.upper()}:")
                print(f"   Success: {step_data.get('success', False)}")
                print(f"   Output: {step_data.get('output', '')[:150]}...")
                print(f"   Tokens: {step_data.get('tokens', 0)}")
        else:
            print(f"❌ Simple orchestration failed: {result.get('error', 'Unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Simple orchestrator error: {e}")
        return None


def interactive_strands_mode():
    """Interactive mode with real Strands agents"""
    
    print("\n" + "="*70)
    print("  INTERACTIVE MODE - REAL STRANDS AI")
    print("="*70)
    
    print("\nEnter development tasks and get REAL AI responses!")
    print("Type 'quit' to exit.\n")
    
    try:
        orchestrator = StrandsCodeCollabOrchestrator()
        
        while True:
            task = input("🤖 Your development task: ").strip()
            
            if task.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not task:
                continue
            
            print("\n⏳ Processing with REAL Strands agents...")
            
            start_time = time.time()
            result = orchestrator.process_task(task)
            execution_time = time.time() - start_time
            
            if result.get('success'):
                print("✅ REAL AI task completed!")
                
                # Show code
                code = result.get('code') or result.get('final_result', '')
                if code:
                    print(f"\n📄 AI-Generated Code:")
                    print("-" * 50)
                    print(code[:2000])  # Show first 2000 chars
                    if len(code) > 2000:
                        print("... (truncated)")
                    print("-" * 50)
                
                # Show metrics
                tokens = result.get('tokens_used', 0)
                decision = result.get('final_decision', 'Unknown')
                print(f"\n📊 Stats: {tokens} tokens, {execution_time:.1f}s, Decision: {decision}")
                
            else:
                print(f"❌ Error: {result.get('error', 'Unknown')}")
            
            print()  # Blank line
            
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"❌ Interactive mode error: {e}")


def main():
    """Main test function"""
    
    print("="*70)
    print("  CODECOLLAB REAL STRANDS IMPLEMENTATION TEST")
    print("="*70)
    
    print("\nChoose a test:")
    print("1. Full Strands Orchestrator Test")
    print("2. Simple Strands Orchestrator Test") 
    print("3. Interactive Mode with Real AI")
    print("4. Run All Tests")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        test_strands_orchestrator()
    elif choice == '2':
        test_simple_strands_orchestrator()
    elif choice == '3':
        interactive_strands_mode()
    elif choice == '4':
        print("\n🚀 Running all tests...\n")
        test_strands_orchestrator()
        test_simple_strands_orchestrator()
    else:
        print("Invalid choice. Running full orchestrator test...")
        test_strands_orchestrator()


if __name__ == "__main__":
    main()