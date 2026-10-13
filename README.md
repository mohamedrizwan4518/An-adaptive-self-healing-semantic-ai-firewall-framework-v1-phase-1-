# 🛡️ Aegis AI — Enterprise AI Firewall & Autonomous SOC

**Aegis AI** is an enterprise-grade Autonomous Cybersecurity Firewall and Security Operations Center (SOC) designed to protect Large Language Models (LLMs) from real-time adversarial prompt injection, jailbreaks, data exfiltration, system prompt leaks, and role manipulation across multilingual vectors (English, Tamil, and Tanglish).

---

## 📸 System Screenshots

| **Enterprise SOC Dashboard Overview** | **Interactive 5-Stage Security Pipeline** |
| :---: | :---: |
| ![SOC Dashboard](assets/screenshots/soc_dashboard_overview.png) | ![Security Pipeline Lab](assets/screenshots/testing_lab_pipeline_full.png) |

| **Authentication & Role-Based Access** | **User Conversational Inspection Telemetry** |
| :---: | :---: |
| ![Login Screen](assets/screenshots/login_screen.png) | ![User Chat View](assets/screenshots/user_chat_view.png) |

---

## 🌟 Key Architecture & Capabilities

1. **Dual-Engine Threat Detection Pipeline**:
   - **Lexical Gatekeeper**: High-throughput rule matcher covering 80+ known adversarial signatures.
   - **Semantic Cosine Engine**: Sub-word N-gram TF-IDF & Neural Cosine similarity detector capable of identifying zero-day paraphrased and transliterated attacks without OS DLL restrictions.
2. **Adaptive Self-Healing Threat Memory**:
   - Autonomously stores intercepted adversarial patterns into persistent memory, continuously hardening the firewall against repeat vectors.
3. **In-Flight Prompt Neutralization (Sanitizer)**:
   - Sanitizes and neutralizes medium-risk prompts before reaching the model, transforming malicious intent into safe inquiries.
4. **Interactive Security Testing Lab**:
   - 1-Click test battery covering all primary LLM attack surfaces (Prompt Injection, Jailbreak/DAN, System Prompt Extraction, Role Manipulation, Safety Bypass, Multilingual Tamil/Tanglish, and Benign Prompts).
   - Real-time 5-stage pipeline breakdown visualizer (`Lexical Gate` ➔ `Semantic Vector` ➔ `Sanitizer Engine` ➔ `Decision Gate` ➔ `Output Verdict`).
5. **Next-Gen Cybersecurity SOC Dashboard**:
   - **Level 1 (Threat Triage)**: Real-time incident feed with 1-click administrative actions (Warn, Block, Blacklist, Restore).
   - **Level 2 & 4 (Threat Intelligence)**: Executive KPI cards, categorical attack distribution, adversarial account metrics, and CSV compliance export.
   - **Level 3 & 5 (Security Ledger & User Control)**: Comprehensive user directory, risk scores (0–100), warning counters, and access policy enforcement.

---

## ☁️ Deploying to Streamlit Community Cloud

Aegis AI is preconfigured for single-click deployment on [Streamlit Community Cloud](https://share.streamlit.io):

1. **Push this repository to GitHub** (see [GitHub Setup](#-pushing-to-github)).
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/) and click **New app**.
3. Select your repository, branch (`main`), and set **Main file path** to:
   ```text
   streamlit_app.py
   ```
4. Click **Advanced settings...** and add your Groq API key to **Secrets**:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key_here"
   ```
5. Click **Deploy!** — The application automatically boots the background FastAPI security engine and mounts the SOC Dashboard in a unified environment.

---

## 🚀 Local Quick Start

### 1. Clone & Setup Environment
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure your API key
copy .env.example .env     # Windows
cp .env.example .env       # Linux / macOS
# Edit .env and insert your GROQ_API_KEY
```

### 2. Launch the Application

#### Windows (Easiest Way)
```powershell
.\run.ps1
# or in Command Prompt:
run.bat
```

#### Manual / Cross-Platform
```bash
streamlit run streamlit_app.py
```
* **Web Application UI**: `http://localhost:8501`
* **FastAPI Backend Server**: `http://127.0.0.1:8000` (auto-started)
* **Interactive OpenAPI Swagger Docs**: `http://127.0.0.1:8000/docs`

---

## 🧪 Automated Testing & Audit Suite

Run the comprehensive unit and integration test suite verifying all 9 security gates, authentication, user lifecycle, and detection pipelines:

```bash
python -m unittest tests/test_aegis.py -v
```

All 9 tests pass with exit code 0:
- `test_01_health_and_root`
- `test_02_authentication`
- `test_03_user_security_lifecycle`
- `test_04_prompt_detector_multilingual`
- `test_05_semantic_detector`
- `test_06_prompt_sanitizer`
- `test_07_chat_endpoint_security_pipeline`
- `test_08_analytics_and_threat_intelligence`
- `test_09_threat_memory_management`

---

## 👥 Demo Accounts (1-Click Login in UI)

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **SOC Administrator** | `admin` | `admin123` | Full administrative control, live threat triage, analytics, user policy |
| **Standard User** | `hari` | `user123` | Safe conversational chat with real-time security inspection telemetry |
| **Simulated Attacker** | `rashi` | `user1234` | Adversarial payload simulation and quota testing |

---

## 📂 Repository Structure

```text
├── .streamlit/
│   └── config.toml             # Streamlit theme & server options
├── assets/
│   └── screenshots/            # Curated UI demonstration captures
├── backend/
│   ├── attack_logger.py        # Attack logging & persistence
│   ├── auth.py                 # User authentication & role management
│   ├── blacklist_manager.py    # IP/user blacklist manager
│   ├── dashboard_analytics.py  # Aggregated metrics & SOC telemetry
│   ├── llm_engine.py           # Multi-provider LLM & Groq integration
│   ├── main.py                 # FastAPI application & security endpoints
│   ├── runner.py               # Auto-supervisor for single-process deployments
│   ├── threat_engine.py        # Risk score calculation & heuristics
│   ├── threat_intelligence.py  # Trend analytics & incident reports
│   └── user_manager.py         # User status, warnings & block policies
├── data/
│   ├── attacks.json            # Attack incidents database
│   ├── blacklist.json          # Blacklisted entities
│   ├── blocked_users.json      # Blocked users ledger
│   ├── threat_memory.json      # Adaptive threat memory storage
│   ├── users.json              # System users database
│   └── warnings.json           # User warnings log
├── frontend/
│   └── app.py                  # Full Cyber SOC & Testing Lab Dashboard (Streamlit)
├── security/
│   ├── prompt_detector.py      # Lexical signature pattern matcher
│   ├── prompt_sanitizer.py     # In-flight neutralizing engine
│   ├── semantic_detector.py    # Sub-word TF-IDF / Neural cosine detector
│   └── threat_memory.py        # Self-healing threat memory manager
├── tests/
│   └── test_aegis.py           # 9-Gate integration & unit test suite
├── .env.example                # Safe environment variables template
├── .gitignore                  # Git ignore rules (protects .env & venv)
├── README.md                   # Project documentation
├── requirements.txt            # Python production dependencies
├── run.bat                     # Windows cmd quick-start script
├── run.ps1                     # Windows PowerShell quick-start script
└── streamlit_app.py            # Streamlit Cloud root entrypoint
```

---

## 📤 Pushing to GitHub

Follow these steps to push to your GitHub repository:

```bash
# 1. Initialize local repository and set branch to main
git init -b main

# 2. Stage all clean project files (.env & venv are automatically excluded)
git add .

# 3. Commit your initial release
git commit -m "feat: Aegis AI Enterprise Firewall & Autonomous SOC v2.5.0"

# 4. Add your GitHub remote repository (replace with your URL)
git remote add origin https://github.com/<your-username>/<your-repo-name>.git

# 5. Push to GitHub
git push -u origin main
```
