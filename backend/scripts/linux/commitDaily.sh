#!/bin/bash
# commit.sh

# Change to the project directory
cd "$1" || exit 1

# Function to commit, push, and pull
commit_push_pull() {
    # Stage all changes
    git add --all

    # Get the commit message from the command line argument
    commitMessage="Update"
    echo "Commit message: $commitMessage"

    # Commit all changes with the provided message
    git commit -a -m "$commitMessage"

    # Pull and push changes
    git pull
    git push
}

# Create a new file with "hello world" content in the same directory
echo "hello world" > hello_world.txt

# Get the current branch name
currentBranch=$(git rev-parse --abbrev-ref HEAD)

if [ "$currentBranch" != "develop" ]; then
    # First commit with the new file
    commit_push_pull

    # Delete the file
    rm hello_world.txt

    # Second commit after deleting the file
    commit_push_pull

    # Recreate the file with "hello world"
    echo "hello world" > hello_world.txt

    # Third commit with the recreated file
    commit_push_pull
fi
