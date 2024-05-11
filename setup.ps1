Write-Host "---Setting up server---"
Write-Host "Creating virtual environment"
Set-Location server
python -m venv venv

Write-Host "Activating virtual environment"
. .\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies"
pip install -r requirements.txt

Write-Host "Run the application with 'cd server; .\venv\Scripts\Activate.ps1; python doggo_server.py'"
deactivate

Set-Location ..

Write-Host "---Setting up test client---"
Write-Host "Creating virtual environment"
Set-Location test_client
python -m venv venv

Write-Host "Activating virtual environment"
. .\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies"
pip install -r requirements.txt

Write-Host "Run the test client application with 'cd test_client; .\venv\Scripts\Activate.ps1; python main.py'"
deactivate

Set-Location ..
