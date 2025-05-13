@echo off
REM commit.bat

REM Change to the project directory
cd "%~1" || exit /b 1

REM Create a new file with "hello world" content in the same directory
echo hello world > hello_world.txt

REM Get the current branch name
FOR /F "tokens=*" %%i IN ('git rev-parse --abbrev-ref HEAD') DO SET currentBranch=%%i

IF NOT "%currentBranch%"=="develop" (
    REM Stage all changes, including the new file
    git add --all

    REM Commit message
    set commitMessage=Update
    echo Commit message: %commitMessage%

    REM Commit all changes with the provided message
    git commit -a -m "%commitMessage%"
    git pull
    git push
)
