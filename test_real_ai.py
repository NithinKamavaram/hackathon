#!/usr/bin/env python3
"""
Test Real AI Implementation
Run with actual OpenAI/Anthropic APIs instead of mocks
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

# Load real environment variables
load_dotenv('.env.real')

def test_api_keys():
    """Test if API keys are configured"""
    
    print("\n" + "="*60)
    print("  API CONFIGURATION CHECK")
    print("="*60)
    
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    
    if openai_key:
        masked_key = openai_key[:8] + "..." + openai_key[-4:] if len(openai_key) > 12 else "***"
        print(f"✅ OpenAI API Key: {masked_key}")
    else:
        print("❌ OpenAI API Key: Not configured")
    
    if anthropic_key:
        masked_key = anthropic_key[:8] + "..." + anthropic_key[-4:] if len(anthropic_key) > 12 else "***"
        print(f"✅ Anthropic API Key: {masked_key}")
    else:
        print("❌ Anthropic API Key: Not configured")
    
    if not openai_key and not anthropic_key:
        print("\n⚠️  No API keys configured!")
        print("Please set up your API keys in .env.real file:")
        print("  OPENAI_API_KEY=sk-your-key-here")
        print("  ANTHROPIC_API_KEY=your-key-here")
        return False
    
    return True


def test_real_agents():
    """Test real AI agents with a simple task"""
    
    if not test_api_keys():
        return
    
    print("\n" + "="*60)
    print("  TESTING REAL AI AGENTS")
    print("="*60)
    
    try:
        from agents.swarm_orchestrator_real import CodeCollabSwarmReal
        
        # Determine which provider to use
        provider = "openai" if os.getenv('OPENAI_API_KEY') else "anthropic"
        
        print(f"\n🤖 Initializing Real AI Swarm with {provider.upper()}...")
        swarm = CodeCollabSwarmReal(ai_provider=provider)
        print("✅ Real swarm initialized successfully!")
        
        # Test with a simple task
        task = "Create a Python function that calculates the factorial of a number"
        
        print(f"\n📝 Test Task: {task}")
        print("\n🔄 Processing with REAL AI agents...")
        
        result = swarm.process_task(task)
        
        # Display results
        print("\n" + "="*60)
        print("  REAL AI RESULTS")
        print("="*60)
        
        if result.get('success'):
            print("✅ Task processed successfully by real AI!")
            
            # Show agent sequence
            if result.get('agent_sequence'):
                print(f"\n🔀 Agent Flow: {' → '.join(result['agent_sequence'])}")
            
            # Show generated code
            if result.get('code'):
                print("\n📄 Generated Code:")
                print("-" * 50)
                print(result['code'])
                print("-" * 50)
            elif result.get('final_result'):
                print("\n📄 Final Result:")
                print("-" * 50)
                print(result['final_result'][:1000])  # Show first 1000 chars
                print("-" * 50)
            
            # Show stats
            tokens = result.get('tokens_used', 0)
            latency = result.get('latency_ms', 0)
            provider_used = result.get('ai_provider', 'unknown')
            
            print(f"\n📊 Statistics:")
            print(f"   • AI Provider: {provider_used.upper()}")
            print(f"   • Tokens Used: {tokens}")
            print(f"   • Total Latency: {latency:.0f}ms")
            print(f"   • Implementation: {result.get('implementation', 'unknown')}")
            
            # Show decision
            decision = result.get('final_decision', result.get('decision', 'Unknown'))
            print(f"   • Decision: {decision}")
            
        else:
            print("❌ Task failed!")
            error = result.get('error', 'Unknown error')
            print(f"   Error: {error}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Check your API keys and internet connection")


def test_interactive_real():
    """Interactive mode with real AI"""
    
    if not test_api_keys():
        return
    
    print("\n" + "="*60)
    print("  REAL AI INTERACTIVE MODE")
    print("="*60)
    
    try:
        from agents.swarm_orchestrator_real import CodeCollabSwarmReal
        
        provider = "openai" if os.getenv('OPENAI_API_KEY') else "anthropic"
        swarm = CodeCollabSwarmReal(ai_provider=provider)
        
        print(f"\n🤖 Real AI Swarm ready with {provider.upper()}")
        print("Enter development tasks and get real AI-generated code!")
        print("Type 'quit' to exit.\n")
        
        while True:
            task = input("📝 Your task: ").strip()
            
            if task.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not task:
                continue
            
            print("\n⏳ Processing with REAL AI agents...")
            
            result = swarm.process_task(task)
            
            if result.get('success'):
                print("✅ Real AI task completed!")
                
                code = result.get('code') or result.get('final_result', '')
                if code:
                    print("\n📄 AI-Generated Code:")
                    print("-" * 50)
                    print(code[:1500])  # Show first 1500 chars
                    if len(code) > 1500:
                        print("... (truncated)")
                    print("-" * 50)
                
                tokens = result.get('tokens_used', 0)
                latency = result.get('latency_ms', 0)
                print(f"\n📊 Stats: {tokens} tokens, {latency:.0f}ms")
                
            else:
                print(f"❌ Error: {result.get('error', 'Unknown')}")
            
            print()  # Blank line
            
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main test function"""
    
    print("="*60)
    print("  CODECOLLAB REAL AI IMPLEMENTATION TEST")
    print("="*60)
    
    print("\nChoose a test:")
    print("1. Test API Configuration")
    print("2. Test Real AI Agents (Single Task)")
    print("3. Interactive Mode with Real AI")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        test_api_keys()
    elif choice == '2':
        test_real_agents()
    elif choice == '3':
        test_interactive_real()
    else:
        print("Invalid choice. Running API configuration test...")
        test_api_keys()


if __name__ == "__main__":
    main()