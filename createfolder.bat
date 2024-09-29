@echo off
REM Batch script to create E:\project\ directory structure

REM Define the project path
SET "PROJECT_PATH=E:\project"

REM Create the project directory if it doesn't exist
IF NOT EXIST "%PROJECT_PATH%" (
    mkdir "%PROJECT_PATH%"
    echo Created directory: %PROJECT_PATH%
) ELSE (
    echo Directory already exists: %PROJECT_PATH%
)

REM Navigate to the project directory
cd /d "%PROJECT_PATH%"

REM List of Python files to create
SET FILES=main.py inserturl.py downloadsoftware.py downloadthread.py installer.py config.py logger_config.py utilities.py

REM Create Python files
FOR %%F IN (%FILES%) DO (
    IF NOT EXIST "%%F" (
        type nul > "%%F"
        echo Created file: %%F
    ) ELSE (
        echo File already exists: %%F
    )
)

REM Create additional files
SET ADDITIONAL_FILES=config.json software_urls.txt

FOR %%F IN (%ADDITIONAL_FILES%) DO (
    IF NOT EXIST "%%F" (
        type nul > "%%F"
        echo Created file: %%F
    ) ELSE (
        echo File already exists: %%F
    )
)

REM Create the downloads directory
IF NOT EXIST "%PROJECT_PATH%\downloads" (
    mkdir "%PROJECT_PATH%\downloads"
    echo Created directory: %PROJECT_PATH%\downloads
) ELSE (
    echo Directory already exists: %PROJECT_PATH%\downloads
)

echo.
echo Directory structure setup complete.
pause
