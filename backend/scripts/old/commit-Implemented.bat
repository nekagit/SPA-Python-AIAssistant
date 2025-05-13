cd /d %1
REM Get the current branch name
FOR /F %%i IN ('git rev-parse --abbrev-ref HEAD') DO SET currentBranch=%%i

REM Check if the current branch is 'develop', 'master', or 'main'
IF NOT "%currentBranch%"=="develop" (
  REM Stage all changes, including new files
  git add --all
  git pull
  git commit -a -m "Update"
  git push
) 
pause

