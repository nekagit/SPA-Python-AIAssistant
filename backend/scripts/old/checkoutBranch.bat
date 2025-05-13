cd /d %1
FOR /F %%i IN ('git rev-parse --abbrev-ref HEAD') DO SET currentBranch=%%i

REM Check if the current branch is 'develop', 'master', or 'main'
IF NOT "%currentBranch%"=="develop" (
    REM If it's 'develop', just push the changes
    git add --all
    git commit -m "Auto-commit changes"
) 

REM Get the new branch name from the command line argument (e.g., 'new-branch-name')
SET checkoutBranch=%2
echo %checkoutBranch%

REM Attempt to checkout 'branch'
git checkout %checkoutBranch% 2>nul

echo Successfull checkout to %checkoutBranch%

