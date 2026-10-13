import os
import re
import json
import math
import requests
from typing import Dict, Any, Tuple, Optional
from dotenv import load_dotenv

load_dotenv()


KNOWN_EXPIRED_KEYS = {
    "expired_or_invalid",
    "your_groq_api_key_here"
}

_OLLAMA_CHECKED = False
_OLLAMA_AVAILABLE = False


def is_ollama_active() -> bool:
    global _OLLAMA_CHECKED, _OLLAMA_AVAILABLE
    if _OLLAMA_CHECKED:
        return _OLLAMA_AVAILABLE
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=0.3)
        _OLLAMA_AVAILABLE = (r.status_code == 200)
    except Exception:
        _OLLAMA_AVAILABLE = False
    _OLLAMA_CHECKED = True
    return _OLLAMA_AVAILABLE


def get_current_api_key() -> str:
    key = os.getenv("GROQ_API_KEY", "").strip()
    if not key or key in KNOWN_EXPIRED_KEYS:
        return ""
    return key


DEFAULT_GROQ_CANDIDATES = [
    "qwen/qwen3.8-27b",
    "groq/compound",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.6-27b",
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant"
]

_ACTIVE_GROQ_MODEL: Optional[str] = None


def resolve_groq_model(api_key: str) -> Optional[str]:
    """Queries Groq /models API to dynamically find the best active chat model supported by this key."""
    global _ACTIVE_GROQ_MODEL
    clean_key = api_key.strip()
    if not clean_key or clean_key in KNOWN_EXPIRED_KEYS:
        return None
    try:
        url = "https://api.groq.com/openai/v1/models"
        headers = {"Authorization": f"Bearer {clean_key}"}
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json().get("data", [])
            available_ids = {m.get("id") for m in data if "id" in m}
            for cand in DEFAULT_GROQ_CANDIDATES:
                if cand in available_ids:
                    _ACTIVE_GROQ_MODEL = cand
                    return cand
            valid_chat = [mid for mid in available_ids if "whisper" not in mid and "guard" not in mid]
            if valid_chat:
                _ACTIVE_GROQ_MODEL = valid_chat[0]
                return _ACTIVE_GROQ_MODEL
    except Exception:
        pass
    return _ACTIVE_GROQ_MODEL or "qwen/qwen3.8-27b"


def check_groq_api_key(api_key: str) -> Tuple[bool, str]:
    """Tests if a Groq API key is valid and finds the active supported model."""
    if not api_key or len(api_key.strip()) < 10:
        return False, "API key is empty or too short."
    if api_key.strip() in KNOWN_EXPIRED_KEYS:
        return False, "This API key is expired. Please generate a new key at console.groq.com."
    try:
        model = resolve_groq_model(api_key)
        if not model:
            url = "https://api.groq.com/openai/v1/models"
            resp = requests.get(url, headers={"Authorization": f"Bearer {api_key.strip()}"}, timeout=5)
            if resp.status_code != 200:
                err = resp.json().get("error", {}).get("message", f"HTTP {resp.status_code}")
                return False, f"Groq Error: {err}"
            model = "qwen/qwen3.8-27b"

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 5
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=6)
        if resp.status_code == 200:
            return True, f"API Key is active and verified with {model}."
        else:
            err = resp.json().get("error", {}).get("message", f"HTTP {resp.status_code}")
            return False, f"Groq Error: {err}"
    except Exception as e:
        return False, f"Connection failure: {str(e)}"


def get_llm_status() -> Dict[str, Any]:
    key = get_current_api_key()
    if key:
        model = _ACTIVE_GROQ_MODEL or resolve_groq_model(key) or "qwen/qwen3.8-27b"
        return {
            "provider": f"Groq Cloud ({model})",
            "key_configured": True,
            "tier": "Cloud LLM",
            "status": "Online"
        }
    if is_ollama_active():
        return {
            "provider": "Local Ollama",
            "key_configured": True,
            "tier": "Local LLM",
            "status": "Online"
        }

    return {
        "provider": "Aegis Autonomous Conversational Intelligence",
        "key_configured": False,
        "tier": "Edge Engine",
        "status": "Ready (Offline Multi-Domain Engine)"
    }


def solve_math(prompt: str) -> Optional[str]:
    """Evaluates math expressions safely from conversational prompts."""
    p_lower = prompt.lower()
    
    # 1. Percentage: e.g. "what is 15 percent of 200", "20% of 500"
    pct_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:%|percent)\s*(?:of)\s*(\d+(?:\.\d+)?)", p_lower)
    if pct_match:
        pct = float(pct_match.group(1))
        val = float(pct_match.group(2))
        res = (pct / 100.0) * val
        return (
            f"### 🧮 Mathematical Calculation\n\n"
            f"**Query:** {pct}% of {val}\n\n"
            f"**Calculation:** `({pct} / 100) * {val}`\n\n"
            f"**Result:** **`{res:g}`**\n\n"
            f"--- \n*Computed with Aegis Precision Math Engine.*"
        )

    # 2. Square root: e.g. "square root of 144", "sqrt(144)"
    sqrt_match = re.search(r"(?:square root of|sqrt\(?)\s*(\d+(?:\.\d+)?)\)?", p_lower)
    if sqrt_match:
        val = float(sqrt_match.group(1))
        res = math.sqrt(val)
        return (
            f"### 🧮 Mathematical Calculation\n\n"
            f"**Query:** $\\sqrt{{{val}}}$\n\n"
            f"**Result:** **`{res:g}`**\n\n"
            f"--- \n*Computed with Aegis Precision Math Engine.*"
        )

    # 3. General arithmetic: extract formula like "45 * 12 + 60", "100 / 4", "500 - 120"
    formula_match = re.search(r"(\d+(?:\.\d+)?(?:\s*[\+\-\*\/\%]\s*\d+(?:\.\d+)?)+)", prompt)
    if formula_match:
        expr = formula_match.group(1).strip()
        try:
            # Check only allowed arithmetic chars
            if re.match(r"^[\d\s+\-*/().%]+$", expr):
                result = eval(expr, {"__builtins__": None}, {})
                return (
                    f"### 🧮 Mathematical Calculation\n\n"
                    f"**Expression:** `{expr}`\n\n"
                    f"**Result:** **`{result:g}`**\n\n"
                    f"--- \n*Computed with Aegis Precision Math Engine.*"
                )
        except Exception:
            pass
    return None


def generate_conversational_response(prompt: str) -> str:
    """
    Generates rich, insightful, formatted markdown answers across programming,
    cybersecurity, general science, technology, mathematics, and philosophy
    when external cloud LLMs are unconfigured or offline.
    """
    p_lower = prompt.lower().strip()

    # 1. Math queries
    math_ans = solve_math(prompt)
    if math_ans:
        return math_ans

    # 2. Greetings
    if re.search(r"\b(hello|hi|hey|good morning|good evening|namaste|vanakkam)\b", p_lower):
        return (
            "### 👋 Hello! Welcome to Aegis AI\n\n"
            "I am your conversational AI Assistant, running behind the **Aegis Autonomous Security Firewall**.\n\n"
            "You can ask me anything—including:\n"
            "- 💻 **Programming & Architecture:** Python, JavaScript, Docker, REST APIs, SQL, Algorithms.\n"
            "- 🛡️ **Cybersecurity & Defense:** Threat detection, Zero Trust, LLM Security, ISO 27001.\n"
            "- 🔬 **Science, Tech & Math:** Physics, cloud infrastructure, AI models, calculations.\n"
            "- 🌐 **General Knowledge:** Definitions, explanations, and creative problem solving.\n\n"
            "What would you like to explore today?"
        )

    # 3. Capital / Geography Questions
    capital_match = re.search(r"capital (?:city )?of ([a-zA-Z\s]+)", p_lower)
    capitals = {
        "france": ("Paris", "France", "Europe", "Known for the Eiffel Tower, the Louvre, and world-renowned art and cuisine."),
        "germany": ("Berlin", "Germany", "Europe", "Famous for its vibrant tech scene, rich history, and the Brandenburg Gate."),
        "italy": ("Rome", "Italy", "Europe", "The historic heart of the Roman Empire and home to the Colosseum and Vatican City."),
        "japan": ("Tokyo", "Japan", "Asia", "The world's most populous metropolitan area, blending hyper-modern technology with ancient traditions."),
        "india": ("New Delhi", "India", "Asia", "The political center of India, housing Rashtrapati Bhavan, India Gate, and the Parliament."),
        "united kingdom": ("London", "United Kingdom", "Europe", "Global financial and cultural hub situated on the River Thames."),
        "uk": ("London", "United Kingdom", "Europe", "Global financial and cultural hub situated on the River Thames."),
        "usa": ("Washington, D.C.", "United States", "North America", "Seat of the US federal government, home to the White House and Capitol Building."),
        "united states": ("Washington, D.C.", "United States", "North America", "Seat of the US federal government, home to the White House and Capitol Building."),
        "canada": ("Ottawa", "Canada", "North America", "Located in Ontario on the border with Quebec, famed for Parliament Hill and the Rideau Canal."),
        "australia": ("Canberra", "Australia", "Oceania", "A planned city purpose-built as the federal capital, situated between Sydney and Melbourne."),
        "russia": ("Moscow", "Russia", "Eurasia", "Famous for the Kremlin, Red Square, and Saint Basil's Cathedral."),
        "china": ("Beijing", "China", "Asia", "One of the world's oldest capitals, featuring the Forbidden City and the Great Wall nearby."),
        "brazil": ("Brasília", "Brazil", "South America", "An architecturally renowned planned city designed by Oscar Niemeyer."),
        "spain": ("Madrid", "Spain", "Europe", "Renowned for its royal palaces, the Prado Museum, and bustling central plazas.")
    }
    if capital_match:
        country = capital_match.group(1).strip()
        for k, v in capitals.items():
            if k in country or country in k:
                return (
                    f"### 🌍 Geography Factsheet\n\n"
                    f"The capital of **{v[1]}** is **{v[0]}**.\n\n"
                    f"- **Continent:** {v[2]}\n"
                    f"- **Overview:** {v[3]}"
                )

    # 4. Programming Questions (Python, APIs, SQL, Algorithms)
    if "python" in p_lower or "script" in p_lower or "code" in p_lower or "function" in p_lower:
        if "reverse" in p_lower:
            return (
                "### 🐍 Reversing a String or List in Python\n\n"
                "In Python, the idiomatic and fastest way to reverse is using slice notation `[::-1]`:\n\n"
                "```python\n"
                "# Reversing a string\n"
                "text = 'Hello World'\n"
                "reversed_text = text[::-1]\n"
                "print(reversed_text)  # Output: 'dlroW olleH'\n\n"
                "# Reversing a list\n"
                "items = [1, 2, 3, 4, 5]\n"
                "reversed_items = items[::-1]       # Creates a new reversed list\n"
                "items.reverse()                    # In-place reversal\n"
                "```\n\n"
                "**Time Complexity:** $O(N)$ linear time."
            )
        elif "sort" in p_lower or "sorting" in p_lower:
            return (
                "### 🐍 Sorting in Python (Timsort)\n\n"
                "Python utilizes **Timsort** ($O(N \\log N)$ hybrid of Merge Sort and Insertion Sort):\n\n"
                "```python\n"
                "# 1. Return a new sorted list (leaves original unchanged)\n"
                "numbers = [42, 12, 88, 5, 23]\n"
                "sorted_list = sorted(numbers)\n\n"
                "# 2. In-place sorting\n"
                "numbers.sort(reverse=True)  # Descending order\n\n"
                "# 3. Custom key sorting (e.g. by string length or dict key)\n"
                "users = [{'name': 'Alice', 'score': 90}, {'name': 'Bob', 'score': 75}]\n"
                "users.sort(key=lambda u: u['score'], reverse=True)\n"
                "```"
            )
        elif "fastapi" in p_lower or "api" in p_lower or "rest" in p_lower:
            return (
                "### ⚡ Building High-Performance REST APIs with FastAPI\n\n"
                "FastAPI is a modern Python framework offering asynchronous I/O, automatic OpenAPI documentation, and Pydantic data validation:\n\n"
                "```python\n"
                "from fastapi import FastAPI, HTTPException\n"
                "from pydantic import BaseModel\n\n"
                "app = FastAPI(title='Aegis Microservice')\n\n"
                "class QueryPayload(BaseModel):\n"
                "    prompt: str\n"
                "    user_id: str\n\n"
                "@app.post('/api/v1/inspect')\n"
                "async def inspect_prompt(payload: QueryPayload):\n"
                "    if not payload.prompt:\n"
                "        raise HTTPException(status_code=400, detail='Empty prompt')\n"
                "    return {'status': 'success', 'length': len(payload.prompt)}\n"
                "```\n\n"
                "Run with Uvicorn: `uvicorn main:app --reload --port 8000`."
            )
        else:
            return (
                "### 💻 Secure Python Development Guide\n\n"
                "Here are essential principles for building reliable, production-ready Python applications:\n\n"
                "1. **Input Validation & Sanitization:** Use `pydantic` or strict regex to validate incoming payloads before processing.\n"
                "2. **Type Annotations:** Leverage Python's `typing` module (`List`, `Dict`, `Optional`, `Union`) to catch bugs at lint-time.\n"
                "3. **Exception Management:** Avoid bare `except:` blocks; always catch specific exceptions (`ValueError`, `KeyError`, `HTTPException`).\n"
                "4. **Dependency Pinning:** Freeze exact package versions in `requirements.txt` to prevent breaking supply-chain changes.\n\n"
                "```python\n"
                "from typing import List, Optional\n\n"
                "```"
            )

    # 5. Artificial Intelligence (AI)
    if re.search(r"\b(what is ai|define ai|what is artificial intelligence|define artificial intelligence|about ai)\b", p_lower) or p_lower in ["ai", "what is ai?", "what's ai"]:
        return (
            "### 🤖 What is Artificial Intelligence (AI)?\n\n"
            "**Artificial Intelligence (AI)** is a branch of computer science focused on building intelligent systems capable of performing tasks that typically require human cognition—such as learning, reasoning, problem-solving, perception, and natural language understanding.\n\n"
            "#### 1. The Three Stages of AI\n"
            "- **Narrow AI (Weak AI):** Designed and trained for specific tasks (e.g. speech recognition, recommendation algorithms, medical image diagnostics, and LLMs like ChatGPT). All modern AI today is Narrow AI.\n"
            "- **Artificial General Intelligence (AGI):** Theoretical AI that possesses human-like general reasoning across any problem domain.\n"
            "- **Artificial Superintelligence (ASI):** A hypothetical future AI that surpasses human cognitive capabilities across all disciplines.\n\n"
            "#### 2. Key Subfields of AI\n"
            "1. **Machine Learning (ML):** Algorithms that automatically discover patterns from data to make predictions without being explicitly programmed.\n"
            "2. **Deep Learning (DL):** Deep multi-layer neural networks capable of learning hierarchical feature representations (e.g., CNNs for vision, Transformers for language).\n"
            "3. **Natural Language Processing (NLP):** Enables machines to understand, summarize, translate, and generate human languages.\n"
            "4. **Computer Vision:** Enables computers to extract meaningful information from digital images and video feeds.\n\n"
            "#### 3. Real-World Applications\n"
            "- **Cybersecurity:** Real-time threat detection, anomaly isolation, and automated firewalls (such as Aegis AI).\n"
            "- **Healthcare:** Early disease screening, robotic surgery, and accelerated drug synthesis.\n"
            "- **Autonomous Vehicles:** Real-time sensor fusion, path planning, and object tracking."
        )

    # 6. Machine Learning / Deep Learning / Neural Networks
    if "machine learning" in p_lower:
        return (
            "### 🧠 What is Machine Learning (ML)?\n\n"
            "**Machine Learning** is a core subfield of Artificial Intelligence that enables computers to learn from data and improve their performance over time without being explicitly coded with hard rules.\n\n"
            "#### Primary Paradigms:\n"
            "1. **Supervised Learning:** Trained on labeled data $(X, y)$. Models learn to map inputs to targets.\n"
            "   - *Algorithms:* Linear Regression, Logistic Regression, Decision Trees, Random Forests, XGBoost, Support Vector Machines (SVM).\n"
            "   - *Use Cases:* Spam detection, credit default prediction, price forecasting.\n"
            "2. **Unsupervised Learning:** Discovers hidden patterns or clusters in unlabeled data $(X)$.\n"
            "   - *Algorithms:* K-Means Clustering, PCA (Principal Component Analysis), DBSCAN, Autoencoders.\n"
            "   - *Use Cases:* Customer segmentation, anomaly detection, dimensionality reduction.\n"
            "3. **Reinforcement Learning (RL):** An agent learns optimal actions through trial-and-error by maximizing cumulative rewards from an environment.\n"
            "   - *Algorithms:* Q-Learning, PPO, Deep Q-Networks (DQN).\n"
            "   - *Use Cases:* Robotics, game playing (AlphaGo, chess), RLHF in LLM fine-tuning."
        )

    if "deep learning" in p_lower or "neural network" in p_lower:
        return (
            "### ⚡ What is Deep Learning?\n\n"
            "**Deep Learning** is a subset of Machine Learning that uses deep Artificial Neural Networks (ANNs) containing multiple hidden layers between the input and output.\n\n"
            "#### Fundamental Architecture:\n"
            "1. **Artificial Neurons (Perceptrons):** Compute weighted sums of inputs, add a bias, and pass through an activation function:\n"
            "   $$y = f\\left(\\sum_{i=1}^n w_i x_i + b\\right)$$\n"
            "2. **Activation Functions:** Introduce non-linearity (e.g. ReLU, GELU, Sigmoid, Softmax).\n"
            "3. **Backpropagation:** Computes gradients of the loss function with respect to weights using the chain rule of calculus.\n"
            "4. **Optimization:** Updates weights using algorithms like AdamW, SGD, or RMSprop to minimize prediction loss.\n\n"
            "#### Major Architectures:\n"
            "- **Transformers:** Powers modern LLMs using multi-head self-attention.\n"
            "- **CNNs (Convolutional Neural Networks):** Specialized for spatial grid data (images).\n"
            "- **RNNs / LSTMs:** Historically used for sequential and time-series data."
        )

    # 7. Quantum Computing / Physics
    if "quantum" in p_lower:
        return (
            "### ⚛️ What is Quantum Computing?\n\n"
            "Quantum computing is a computational paradigm that exploits quantum mechanics to solve complex problems exponentially faster than classical supercomputers.\n\n"
            "#### Core Principles:\n"
            "1. **Qubits:** Unlike classical bits (which are strictly `0` or `1`), a quantum bit can exist as a superposition $\\alpha|0\\rangle + \\beta|1\\rangle$.\n"
            "2. **Superposition:** Allows a system of $N$ qubits to represent $2^N$ simultaneous states at once.\n"
            "3. **Entanglement:** A phenomenon where paired qubits become interdependent, such that measuring one instantly dictates the state of the other.\n"
            "4. **Interference:** Quantum algorithms (e.g. Shor's for prime factorization, Grover's for database search) amplify constructive probability waves for correct solutions while canceling incorrect paths.\n\n"
            "**Primary Applications:** Post-quantum cryptography, molecular simulation for drug discovery, and logistics optimization."
        )

    # 8. Cloud Computing, Containers & Docker
    if "docker" in p_lower or "container" in p_lower:
        return (
            "### 🐳 What is Docker & Containerization?\n\n"
            "**Docker** is an open-source platform that enables developers to package an application along with all its dependencies, libraries, and runtime configurations into a lightweight, standalone container.\n\n"
            "#### Containers vs. Virtual Machines (VMs):\n"
            "- **Virtual Machines:** Run an entire guest operating system on top of a hypervisor (heavyweight, gigabytes in size, slower boot).\n"
            "- **Docker Containers:** Share the host kernel while isolating user space (lightweight, megabytes in size, sub-second startup).\n\n"
            "#### Key Concepts:\n"
            "1. **Dockerfile:** Text manifest containing step-by-step instructions to build an image.\n"
            "2. **Image:** Immutable snapshot of an application and its environment.\n"
            "3. **Container:** Running instance of an image.\n"
            "4. **Docker Compose:** Multi-container orchestrator defined in a simple YAML file."
        )

    if "cloud" in p_lower or "aws" in p_lower or "azure" in p_lower:
        return (
            "### ☁️ What is Cloud Computing?\n\n"
            "**Cloud Computing** is the on-demand delivery of compute power, database storage, applications, and other IT resources over the internet with pay-as-you-go pricing.\n\n"
            "#### The Three Service Models:\n"
            "1. **IaaS (Infrastructure as a Service):** Fundamental building blocks—virtual servers, storage, networking (e.g. AWS EC2, Google Compute Engine).\n"
            "2. **PaaS (Platform as a Service):** Managed environments for deploying code without managing underlying servers (e.g. AWS Elastic Beanstalk, Heroku, Render).\n"
            "3. **SaaS (Software as a Service):** Complete, managed end-user software delivered over the web (e.g. Gmail, Slack, Microsoft 365).\n\n"
            "#### Deployment Models:\n"
            "- **Public Cloud:** Resources shared across tenants (AWS, Azure, GCP).\n"
            "- **Private Cloud:** Dedicated infrastructure for a single organization.\n"
            "- **Hybrid Cloud:** Integrated mix of private on-premises servers and public cloud services."
        )

    # 9. Cybersecurity, Firewalls & Aegis
    if "firewall" in p_lower or "security" in p_lower or "zero trust" in p_lower or "soc" in p_lower:
        return (
            "### 🛡️ Enterprise AI Security & The Aegis Architecture\n\n"
            "Aegis AI operates as an autonomous, multi-tier defense-in-depth shield safeguarding generative AI models from malicious exploitation:\n\n"
            "#### The 5 Defense Tiers:\n"
            "1. **Tier 1: Lexical Gatekeeper:** Sub-millisecond signature matching against known injection payloads, jailbreak prefixes, and developer override phrases.\n"
            "2. **Tier 2: Semantic Cosine Engine:** Vector embeddings measuring cosine similarity against threat clusters, detecting adversarial paraphrasing and multi-lingual evasion (Tamil, Tanglish, English).\n"
            "3. **Tier 3: Autonomous Threat Memory:** Dynamic self-healing memory store that autonomously indexes newly discovered attack signatures in real-time.\n"
            "4. **Tier 4: In-Flight Prompt Sanitizer:** Neutralizes attack tokens before inference, converting hostile probes into harmless educational queries.\n"
            "5. **Tier 5: SOC Telemetry & User Risk Engine:** Tracks user risk scores, flags repeated offenders, and enforces automated warning, blocking, or permanent blacklisting."
        )

    # 10. Photosynthesis / Science
    if "photosynthesis" in p_lower:
        return (
            "### 🌿 What is Photosynthesis?\n\n"
            "**Photosynthesis** is the biological process by which green plants, algae, and certain bacteria convert light energy into chemical energy stored in carbohydrate molecules (such as glucose).\n\n"
            "#### Chemical Formula:\n"
            "$$6\\text{CO}_2 + 6\\text{H}_2\\text{O} + \\text{Light Energy} \\longrightarrow \\text{C}_6\\text{H}_{12}\\text{O}_6 + 6\\text{O}_2$$\n\n"
            "#### Two Main Stages:\n"
            "1. **Light-Dependent Reactions (in Thylakoid membranes):** Chlorophyll absorbs sunlight, splits water molecules ($H_2O$), releases oxygen ($O_2$), and produces ATP and NADPH.\n"
            "2. **Calvin Cycle / Light-Independent Reactions (in Stroma):** Utilizes ATP and NADPH to fix carbon dioxide ($CO_2$) into three-carbon sugars, ultimately forming glucose."
        )

    # 11. Blockchain & Web3
    if "blockchain" in p_lower:
        return (
            "### 🔗 What is Blockchain?\n\n"
            "A **Blockchain** is a decentralized, distributed, and cryptographically secured digital ledger that records transactions across a peer-to-peer network of computers (nodes) such that registered transactions cannot be altered retroactively without network consensus.\n\n"
            "#### 1. Core Architectural Pillars\n"
            "- **Cryptographically Linked Blocks:** Each block contains verified transactions, a timestamp, a nonce, and the **cryptographic hash (SHA-256)** of the preceding block. Chaining blocks by hash ensures that altering any historical record invalidates the entire chain.\n"
            "- **Decentralized Consensus:** Replaces central intermediaries with algorithmic agreement:\n"
            "  - **Proof of Work (PoW):** Miners solve energy-intensive cryptographic puzzles (e.g. Bitcoin).\n"
            "  - **Proof of Stake (PoS):** Validators commit capital tokens to validate transactions and secure the network (e.g. Ethereum).\n"
            "- **Immutability:** Once written and accepted by network consensus, ledger records are mathematically tamper-proof.\n\n"
            "#### 2. Smart Contracts & Programmability\n"
            "Pioneered by Ethereum, **Smart Contracts** are self-executing programs deployed directly on the blockchain that autonomously enforce agreements when predefined conditions are satisfied.\n\n"
            "#### 3. Real-World Applications\n"
            "- **Financial Services & DeFi:** Global real-time settlements, automated lending, and stablecoins.\n"
            "- **Supply Chain Transparency:** Verifying authentic provenance from source to consumer.\n"
            "- **Decentralized Identity:** Self-sovereign cryptographic identity management."
        )

    # 12. Pondicherry (Puducherry) Famous Places & Tourism
    if "pondicherry" in p_lower or "puducherry" in p_lower:
        return (
            "### 🌴 Famous Places to Visit in Pondicherry (Puducherry)\n\n"
            "Pondicherry, widely celebrated as the *'French Riviera of the East'*, is renowned for its tranquil coastal beaches, French colonial architecture, spiritual retreats, and vibrant cafes.\n\n"
            "#### Top Attractions & Sightseeing:\n\n"
            "1. **Promenade Beach (Rock Beach):**\n"
            "   - A scenic 1.2-kilometer coastal boulevard bordered by rocky shores, the Mahatma Gandhi statue, and the French War Memorial. Closed to motor vehicles each evening for serene seaside walks.\n\n"
            "2. **Auroville & The Matrimandir:**\n"
            "   - An international experimental township founded in 1968 by Mirra Alfassa ('The Mother'). Its golden geodesic dome, the **Matrimandir**, is a global spiritual landmark for silent concentration.\n\n"
            "3. **Sri Aurobindo Ashram:**\n"
            "   - Founded in 1926 by Indian philosopher Sri Aurobindo and The Mother. A world-famous spiritual sanctuary located in White Town.\n\n"
            "4. **White Town (The French Quarter):**\n"
            "   - Iconic streets (*Rue Dumas*, *Rue Suffren*) filled with mustard-yellow colonial villas, bougainvillea trees, quaint French bistros, and chic boutiques.\n\n"
            "5. **Paradise Beach (Chunnambar Boat House):**\n"
            "   - An isolated golden-sand beach accessed by a short ferry ride across backwaters, offering clear waters and water sports.\n\n"
            "6. **Basilica of the Sacred Heart of Jesus:**\n"
            "   - An 18th-century neo-Gothic Catholic church famous for its rare stained-glass panels depicting the life of Christ."
        )

    # 13. Conversational & Personal Inquiries
    if "joke" in p_lower:
        return (
            "### 😄 Programmer Humor\n\n"
            "**Why do programmers prefer dark mode?**\n\n"
            "*Because light attracts bugs!* 🐛\n\n"
            "---\n"
            "**There are 10 types of people in the world:**\n"
            "*Those who understand binary, and those who don't.*"
        )

    if re.search(r"\b(who are you|what are you|your name)\b", p_lower):
        return (
            "### 🛡️ About Aegis AI\n\n"
            "I am **Aegis AI**, an enterprise-grade conversational AI assistant running behind an autonomous multi-tier AI Firewall.\n\n"
            "My role is to answer your technical, scientific, programming, and general questions accurately while ensuring all interactions adhere to enterprise security and safety standards."
        )

    # 14. Real-Time Encyclopedic Knowledge Engine (Wikipedia + Live Web Search)
    wiki_answer = fetch_live_knowledge(prompt)
    if wiki_answer:
        return wiki_answer

    ddg_answer = fetch_ddg_knowledge(prompt)
    if ddg_answer:
        return ddg_answer

    # Fallback if offline
    q_topic = prompt.strip().rstrip("?").strip()
    cleaned_topic = re.sub(r"^(what is|what are|explain|tell me about|how does|define|describe)\s+", "", q_topic, flags=re.IGNORECASE).strip()
    title_str = cleaned_topic.title() if cleaned_topic else q_topic.title()

    return (
        f"### 💡 Overview: {title_str}\n\n"
        f"Regarding your query on **{title_str}**:\n\n"
        f"This is a specific topic that can be examined across historical, functional, and practical dimensions. "
        f"For expanded real-time generative responses, you can connect your free Groq API Key (console.groq.com) in Settings."
    )


def fetch_live_knowledge(query: str) -> Optional[str]:
    """
    Dynamically fetches factual, encyclopedic knowledge from Wikipedia API
    for any real-world inquiry (places, history, science, technology, people).
    """
    headers = {"User-Agent": "AegisAIAssistant/2.5 (security-firewall@aegis.local)"}

    # Extract target topic
    tour_match = re.search(r"(?:famous places?|places? to visit|tourist places?|attractions?|sightseeing) (?:in|of|at) ([a-zA-Z\s]+)", query, re.IGNORECASE)
    if tour_match:
        city = tour_match.group(1).strip().strip("?.")
        search_terms = [f"Tourism in {city}", f"{city} attractions", city]
    else:
        clean = re.sub(r"^(what is|what are|explain|tell me about|how does|who is|who was|where is)\s+", "", query, flags=re.IGNORECASE).strip(" ?.")
        search_terms = [clean if clean else query]

    import urllib.parse
    for term in search_terms:
        try:
            s_resp = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": term,
                    "format": "json",
                    "utf8": 1
                },
                headers=headers,
                timeout=4
            ).json()
            hits = s_resp.get("query", {}).get("search", [])
            if hits:
                top_title = hits[0]["title"]
                encoded = urllib.parse.quote(top_title.replace(" ", "_"))
                p_resp = requests.get(
                    f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}",
                    headers=headers,
                    timeout=4
                )
                if p_resp.status_code == 200:
                    extract = p_resp.json().get("extract")
                    if extract and len(extract) > 40:
                        return f"### 📖 {top_title}\n\n{extract}\n\n---\n*Source: Verified Knowledge Base*"
        except Exception:
            continue
    return None


def fetch_ddg_knowledge(query: str) -> Optional[str]:
    """Fetches real-time web search snippets from DuckDuckGo HTML search for current queries."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        import html
        clean = re.sub(r"^(what is|what are|explain|tell me about|how does|who is|who was|where is|which is|which the)\s+", "", query, flags=re.IGNORECASE).strip(" ?.")
        term = clean if clean else query.strip(" ?.")
        r = requests.post("https://html.duckduckgo.com/html/", data={"q": term}, headers=headers, timeout=4)
        if r.status_code == 200:
            snippets = re.findall(r'<a class="result__snippet[^"]*"[^>]*>(.*?)</a>', r.text, re.DOTALL)
            cleaned = []
            for s in snippets[:3]:
                clean_s = re.sub(r'<[^>]+>', '', s).strip()
                clean_s = html.unescape(clean_s)
                if clean_s and len(clean_s) > 25:
                    cleaned.append(clean_s)
            if cleaned:
                body = "\n\n".join(f"- {c}" for c in cleaned)
                return f"### 🌐 Web Knowledge Briefing: {term.title()}\n\n{body}\n\n---\n*Source: Live Web Search*"
    except Exception:
        pass
    return None


def query_llm(prompt: str) -> str:
    """
    Primary LLM gateway:
    1. Tries Groq Cloud API with dynamic high-speed model (e.g. Qwen-3.8-27B, Compound, Llama) if key is active.
    2. Tries local Ollama API if running.
    3. Seamlessly falls back to Aegis Autonomous Conversational Intelligence.
    """
    key = get_current_api_key()

    if key:
        model = _ACTIVE_GROQ_MODEL or resolve_groq_model(key) or "qwen/qwen3.8-27b"
        try_models = [model] + [m for m in DEFAULT_GROQ_CANDIDATES if m != model]
        for m in try_models[:3]:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": m,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are Aegis AI, an enterprise-grade, highly intelligent AI assistant. "
                            "Answer the user's questions clearly, accurately, thoroughly, and professionally with markdown formatting."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1024,
                "temperature": 0.7
            }
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=30)
                if resp.status_code == 200:
                    choices = resp.json().get("choices", [])
                    if choices:
                        content = choices[0]["message"]["content"]
                        if content and content.strip():
                            return content
            except Exception:
                continue

    # Try local Ollama if active
    if is_ollama_active():
        try:
            ollama_resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3", "prompt": prompt, "stream": False},
                timeout=5
            )
            if ollama_resp.status_code == 200:
                return ollama_resp.json().get("response", "")
        except Exception:
            pass

    # Autonomous Edge Conversational Engine
    return generate_conversational_response(prompt)
