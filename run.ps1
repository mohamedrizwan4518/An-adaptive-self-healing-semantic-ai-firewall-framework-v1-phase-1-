Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host " Aegis AI - Enterprise AI Firewall & Autonomous SOC" -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan

$PythonExec = "python"
if (Test-Path ".\venv\Scripts\python.exe") {
    $PythonExec = ".\venv\Scripts\python.exe"
}

Write-Host "Starting Aegis AI..." -ForegroundColor Green
& $PythonExec -m streamlit run streamlit_app.py --server.headless true --server.port 8501
