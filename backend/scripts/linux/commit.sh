#!/bin/bash
# commit.sh

# Change to the project directory
cd "$1" || exit 1

# Create a new file with "hello world" content in the same directory
echo "hello world" > hello_world.txt

# Get the current branch name
currentBranch=$(git rev-parse --abbrev-ref HEAD)

if [ "$currentBranch" != "develop" ]; then
    # Stage all changes, including the new file
    git add --all

    # Get the commit message from the command line argument
    commitMessage="Update"
    echo "Commit message: $commitMessage"

    # Commit all changes with the provided message
    git commit -a -m "$commitMessage"
    git pull
    git push
fi
