HOSTED_AGENTS_PATH="1-uagents"
CATEGORIES=("finance" "geo" "knowledge-base" "search" "travel" "utility" "communication")

cd $HOSTED_AGENTS_PATH

for category in ${CATEGORIES[@]}; do
    for agent in $category/*; do
        cd $agent

        echo "Deploying agent $agent..."

        while IFS='=' read -r key value; do
            if cat *.py | grep -q $key; then
                echo "Adding secret $key to agent $agent..."
                echo "$key=$value" # >> .secrets
            fi
        done < <(printenv | grep API_KEY)

        # Create a .avctl folder for new agents if it doesn't exist
        avctl hosting init

        # Get the agent's name from the README.md top line header
        agent_name=$(head -n 1 README.md | sed -e 's/#//g' | xargs)

        # Deploy the agent with secrets if they exist
        if [ -s .secrets ]; then
            avctl hosting deploy -n "$agent_name" -s .secrets --no-dependency-check || true
        else
            avctl hosting deploy -n "$agent_name" --no-dependency-check || true
        fi

        cd ../..
    done
done