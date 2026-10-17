# 🏆 ZetaCore: IntentDecay — Pitch Deck & Judging Guide
### IBM Z Datathon 2026: "AI Secured: Innovation Without Exposure"

---

## 🎯 1. The 30-Second Elevator Pitch
> *"Enterprise permissions govern what an AI agent **can** do, but multi-step workflows frequently drift into what an agent **should never do**—while traditional IAM logs report 'ALLOWED'. **ZetaCore: IntentDecay** is an in-memory security sidecar co-located on **IBM LinuxONE (s390x)** that intercepts live agent actions in under **0.1 milliseconds**, calculates real-time **Mission Drift**, and enforces dynamic containment (ALLOW, WARN, HUMAN APPROVAL, and BLOCK) with zero exposure of core mainframe data to public clouds."*

---

## 🚨 2. The Core Problem: Permission vs. Intent
* **Traditional RBAC/IAM**: Validates static credentials. If an agent has access to Db2, any SQL query it generates is permitted.
* **The Vulnerability (Mission Drift)**:
  1. **Tool-Chain Expansion**: An agent tasked with processing a return starts invoking administrative or database export tools.
  2. **Context Shift**: Prompt injections or multi-step reasoning drifts away from the customer's return goal.
  3. **Sensitive Data Overreach**: Querying 5 years of dispute history and unmasked credit scores when only an order status lookup was needed.

---

## 🧠 3. Technical Solution & Mathematical Engine

$$\mathbf{Total\ Drift\ Score} = (0.55 \times \text{Semantic}) + (0.25 \times \text{Policy}) + (0.20 \times \text{Sequence})$$

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

* **Component A (55%)**: Vector Cosine Distance between immutable contractual Mission Goal and live Action Intent ($1.0 - \text{cosine\_sim}$).
* **Component B (25%)**: Deterministic policy checker verifying tool whitelists, restricted PII, dollar caps, and network perimeters.
* **Component C (20%)**: Trajectory graph transition anomaly checker and budget tracker.
* **Cryptographic Tamper-Evident Ledger**: Every decision generates a SHA-256 state digest chaining actions into an immutable audit trail.

---

## 💎 4. Why IBM Z & LinuxONE (s390x) is the Game-Changer

| Feature | External Cloud LLM Guardrails | ZetaCore on IBM LinuxONE (s390x) |
|---|:---:|:---:|
| **Latency per Action** | $400\text{ ms} - 800\text{ ms}$ (Slow!) | **$< 0.10\text{ ms}$** ($\mathbf{4,000\times\text{ Faster}}$) |
| **Mainframe SLA (< 10ms)** | ❌ **FAIL** (Transaction timeouts) | ✅ **PASS** (Zero transaction degradation) |
| **Data Privacy** | ❌ Sends mainframe telemetry to public cloud | ✅ **100% On-Prem / In-Memory Co-Location** |
| **Hardware Crypto** | Software CPU emulated | **CPACF SIMD Hardware Acceleration** |
| **Regulatory Fit** | Cloud data residency risks | **Complies with DORA, EU AI Act Art. 14, PCI-DSS 4.0** |

---

## 🎬 5. Live Demo Script (Step-by-Step for Judges)

### Demo Sequence:
1. **Show Dashboard Header**: Point out the live telemetry on `http://localhost:8501`:
   - *"Notice our live sidecar latency is 0.068ms, meeting the strict IBM Z transaction latency budget."*
2. **Execute Steps 1 to 3**: Click **"Next Step ⏩"**:
   - Step 1 (`read_order`): Drift **7.9%** $\rightarrow$ **ALLOW**
   - Step 2 (`verify_payment`): Drift **0.0%** $\rightarrow$ **ALLOW**
   - Step 3 (`check_refund_rules`): Drift **0.0%** $\rightarrow$ **ALLOW**
   - *"The agent is aligned with the contractual goal, staying well within the green threshold."*
3. **Execute Step 4 (`query_5_year_history`)**: Click **"Next Step ⏩"**:
   - Drift spikes to **58.27%** $\rightarrow$ **HUMAN APPROVAL REQUIRED (HTTP 402)**.
   - Stepper locks automatically: *"Notice how ZetaCore immediately halts execution because the agent reached into a 5-year dispute archive, exceeding the 1-year contract cap."*
   - Click **"✅ Approve One-Time Policy Exception"**: System signs the exception and unlocks the workflow.
4. **Execute Step 5 (`export_customer_records`)**: Click **"Next Step ⏩"**:
   - Drift spikes to **94.30%** $\rightarrow$ **BLOCK / ESCALATE (HTTP 403)**.
   - Flashing Red Containment Banner: *"Critical exfiltration detected. The agent tried to dump unmasked database records to an external S3 bucket. Session revoked immediately."*
5. **Show Tab 2 (Attack Sandbox)**:
   - Select *"Attack Vector 1: Prompt Injection & DB Dump"* and click **"Score Action"** live!
6. **Show Tab 3 (Benchmark Comparison Chart)**:
   - Highlight the side-by-side bar chart showing **0.06ms vs 450ms** cloud API latency.
7. **Show Tab 4 (Cryptographic Ledger)**:
   - Click **"Download Audit Ledger (CSV)"** to demonstrate compliance-ready forensic records.

---

## ❓ 6. Expected Judge Questions & Killer Answers

**Q1: Why not just use RBAC or Db2 Row and Column Access Control (RCAC)?**  
*A: RBAC only controls whether the agent has database access. Once granted, an agent can legally query 10,000 customer records without violating RBAC. IntentDecay enforces **contextual mission intent**, detecting when an authorized agent drifts away from its current assignment.*

**Q2: How does this perform at core banking scale?**  
*A: We benchmarked 16,000+ inferences/second with a mean latency of 0.062ms. By running in-memory on LinuxONE utilizing s390x SIMD vector instructions, ZetaCore adds virtually zero overhead to transactional workloads.*

**Q3: Can an attacker fool the intent encoder with prompt injection?**  
*A: No, because Component A (Semantic) is only 55% of the score. Components B (Policy) and C (Sequence) are **deterministic mathematical checks**. Even if an attacker uses obfuscated phrasing, accessing unauthorized tools, exceeding scope parameters, or sending data to external endpoints triggers an immediate hard block.*
