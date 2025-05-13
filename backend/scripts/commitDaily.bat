@echo off
setlocal

cd %1 || exit /b 1

echo hello world > hello_world.txt

git add --all
git commit -m "Update"
git pull
git push

del hello_world.txt

git add --all
git commit -m "Update"
git pull
git push

endlocal