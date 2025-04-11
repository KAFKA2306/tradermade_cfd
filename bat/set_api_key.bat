@echo off
setlocal

REM Check if API key is already set
if defined TRADERMADE_API_KEY (
  echo API key is already set.
  goto :eof
)

REM Prompt for API key and secret key
set /p API_KEY="Enter Tradermade API key: "

REM Set API key in environment variables (temporary)
set TRADERMADE_API_KEY=%API_KEY%

REM Set API key in environment variables (permanent)
setx TRADERMADE_API_KEY "%API_KEY%" /M

echo Tradermade API key has been set.

endlocal