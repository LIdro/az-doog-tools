#!/bin/bash
# Doogarey Tools Setup Script for Agent Zero
# This script helps set up and maintain the Doogarey integration

set -e

AGENT_ZERO_DIR="/a0"
BACKUP_DIR="/backup/doogarey-tools"
TOOLS_DIR="$AGENT_ZERO_DIR/python/tools"
PROMPTS_DIR="$AGENT_ZERO_DIR/prompts/doog_prompts"

echo "🚀 Doogarey Tools Setup for Agent Zero"
echo "======================================"

# Function to backup existing doog tools
backup_tools() {
    echo "📦 Creating backup..."
    mkdir -p "$BACKUP_DIR/tools"
    mkdir -p "$BACKUP_DIR/prompts"
    
    if [ -f "$TOOLS_DIR/doog_workspace.py" ]; then
        cp "$TOOLS_DIR"/doog_*.py "$BACKUP_DIR/tools/" 2>/dev/null || true
        echo "✅ Backed up tool files"
    fi
    
    if [ -d "$PROMPTS_DIR" ]; then
        cp -r "$PROMPTS_DIR" "$BACKUP_DIR/prompts/" 2>/dev/null || true
        echo "✅ Backed up prompt files"
    fi
}

# Function to verify tool installation
verify_installation() {
    echo "🔍 Verifying installation..."
    
    # Check tool files
    local tools_ok=true
    for tool in "doog_workspace" "doog_project" "doog_task" "doog_file"; do
        if [ ! -f "$TOOLS_DIR/${tool}.py" ]; then
            echo "❌ Missing tool: ${tool}.py"
            tools_ok=false
        fi
    done
    
    # Check prompt files
    local prompts_ok=true
    for prompt in "doog_workspace" "doog_project" "doog_task" "doog_file"; do
        if [ ! -f "$PROMPTS_DIR/agent.system.tool.${prompt}.md" ]; then
            echo "❌ Missing prompt: agent.system.tool.${prompt}.md"
            prompts_ok=false
        fi
    done
    
    if [ "$tools_ok" = true ] && [ "$prompts_ok" = true ]; then
        echo "✅ All Doogarey tools and prompts are properly installed"
        return 0
    else
        echo "❌ Installation verification failed"
        return 1
    fi
}

# Function to test API connectivity
test_api() {
    local api_url="${1:-http://localhost:3000}"
    echo "🌐 Testing API connectivity to $api_url..."
    
    if command -v curl >/dev/null 2>&1; then
        if curl -s --connect-timeout 5 "$api_url/health" >/dev/null 2>&1; then
            echo "✅ API is accessible"
        else
            echo "⚠️  API might not be accessible (this is normal if Doogarey isn't running)"
        fi
    else
        echo "⚠️  curl not available, skipping API test"
    fi
}

# Function to show usage information
show_usage() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  verify              Verify installation"
    echo "  backup              Backup existing doog tools"
    echo "  test-api [url]      Test API connectivity (default: http://localhost:3000)"
    echo "  setup-prompts       Set up Agent Zero to use doog_prompts"
    echo "  help                Show this help"
    echo ""
    echo "Examples:"
    echo "  $0 verify"
    echo "  $0 test-api https://api.doogarey.com"
}

# Function to setup prompts configuration
setup_prompts() {
    echo "⚙️  Setting up Agent Zero to use Doogarey prompts..."
    
    # This would typically involve updating Agent Zero's configuration
    # The exact method depends on how Agent Zero handles prompt selection
    echo "📝 To use Doogarey prompts:"
    echo "   1. Open Agent Zero settings"
    echo "   2. Navigate to Agent Config section"
    echo "   3. Set prompt directory to 'doog_prompts'"
    echo "   4. Save configuration"
    echo ""
    echo "✅ Instructions provided"
}

# Function to show system status
show_status() {
    echo "📊 Doogarey Integration Status"
    echo "=============================="
    
    # Check if running in Agent Zero environment
    if [ -d "$AGENT_ZERO_DIR" ]; then
        echo "✅ Agent Zero environment detected"
    else
        echo "❌ Agent Zero environment not found at $AGENT_ZERO_DIR"
    fi
    
    # Check tools
    local tool_count=0
    for tool in "doog_workspace" "doog_project" "doog_task" "doog_file"; do
        if [ -f "$TOOLS_DIR/${tool}.py" ]; then
            ((tool_count++))
        fi
    done
    echo "📦 Doog tools installed: $tool_count/4"
    
    # Check prompts
    local prompt_count=0
    for prompt in "doog_workspace" "doog_project" "doog_task" "doog_file"; do
        if [ -f "$PROMPTS_DIR/agent.system.tool.${prompt}.md" ]; then
            ((prompt_count++))
        fi
    done
    echo "📝 Doog prompts installed: $prompt_count/4"
    
    # Check documentation
    if [ -f "$AGENT_ZERO_DIR/DOOGAREY_INTEGRATION.md" ]; then
        echo "✅ Integration documentation available"
    else
        echo "❌ Integration documentation missing"
    fi
}

# Main script logic
case "${1:-help}" in
    "verify")
        verify_installation
        ;;
    "backup")
        backup_tools
        ;;
    "test-api")
        test_api "$2"
        ;;
    "setup-prompts")
        setup_prompts
        ;;
    "status")
        show_status
        ;;
    "help"|*)
        show_usage
        ;;
esac

echo ""
echo "📚 For detailed information, see: DOOGAREY_INTEGRATION.md"
echo "🔗 Doogarey Platform: https://doogarey.com"
