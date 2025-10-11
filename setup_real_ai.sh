#!/bin/bash
# Setup script for real AI implementation

echo "🚀 Setting up Real AI Implementation..."

# Check if .env.real exists
if [ ! -f ".env.real" ]; then
    echo "📝 Creating .env.real configuration file..."
    cat > .env.real << 'EOF'
# Real AI Implementation Configuration

# === OpenAI Configuration ===
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# === Anthropic Configuration ===  
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# === Settings ===
USE_REAL_AGENTS=true
PREFERRED_AI_PROVIDER=openai
APP_ENV=production
DEBUG=false
LOG_LEVEL=INFO
EOF
fi

echo "⚠️  IMPORTANT: Edit .env.real and add your API keys!"
echo ""
echo "Get API keys from:"
echo "  • OpenAI: https://platform.openai.com/api-keys"
echo "  • Anthropic: https://console.anthropic.com/"
echo ""
echo "Then run: python test_real_ai.py"