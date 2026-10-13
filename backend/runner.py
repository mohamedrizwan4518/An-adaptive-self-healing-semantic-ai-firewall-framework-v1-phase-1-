"""
Aegis AI — Backend Process & Service Supervisor
Ensures the FastAPI backend is seamlessly running for both local and Streamlit Community Cloud environments.
"""

import os
import sys
import socket
import time
import subprocess
import threading
import urllib.request
from pathlib import Path
from typing import Optional

_BACKEND_PROCESS: Optional[subprocess.Popen] = None
_BACKEND_LOCK = threading.Lock()


def sync_streamlit_secrets() -> None:
    """Sync Streamlit secrets to environment variables if running in Streamlit."""
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            for key in ["GROQ_API_KEY", "AEGIS_API_BASE", "API_BASE"]:
                if key in st.secrets and not os.getenv(key):
                    os.environ[key] = str(st.secrets[key])
    except Exception:
        pass


def is_backend_healthy(host: str = "127.0.0.1", port: int = 8000, timeout: float = 0.6) -> bool:
    """Check if the backend is actively listening and responding to health queries."""
    try:
        req = urllib.request.Request(f"http://{host}:{port}/health")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                return s.connect_ex((host, port)) == 0
        except Exception:
            return False


def ensure_backend_running(host: str = "127.0.0.1", port: int = 8000) -> bool:
    """
    Guarantees that the FastAPI backend is operational.
    If the backend is not running on (host, port), spawns it in a background process/thread.
    """
    global _BACKEND_PROCESS

    sync_streamlit_secrets()

    # If already responsive, nothing to do
    if is_backend_healthy(host, port):
        return True

    with _BACKEND_LOCK:
        # Re-check after acquiring lock to prevent double-spawning
        if is_backend_healthy(host, port):
            return True

        project_root = Path(__file__).resolve().parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        env = os.environ.copy()
        env["PYTHONPATH"] = str(project_root)

        # Attempt 1: Subprocess invocation (preferred for process isolation)
        try:
            cmd = [
                sys.executable,
                "-m",
                "uvicorn",
                "backend.main:app",
                "--host",
                host,
                "--port",
                str(port),
                "--log-level",
                "warning"
            ]
            _BACKEND_PROCESS = subprocess.Popen(
                cmd,
                cwd=str(project_root),
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as proc_err:
            print(f"[Aegis AI] Notice: Subprocess launch failed ({proc_err}). Falling back to daemon thread.")
            
            # Attempt 2: Daemon thread fallback
            def _thread_target():
                try:
                    import asyncio
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    import uvicorn
                    from backend.main import app
                    config = uvicorn.Config(app=app, host=host, port=port, log_level="warning")
                    server = uvicorn.Server(config)
                    loop.run_until_complete(server.serve())
                except Exception as th_err:
                    print(f"[Aegis AI] Daemon thread server error: {th_err}")

            th = threading.Thread(target=_thread_target, daemon=True)
            th.start()

        # Poll until backend is active (up to 8 seconds)
        for _ in range(40):
            if is_backend_healthy(host, port):
                return True
            time.sleep(0.2)

        return is_backend_healthy(host, port)
