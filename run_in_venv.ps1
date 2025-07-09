# HINT: If the current PowerShell execution policy 
#       does not allow running this script, execute 
#       the following command first:
#
# ```Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser```


# Activate the virtual environment
if (Test-Path .\env\Scripts\Activate.ps1) {
    .\env\Scripts\Activate.ps1
} else {
    Write-Host "Virtual environment not found. Creating a new one..." -ForegroundColor Yellow
    py -m venv env
    if (Test-Path .\env\Scripts\Activate.ps1) {
        .\env\Scripts\Activate.ps1
        if (Test-Path .\requirements.txt) {
            python -m pip install -r .\requirements.txt
        } else {
            Write-Host "requirements.txt not found. Skipping package installation." -ForegroundColor Yellow
        }
    } else {
        Write-Host "Failed to create the virtual environment." -ForegroundColor Red
        exit 1
    }
}

# Run the Python script
try {
    python .\main.py
} catch {
    Write-Host "Failed to execute the Python script. Please check for errors." -ForegroundColor Red
    exit 1
}

# Deactivate the virtual environment
if ($env:VIRTUAL_ENV) {
    deactivate
    Write-Host "Virtual environment deactivated." -ForegroundColor Green
} else {
    Write-Host "No active virtual environment detected." -ForegroundColor Yellow
}

# Script completed
Write-Host "Script execution completed." -ForegroundColor Green
