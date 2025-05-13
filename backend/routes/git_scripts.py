from fastapi import APIRouter, Query
import os
import asyncio
import subprocess
import logging
import traceback
from pathlib import Path
from dotenv import load_dotenv

backend_dir = Path(__file__).resolve().parent.parent

# Construct path to .env file
env_path = backend_dir / '.env'

# Load the environment variables
load_dotenv(env_path)

BASE_DIRECTORY_SCRIPTS = os.getenv('BASE_DIRECTORY_SCRIPTS')
router = APIRouter()

# Create a semaphore to limit concurrent processes
# The parameter determines how many processes can run simultaneously
# Setting it to 1 ensures strict sequential execution
process_semaphore = asyncio.Semaphore(1)

@router.get('/daily_commits')
async def get_daily_commits(directories: list[str] = Query(..., description="List of Git repository paths")):
    results = []
    # Use asyncio.gather to run directories sequentially
    async def process_directory(directory):
        async with process_semaphore:
            try:
                # Normalize and validate the directory path
                normalized_directory = os.path.normpath(os.path.expanduser(directory))

                # Verify directory exists
                if not os.path.exists(normalized_directory):
                    return {
                        "directory": normalized_directory,
                        "error": "Directory does not exist",
                        "returncode": 1
                    }
                print(f"Processing directory: {normalized_directory}")
                # Define the batch file path
                bat_file = rf'{BASE_DIRECTORY_SCRIPTS}\commitDaily.bat'
                print(bat_file)
                # Use asyncio.to_thread to run subprocess in a separate thread
                # This prevents blocking the event loop
                process = await asyncio.to_thread(
                    subprocess.run,
                    ["cmd.exe", "/c", bat_file, normalized_directory],
                    capture_output=True,
                    text=True,
                    cwd=normalized_directory
                )


                return {
                    "directory": normalized_directory,
                    "stdout": process.stdout.strip(),
                    "stderr": process.stderr.strip(),
                    "returncode": process.returncode
                }

            except Exception as e:
                logging.error(f"Detailed error: {traceback.format_exc()}")
                return {
                    "directory": directory,
                    "error": str(e),
                    "traceback": traceback.format_exc(),
                    "returncode": 1
                }
    # Process directories one at a time
    results = await asyncio.gather(*[process_directory(directory) for directory in directories])
    print(results)
    return results