"""
Aegis AI — Enterprise AI Firewall & Autonomous SOC
Streamlit Community Cloud & Local Deployment Entrypoint
"""

import os
import sys
import runpy
from pathlib import Path

# Ensure workspace root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Ensure FastAPI backend server is operational (critical for single-container Streamlit Cloud)
from backend.runner import ensure_backend_running
ensure_backend_running()

# Delegate execution to the main frontend application
frontend_script = str(ROOT_DIR / "frontend" / "app.py")
runpy.run_path(frontend_script, run_name="__main__")
