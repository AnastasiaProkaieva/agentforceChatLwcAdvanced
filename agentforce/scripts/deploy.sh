#!/bin/bash
# Script to deploy Agentforce agent programmatically

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🤖 Agentforce Agent Deployment Script${NC}"
echo ""

# Check if Agentforce CLI plugin is installed
if ! sf plugins | grep -q "@salesforce/plugin-agent"; then
    echo -e "${YELLOW}Installing Salesforce CLI Agentforce plugin...${NC}"
    sf plugins install @salesforce/plugin-agent
fi

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"
AGENT_SPEC="$PROJECT_ROOT/agentforce/agent-spec.yaml"

# Check if agent spec file exists
if [ ! -f "$AGENT_SPEC" ]; then
    echo -e "${RED}Error: agent-spec.yaml not found at $AGENT_SPEC${NC}"
    exit 1
fi

# Get target org (or use default)
TARGET_ORG=${1:-$(sf config get target-org --json | jq -r '.result[0].value')}

if [ -z "$TARGET_ORG" ]; then
    echo -e "${RED}Error: No target org specified and no default org set${NC}"
    echo "Usage: ./agentforce/scripts/deploy.sh [org-alias]"
    exit 1
fi

echo -e "${GREEN}Deploying agent to org: ${TARGET_ORG}${NC}"
echo -e "${YELLOW}Using spec file: ${AGENT_SPEC}${NC}"
echo ""

# Create/update agent
sf agent create \
    --name "Agentforce Chat Agent" \
    --api-name Agentforce_Chat_Agent \
    --spec "$AGENT_SPEC" \
    --target-org "$TARGET_ORG"

echo ""
echo -e "${GREEN}✅ Agent deployed successfully!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Copy the Agent ID from the output above"
echo "2. Update your LWC component configuration with the new Agent ID"
echo "3. Test the agent in your Experience Cloud site"
