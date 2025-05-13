cd /d %1

REM Get the branch name from the command line argument
SET branchName=%2
echo %branchName%
REM Check the current branch name
for /f %%i in ('git rev-parse --abbrev-ref HEAD') do set current_branch=%%i
REM Check if the current branch is one of 'develop'
If NOT "%current_branch%"=="develop" (
  git add --all
  git commit -m "Auto-commit changes"
)

REM Attempt to checkout 'develop or master'
git checkout develop 2>nul

REM Sync with the 'develop' branch (pull changes)
git pull

REM Check out the specified branch
git checkout %branchName% 2>nul

echo %branchName%

REM Merge with 'develop'
git merge develop 2>nul
git push
pause

