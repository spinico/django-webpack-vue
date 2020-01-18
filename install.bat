@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION
CLS

IF NOT EXIST "%PYTHONHOME%" ( GOTO:NoPythonHome )

SET "venv=%CD%\.venv"

IF NOT EXIST "!venv!" (
    ECHO Setup new virtual environment...
    ECHO.

    "%PYTHONHOME%\python" -m venv "%venv%"

    "%venv%\Scripts\python" -m pip install --upgrade pip setuptools

    "%venv%\Scripts\pip" install -r requirements.txt
)

PUSHD backend
CALL npm install
POPD

PUSHD frontend
CALL npm install
CALL npm run build
POPD

GOTO:End

:NoPythonHomeDefined
ECHO The PYTHONHOME environment variable is not set or its value is not valid.
GOTO:End

:End
ECHO.
ECHO Press a key to terminate...
PAUSE >NUL
GOTO:EOF
