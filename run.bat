@echo off
setlocal
echo ==============================================================================
echo  Aegis AI - Enterprise AI Firewall & Autonomous SOC
echo ==============================================================================

set PYTHON_EXEC=python
if exist "venv\Scripts\python.exe" set PYTHON_EXEC=venv\Scripts\python.exe

echo Starting Aegis AI...
%PYTHON_EXEC% -m streamlit run streamlit_app.py --server.headless true --server.port 8501
