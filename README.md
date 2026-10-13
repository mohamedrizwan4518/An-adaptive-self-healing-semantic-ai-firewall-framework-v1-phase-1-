<div align="center">

# Aegis AI
### Adaptive Semantic AI Firewall

**An Adaptive Self-Healing Semantic AI Firewall Framework for Large Language Models**

A team project exploring intelligent detection and mitigation of prompt-based attacks against LLM-powered applications.

<br>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Project](https://img.shields.io/badge/Project-Phase%201-blue?style=flat-square)](#project-information)
[![Version](https://img.shields.io/badge/Version-1.0-green?style=flat-square)](#project-information)

<br>

[Overview](#1-project-overview) ·
[Features](#2-key-features) ·
[Architecture](#3-system-architecture) ·
[Screenshots](#4-application-screenshots) ·
[Installation](#7-getting-started) ·
[Testing](#8-testing-and-validation) ·
[Team](#11-project-team)

</div>

---

# 1. Project Overview

## About Aegis AI

Large Language Models (LLMs) are increasingly used in conversational assistants, intelligent applications, and automated workflows. However, applications using these models can be exposed to prompt injection, jailbreak attempts, system-prompt extraction, role manipulation, and other adversarial inputs.

**Aegis AI** is a cybersecurity project that explores a layered security framework for inspecting incoming prompts, identifying potentially suspicious patterns, evaluating risks, and applying appropriate security decisions.

The project combines lexical threat detection, semantic analysis, prompt sanitization, threat memory, and a Security Operations Center (SOC) dashboard.

It also explores multilingual prompt-security scenarios involving English, Tamil, and Tanglish.

### Project Objectives

- Identify potentially malicious prompts using configured detection rules.
- Analyze suspicious inputs using lexical and semantic techniques.
- Detect prompt injection, jailbreak, and system-prompt extraction attempts.
- Evaluate risks and apply configured security decisions.
- Maintain records of detected threats for further analysis.
- Explore adaptive threat memory for recognizing recurring patterns.
- Provide a dashboard for monitoring security events.
- Evaluate prompt-security behavior across different languages.

### Project Scope

Aegis AI is a development and research prototype. Its effectiveness depends on the implemented detection methods, configuration, and evaluation data.

The project is intended for experimentation, demonstration, and further development. It should not be considered a fully validated production security solution.

---

# 2. Key Features

## 2.1 Lexical Threat Detection

The lexical detection component uses configured patterns and rules to identify potentially suspicious prompt content.

Threat categories of interest include:

- Prompt injection
- Jailbreak attempts
- System-prompt extraction
- Role manipulation
- Safety-policy bypass attempts

Detection coverage depends on the rules implemented in the application.

## 2.2 Semantic Prompt Analysis

The semantic analysis component explores text-similarity techniques to identify potentially suspicious prompts that may use different wording from known examples.

Its intended purposes include:

- Analyzing prompt representations.
- Comparing input against configured threat patterns.
- Supporting risk assessment.
- Investigating paraphrased attack scenarios.

Semantic analysis can produce false positives and false negatives. Its effectiveness must be established through testing.

## 2.3 Prompt Sanitization

The prompt sanitization component provides an additional processing stage for supported security workflows.

Depending on the configured implementation, this stage may inspect suspicious input and apply appropriate transformations before further processing.

Sanitization should not be treated as a guarantee that all malicious intent has been removed.

## 2.4 Adaptive Threat Memory

Threat memory maintains threat-related records that can support the analysis of recurring suspicious patterns.

The project explores how previously observed threats can contribute to subsequent detection and security analysis.

Persistent threat records alone do not establish that a detection model is automatically retrained or improved.

## 2.5 Security Operations Center Dashboard

The SOC dashboard provides an interface for reviewing available security information and administrative workflows.

Depending on the enabled modules, these may include:

- Security-event monitoring
- Threat-category summaries
- Incident information
- User-management controls
- Threat analytics
- Security-record exports

## 2.6 Interactive Security Testing

The testing interface provides a way to experiment with prompts and inspect their security outcomes.

Suggested evaluation categories include:

- Benign prompts
- Prompt injection
- Jailbreak attempts
- System-prompt extraction
- Role manipulation
- Multilingual prompts
- Tamil and Tanglish examples

## 2.7 Authentication and Access Control

The application includes an authentication interface and role-oriented workflows.

Authentication and authorization must be reviewed independently before deploying the application publicly.

---

# 3. System Architecture

Aegis AI explores a layered processing workflow in which incoming prompts are inspected before reaching the configured language-model processing stage.

```mermaid
flowchart TD
    A["User Prompt"] --> B["Input Validation"]

    B --> C["Lexical Threat Detection"]

    C --> D["Semantic Prompt Analysis"]

    D --> E["Risk Evaluation"]

    E --> F{"Security Decision"}

    F -->|Allow| G["Prompt Processing"]

    F -->|Block| H["Reject Request"]

    F -->|Review or Sanitize| I["Additional Security Handling"]

    I --> J{"Policy Result"}

    J -->|Approved| G
    J -->|Rejected| H

    G --> K["LLM Integration, If Configured"]

    K --> L["Response Handling"]

    C -.-> M["Threat Records"]
    D -.-> M
    E -.-> M
    H -.-> M

    M --> N["SOC Dashboard"]
```

### Architecture Components

| Component | Responsibility |
|---|---|
| Input validation | Inspect incoming prompt data. |
| Lexical detection | Match configured suspicious patterns. |
| Semantic analysis | Evaluate similarity to threat patterns. |
| Risk evaluation | Apply configured security decisions. |
| Prompt sanitization | Transform input when supported by the policy. |
| Threat memory | Maintain relevant threat-related records. |
| SOC dashboard | Display available security information. |

**Note:** This diagram represents the conceptual architecture. The actual processing order, integrations, and enforcement behavior depend on the implementation.

---

# 4. Application Screenshots

The following screenshots demonstrate the application's interface and selected workflows.

<table>
<tr>
<td width="50%" align="center">

### SOC Dashboard

<img src="assets/screenshots/soc_dashboard_overview.png" alt="Aegis AI SOC Dashboard" width="100%">

Security monitoring and incident overview.

</td>
<td width="50%" align="center">

### Security Testing Lab

<img src="assets/screenshots/testing_lab_pipeline_full.png" alt="Aegis AI Security Testing Lab" width="100%">

Prompt inspection and security pipeline visualization.

</td>
</tr>
<tr>
<td width="50%" align="center">

### Login Interface

<img src="assets/screenshots/login_screen.png" alt="Aegis AI Login Interface" width="100%">

Authentication and role-oriented workflows.

</td>
<td width="50%" align="center">

### Conversational Interface

<img src="assets/screenshots/user_chat_view.png" alt="Aegis AI Chat Interface" width="100%">

Conversational interaction and security inspection telemetry.

</td>
</tr>
</table>

*Screenshots demonstrate the application interface. Displayed metrics and individual detection outcomes should not be interpreted as independently validated security benchmarks.*

---

# 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and security logic |
| Streamlit | User interface and dashboard |
| FastAPI | Backend API, where configured |
| Scikit-learn | Text-analysis techniques, where implemented |
| Pandas | Data processing, where implemented |
| JSON | Local application data and records |
| Git | Version control |
| GitHub | Source-code hosting |

Additional dependencies and external integrations depend on the application configuration and `requirements.txt`.

---

# 6. Project Structure

The project separates the user interface, backend services, security components, application data, and tests into dedicated directories.

```text
Aegis-AI-Phase1-Version1/
│
├── .streamlit/
│   └── config.toml
│
├── assets/
│   └── screenshots/
│       ├── soc_dashboard_overview.png
│       ├── testing_lab_pipeline_full.png
│       ├── login_screen.png
│       └── user_chat_view.png
│
├── backend/
│   ├── attack_logger.py
│   ├── auth.py
│   ├── blacklist_manager.py
│   ├── dashboard_analytics.py
│   ├── llm_engine.py
│   ├── main.py
│   ├── runner.py
│   ├── threat_engine.py
│   ├── threat_intelligence.py
│   └── user_manager.py
│
├── data/
│
├── experiments/
│
├── frontend/
│   └── app.py
│
├── security/
│   ├── prompt_detector.py
│   ├── prompt_sanitizer.py
│   ├── semantic_detector.py
│   └── threat_memory.py
│
├── tests/
│   └── test_aegis.py
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── run.bat
├── run.ps1
└── streamlit_app.py
```

### Directory and File Descriptions

| Directory or File | Description |
|---|---|
| `.streamlit/` | Streamlit application configuration. |
| `assets/screenshots/` | Application screenshots used in documentation. |
| `backend/` | Backend services, authentication, logging, and management modules. |
| `data/` | Directory for application data and security records. |
| `experiments/` | Directory for experimental work and evaluation. |
| `frontend/` | Streamlit interface and dashboard. |
| `security/` | Prompt detection, sanitization, semantic analysis, and threat memory. |
| `tests/` | Automated tests. |
| `.env.example` | Example environment-variable configuration. |
| `.gitignore` | Specifies files and directories excluded from Git. |
| `LICENSE` | Project license terms. |
| `README.md` | Project documentation. |
| `requirements.txt` | Python package dependencies. |
| `run.bat` | Windows Command Prompt startup script. |
| `run.ps1` | Windows PowerShell startup script. |
| `streamlit_app.py` | Streamlit application entry point. |

*The directory tree reflects the documented project layout. Keep it synchronized with the actual repository. Empty directories may not appear on GitHub.*

---

# 7. Getting Started

Follow these steps to set up Aegis AI locally.

## Prerequisites

Before starting, install:

- Python compatible with the project dependencies.
- Git.
- Visual Studio Code or another code editor.
- PowerShell, Command Prompt, or another compatible terminal.

## Step 1: Clone the Repository

```bash
git clone https://github.com/mohamedrizwan4518/An-adaptive-self-healing-semantic-ai-firewall-framework-v1-phase-1-.git
```

Navigate to the cloned directory:

```bash
cd An-adaptive-self-healing-semantic-ai-firewall-framework-v1-phase-1-
```

## Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```bat
.venv\Scripts\activate.bat
```

### Linux or macOS

```bash
source .venv/bin/activate
```

## Step 3: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

If the application requires environment variables, create a local `.env` file from the example.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux or macOS

```bash
cp .env.example .env
```

Open `.env` and configure the values required by the application.

If an external LLM provider is configured, use the API-key variable expected by the implementation.

**Security reminder:** Never commit real API keys, passwords, access tokens, or production credentials to GitHub.

## Step 5: Launch the Application

### Windows PowerShell

If the startup script is configured for your environment:

```powershell
.\run.ps1
```

Alternatively, launch Streamlit directly:

```bash
streamlit run streamlit_app.py
```

When startup succeeds, Streamlit typically displays a local address similar to:

```text
http://localhost:8501
```

Open that address in your browser.

The backend API and its documentation are available only if the backend starts successfully.

---

# 8. Testing and Validation

The repository includes a test module at:

```text
tests/test_aegis.py
```

Run the tests from the project root:

```bash
python -m unittest tests.test_aegis -v
```

Review the terminal output to determine which tests passed, failed, or encountered errors.

## Recommended Evaluation Metrics

| Metric | Purpose |
|---|---|
| Precision | Measures how many flagged prompts are malicious within the labeled evaluation set. |
| Recall | Measures how many malicious prompts are detected. |
| F1-score | Combines precision and recall into one measure. |
| False-positive rate | Measures benign prompts incorrectly flagged. |
| Detection latency | Measures the time required to inspect a prompt. |
| Language-specific performance | Evaluates behavior across English, Tamil, and Tanglish. |

### Recommended Validation Process

1. Prepare a documented collection of benign and adversarial prompts.
2. Label the examples before evaluating the detector.
3. Run the same test cases against the implementation.
4. Record false positives, false negatives, and processing time.
5. Document the test environment and results.
6. Repeat the evaluation after changing detection rules or models.

Do not report accuracy percentages or claim that every test passes unless the results have been measured and verified.

---

# 9. Security Considerations

Aegis AI is a prototype intended for development, experimentation, and demonstration.

It should not be treated as the sole security boundary for a production LLM application.

Before production deployment, review the following areas:

| Security Area | Considerations |
|---|---|
| Authentication | Password handling and session management. |
| Authorization | Server-side permission checks for privileged actions. |
| Prompt security | Direct and indirect prompt-injection defenses. |
| Secrets | API-key and credential protection. |
| Input handling | Validation of untrusted input. |
| Audit logging | Integrity of records and protection of sensitive data. |
| Abuse prevention | Rate limits and request controls. |
| Threat memory | Integrity and safe handling of stored records. |
| Validation | Testing against realistic attack scenarios. |

### Demo Credentials

If the application contains demonstration accounts, use them only in an isolated demo environment.

Before exposing the application publicly:

- Replace default administrator credentials.
- Verify authentication and authorization.
- Remove sensitive local data.
- Review API-key handling.
- Check whether administrative endpoints are adequately protected.

A security dashboard alone does not guarantee that the underlying application is secure.

---

# 10. Deployment

The repository includes the Streamlit entry point:

```text
streamlit_app.py
```

Streamlit Community Cloud may be suitable for hosting the interface, depending on the application's requirements.

### Pre-Deployment Checklist

- [ ] Confirm that the application runs locally.
- [ ] Verify dependency compatibility.
- [ ] Configure secrets through the hosting platform.
- [ ] Check backend startup requirements.
- [ ] Review file-system and data-persistence behavior.
- [ ] Test authentication and access controls.
- [ ] Verify screenshot and resource paths.
- [ ] Test the deployed application.

A successful local run does not guarantee that the application will work identically in a hosted environment.

Backend processes, external model integrations, persistent storage, and hosting restrictions must be evaluated separately.

Do not expose demonstration credentials or sensitive local data in a public deployment.

---

# 11. Future Roadmap

The following items represent potential improvements for future development.

- [ ] Expand the labeled prompt-attack dataset.
- [ ] Evaluate precision, recall, and F1-score.
- [ ] Measure false-positive rates and detection latency.
- [ ] Improve Tamil and Tanglish evaluation coverage.
- [ ] Enhance explanations for security decisions.
- [ ] Add regression tests for known attack patterns.
- [ ] Strengthen authentication and authorization.
- [ ] Improve security-event reporting.
- [ ] Evaluate concurrent-request performance.
- [ ] Document threat models and limitations.
- [ ] Validate deployment and storage requirements.

These items are proposed future enhancements, not claims that the functionality is already implemented.

---

# 12. Project Team

## Team Aegis AI

Aegis AI is a collaborative team project focused on exploring security techniques for Large Language Model applications.

### Team Members

| No. | Name |
|:---:|---|
| 1 | **HARIHARAN V.S.** |
| 2 | **RASHIKA V.** |
| 3 | **RUBINI T.** |

### Project Information

| Category | Details |
|---|---|
| Project Name | Aegis AI — Adaptive Semantic AI Firewall |
| Project Type | Team Project |
| Project Phase | Phase 1 |
| Version | 1.0 |
| Domain | Artificial Intelligence and Cybersecurity |
| Institution | Achariya College of Engineering and Technology |
| Location | Puducherry, India |

### Team Approach

The project brings together collaborative problem-solving, software development, security experimentation, and documentation.

The team is exploring how layered detection, semantic analysis, and risk-based decisions can contribute to the protection of applications powered by Large Language Models.

Individual responsibilities can be documented once the team's roles have been finalized.

---

# 13. Project Repository

**GitHub Repository:**

[An-adaptive-self-healing-semantic-ai-firewall-framework-v1-phase-1-](https://github.com/mohamedrizwan4518/An-adaptive-self-healing-semantic-ai-firewall-framework-v1-phase-1-)

The repository contains the project source code, configuration, documentation, and available tests.

---

# 14. License

This repository contains a [`LICENSE`](LICENSE) file.

Refer to that file for the applicable license terms.

---

<div align="center">

**AEGIS AI — Adaptive Semantic AI Firewall**

*Detect suspicious inputs. Evaluate risks. Strengthen defenses.*

**Team Aegis AI**

HARIHARAN V.S. · RASHIKA V. · RUBINI T.

</div>
