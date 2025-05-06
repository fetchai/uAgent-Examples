#!/bin/bash

while IFS='=' read -r key value; do
    if cat *.py | grep -q $key; then
        echo "Adding secret $key to agent..."
        echo "$key=$value" >> .secrets
    fi
done < <(printenv | grep _KEY)

# Create a .avctl folder for new agents if it doesn't exist
avctl hosting init

# Get the agent's name from the README.md top line header
agent_name=$(head -n 1 README.md | sed -e 's/#//g' | xargs)

# Deploy the agent with secrets if they exist
if [ -s .secrets ]; then
    avctl hosting deploy -n "$agent_name" --network mainnet -s .secrets --no-dependency-check || true
else
    avctl hosting deploy -n "$agent_name" --network mainnet --no-dependency-check || true
fi
