@echo off
echo Finding process using port 8000...
netstat -ano | findstr :8000
echo.
echo Killing process on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a
)
echo Done! Now try starting the server again.
pause

