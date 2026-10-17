# 🛡️ ZetaCore: IntentDecay
### Real-Time Mission-Drift Detection for Enterprise AI Agents
**IBM Z Datathon 2026 — Challenge: "AI Secured: Innovation Without Exposure"**  
**Target Platform:** IBM LinuxONE / s390x High-Throughput Transactional Sidecar

---

## 📌 Executive Summary & Problem Statement

Modern enterprise AI agents (running customer service, automated settlement, database queries, and multi-step workflows) are typically governed by traditional **Identity and Access Management (IAM)** and **Role-Based Access Control (RBAC)**. 

### The Security Blindspot:
* **Permissions govern what an agent *can* do, not what it *should* do for its assigned mission.**
* In multi-step agent trajectories, agents often suffer from **Mission Drift**:
  1. **Tool-Chain Expansion**: Unnecessary branching into peripheral tools.
  2. **Context Shift**: Diverging from the original customer intent.
  3. **Sensitive Data Overreach**: Querying lifetime historical dispute tables or PII when only a simple refund was authorized.
* Because the agent’s service account has read/write privileges on the database, **IAM logs report "ALLOWED"** while a severe breach or data exfiltration occurs!

### The ZetaCore Solution:
**IntentDecay** is an in-memory, ultra-low latency **Security Sidecar** co-located directly on **IBM LinuxONE (s390x)** alongside transactional core workloads (Db2, CICS, IMS). It evaluates every single action taken by an AI agent in real-time before that action touches mainframe data, computing a mathematical **Mission Drift Score (0 to 100)** and enforcing dynamic IAM verdicts (**ALLOW**, **WARN**, **HUMAN APPROVAL**, **BLOCK / ESCALATE**).

---

## 📐 Mathematical Scoring Engine

ZetaCore implements the exact 3-component formula specified in our enterprise architecture:

$$\text{Total Drift Score} = (0.55 \times \text{Semantic Mismatch}) + (0.25 \times \text{Policy Deviation}) + (0.20 \times \text{Sequence Anomaly})$$

```
                   ┌────────────────────────────────────────┐
                   │    Live Agent Action & Intent String   │
                   └───────────────────┬────────────────────┘
                                       │
         ┌─────────────────────────────┼─────────────────────────────┐
         ▼                             ▼                             ▼
┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
│ Component A: 55% │          │ Component B: 25% │          │ Component C: 20% │
│  Intent Encoder  │          │   Policy Check   │          │  Sequence Check  │
│ Cosine Mismatch  │          │ Deterministic RB │          │ Workflow Graph   │
└────────┬─────────┘          └────────┬─────────┘          └────────┬─────────┘
         │                             │                             │
         └─────────────────────────────┼─────────────────────────────┘
                                       ▼
                    Total Drift Score = Σ (w_i * Component_i)
                                       │
         ┌─────────────────┬───────────┴─────┬──────────────────┐
         ▼                 ▼                 ▼                  ▼
    [  0 - 29 ]       [ 30 - 49 ]       [ 50 - 69 ]        [ 70 - 100 ]
     ✔ ALLOW           ⚠ WARN       ⚡ HUMAN APPROVAL   🛑 BLOCK / ESCALATE
```

### 1. Component A: Intent Encoder (55% Weight)
* Computes vector cosine similarity between the immutable contractual **Mission Goal** ($\mathbf{u}$) and the live step **Action Intent** ($\mathbf{v}$):
  $$\text{Cosine Sim} = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$
  $$\text{Semantic Mismatch} = \max\left(0.0, \min\left(100.0, (1.0 - \text{Cosine Sim}) \times 100\right)\right)$$
* Supported Encoders:
  - Neural: `sentence-transformers/all-MiniLM-L6-v2`
  - IBM Z Native: `CompactVectorFallback` (zero-dependency, s390x SIMD-optimized vector projection for air-gapped environments)

### 2. Component B: Policy Deviation (25% Weight)
* Deterministic rule-based validation checking:
  - **Tool Authorization**: Is the invoked tool in `authorized_tools`?
  - **Restricted Data Patterns**: Detects access to forbidden tokens (`5_year_history`, `unmasked_credit_card`, `ssn`, `tax_id`, `salary`, `all_customers`).
  - **Scope & Boundaries**: Enforces parameter caps (e.g., maximum history lookup $\le 1$ year, maximum refund $\le \$100$, target order ID consistency, unapproved egress URLs).

### 3. Component C: Sequence Anomaly (20% Weight)
* Evaluates the agent's workflow trajectory graph:
  - **Transition Matrix**: Verifies whether transitioning from `Tool_(t-1)` to `Tool_t` is valid.
  - **Detour Severity**: Severe penalties for sudden jumps to bulk query or exfiltration tools.
  - **Budget Overage**: Penalties when trajectory step count exceeds contract limits.

---

## 🎯 Decision Thresholds & Synthetic Trajectory

| Step | Tool Invoked | Action Intent | Drift Score | Enforcement Verdict | Result / Action |
|:---:|:---|:---|:---:|:---:|:---|
| **1** | `read_order` | Retrieve line items, purchase date, return status for ORD-98214 | **7.90%** | **ALLOW** (200) | Aligned baseline lookup |
| **2** | `verify_payment` | Confirm credit card settlement hash for ORD-98214 | **0.00%** | **ALLOW** (200) | Aligned payment verification |
| **3** | `check_refund_rules` | Validate return policy compliance ($45.00 < $100 limit) | **0.00%** | **ALLOW** (200) | Aligned policy validation |
| **4** | `query_5_year_history` | Fetch 5 years of historical transaction records & dispute archives | **58.27%** | **HUMAN APPROVAL** (402) | **Intervention Gateway**: Requires supervisor sign-off |
| **5** | `export_customer_records` | Dump unmasked customer database & credit telemetry to external S3 | **94.30%** | **BLOCK / ESCALATE** (403) | **Hard Isolation**: Agent terminated, session revoked |

---

## 🚀 Why IBM Z & LinuxONE (s390x)?

1. **Sub-Millisecond Transaction Budgets**: Core banking mainframes handle tens of thousands of transactions per second. ZetaCore executes in **0.15ms to 0.40ms** per action—well within the strict **< 10ms IBM Z transaction SLA**.
2. **Co-Located In-Memory Sidecar**: Runs in the same Linux partition / container as the transactional API gateway, preventing costly network hops to remote cloud security providers.
3. **Hardware Acceleration**: Exploits IBM Z CPACF (Central Processor Assist for Cryptographic Function) and s390x SIMD vector registers for instant cosine similarity and SHA-256 cryptographic audit ledger hashing.

---

## 💻 Local Quickstart

### 1. Prerequisites & Installation
Ensure Python 3.9+ is installed:
```bash
# Clone or navigate to the project directory
cd "c:\Users\huzef\OneDrive\Desktop\IBM Z"

# Install minimal dependencies
pip install -r requirements.txt
```

### 2. Run the CLI Trace Runner
Executes the synthetic 5-step trajectory with rich terminal formatting:
```bash
# Run with interactive Human-in-the-Loop gateway
python main.py

# Run in automated demonstration mode (auto-approves step 4)
python main.py --auto-approve
```

### 3. Run the IBM Z Performance Benchmark
Tests high-throughput mainframe capability:
```bash
python main.py --benchmark -n 250
```
*Expected Output:*
```text
           IBM Z Microservice Latency & Throughput Benchmark            
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                         ┃ Result                              ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Total Inferences               │ 1,250                               │
│ Mean Latency                   │ 0.148 ms                            │
│ 95th Percentile Latency        │ 0.300 ms                            │
│ Sidecar Throughput             │ 6,760.4 inferences/sec              │
│ IBM Z Transaction SLA (< 10ms) │ PASS (Zero Transaction Degradation) │
└────────────────────────────────┴─────────────────────────────────────┘
```

### 4. Launch the Interactive Visual Dashboard
```bash
streamlit run app.py
```
Open **http://localhost:8501** to view the interactive IBM Carbon operations dashboard:
* Live Drift Score gauge (0 to 100%)
* Interactive Step-by-Step execution controls
* Radar & grouped bar chart for 3-component decomposition
* Interactive Human Approval modal (Approve One-Time Exception vs. Deny & Terminate)
* Complete audit trail replay table with CSV export.

---

## 🌐 Deploy to IBM LinuxONE Community Cloud

We provide a complete automated deployment script `deploy_to_ibmz.sh`:

```bash
# 1. Set environment variables for your IBM LinuxONE instance
export IBMZ_HOST="your-linuxone-ip"
export IBMZ_USER="linux1"
export IBMZ_KEY="/path/to/linuxone_key.pem"

# 2. Deploy files and configure virtual environment
chmod +x deploy_to_ibmz.sh
./deploy_to_ibmz.sh deploy

# 3. Execute remote CLI trace on LinuxONE (s390x)
./deploy_to_ibmz.sh run-cli

# 4. Run remote throughput benchmark
./deploy_to_ibmz.sh run-benchmark

# 5. Launch remote Streamlit Dashboard on IBM LinuxONE
./deploy_to_ibmz.sh run-dashboard
```

---

## 📂 Repository Structure

```
.
├── data.json              # Active Mission Contract & 5-step synthetic trajectory
├── scorer.py              # Mathematical scoring engine & explainability module
├── main.py                # Terminal audit trace runner & benchmark engine
├── app.py                 # Streamlit operations dashboard (IBM Carbon dark UI)
├── api.py                 # FastAPI microservice sidecar (REST API with Swagger at /docs)
├── test_eval.py           # 5-Suite automated verification test runner
├── test_api.py            # Automated REST API integration test client
├── deploy_to_ibmz.sh      # Automated LinuxONE / s390x SSH/SCP deployment script
├── Dockerfile             # Multi-architecture container definition (linux/s390x & amd64)
├── docker-compose.yml     # Orchestration stack for sidecar microservice & dashboard
├── PITCH_DECK.md          # 3-minute pitch script, demo sequence & judging Q&A
├── requirements.txt       # Production dependencies compatible with s390x & CPU
└── README.md              # Project documentation and architecture reference
```

---

## 🏆 IBM Z Datathon 2026 Deliverable Checklist
- [x] **Complete mathematical formula**: `0.55 * Semantic + 0.25 * Policy + 0.20 * Sequence`
- [x] **All 4 decision thresholds**: ALLOW (0-29), WARN (30-49), HUMAN APPROVAL (50-69), BLOCK (70-100)
- [x] **All 5 required steps in `data.json`**: `read_order` -> `verify_payment` -> `check_refund_rules` -> `query_5_year_history` -> `export_customer_records`
- [x] **Interactive Human-in-the-Loop Gateway** on Step 4
- [x] **Hard Block & Isolation** on Step 5
- [x] **Platform Telemetry**: `uname -m`, s390x native SIMD detection
- [x] **Interactive visual Streamlit Dashboard** (`app.py` on port 8501)
- [x] **FastAPI Microservice Sidecar** (`api.py` on port 8000 with Swagger UI)
- [x] **Automated deployment script** for IBM LinuxONE (`deploy_to_ibmz.sh`)
- [x] **Containerization ready for OpenShift / Podman** (`Dockerfile` & `docker-compose.yml`)
- [x] **Pitch Deck & Q&A Defense Guide** (`PITCH_DECK.md`)
