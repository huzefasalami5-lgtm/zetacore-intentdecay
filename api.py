"""
ZetaCore: IntentDecay - Production FastAPI Microservice Sidecar
Target Architecture: IBM LinuxONE / s390x Transactional Workloads
High-Performance, Low-Latency In-Memory REST API for Enterprise AI Agents
"""

import json
import os
import platform
import time
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from scorer import IntentDecayScorer

# -----------------------------------------------------------------------------
# FastAPI App Initialization
# -----------------------------------------------------------------------------
app = FastAPI(
    title="ZetaCore: IntentDecay Security Sidecar API",
    description="Real-Time Mission-Drift Detection & IAM Enforcement for Enterprise AI Agents on IBM Z (s390x)",
    version="2.4.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cross-origin dashboard queries
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Default Mission Contract from data.json
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    INITIAL_DATA = json.load(f)

GLOBAL_CONTRACT = INITIAL_DATA.get("mission_contract", {})
SCORER_INSTANCE = IntentDecayScorer()


# -----------------------------------------------------------------------------
# Pydantic Request & Response Models
# -----------------------------------------------------------------------------
class StepEvaluationRequest(BaseModel):
    step_id: int = Field(..., description="Sequential step index in trajectory", example=4)
    tool: str = Field(..., description="Name of the tool invoked by the agent", example="query_5_year_history")
    action_intent: str = Field(..., description="Natural language statement of action intent", example="Fetch 5 years of dispute records")
    parameters: dict[str, Any] = Field(default_factory=dict, description="Action parameters", example={"window_years": 5})
    data_accessed: list[str] = Field(default_factory=list, description="Target database tables / columns", example=["customer_archive.5_year_history"])
    destination_network: str = Field(default="internal", description="Outbound network egress endpoint", example="db2.mainframe.local")
    mission_id: str | None = Field(default=None, description="Contract ID reference")


class HumanApprovalRequest(BaseModel):
    step_id: int = Field(..., description="Step ID to approve one-time exception for")
    operator_id: str = Field(..., description="Security Officer IAM username or employee ID", example="SEC-OP-8921")
    notes: str | None = Field(default="Verified customer refund dispute window", description="Approval rationale")


class ContractUpdateRequest(BaseModel):
    mission_id: str
    goal: str
    authorized_tools: list[str]
    restricted_data_patterns: list[str]
    scope: dict[str, Any]
    expected_transitions: dict[str, list[str]] | None = None


# -----------------------------------------------------------------------------
# REST API Endpoints
# -----------------------------------------------------------------------------
@app.get("/", tags=["General"])
def root():
    return {
        "service": "ZetaCore: IntentDecay In-Memory Security Sidecar",
        "challenge": "AI Secured: Innovation Without Exposure - IBM Z Datathon 2026",
        "platform": f"IBM LinuxONE / {platform.machine()}",
        "status": "ONLINE",
        "documentation": "/docs",
        "endpoints": {
            "evaluate_step": "POST /v1/drift/score",
            "approve_exception": "POST /v1/drift/approve",
            "get_contract": "GET /v1/contract",
            "health": "GET /v1/health"
        }
    }


@app.get("/v1/health", tags=["Telemetry"])
def health_check():
    arch = platform.machine()
    is_ibm_z = "s390" in arch.lower()
    return {
        "status": "HEALTHY",
        "architecture": arch,
        "is_native_ibm_z": is_ibm_z,
        "hardware_acceleration": "CPACF SIMD Vector Registers" if is_ibm_z else "SIMD Vector Emulation",
        "target_sla_ms": "< 10.0ms",
        "active_mission_id": GLOBAL_CONTRACT.get("mission_id"),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }


@app.get("/v1/contract", tags=["Contract"])
def get_active_contract():
    return GLOBAL_CONTRACT


@app.post("/v1/contract", tags=["Contract"])
def update_contract(new_contract: ContractUpdateRequest):
    global GLOBAL_CONTRACT
    GLOBAL_CONTRACT = new_contract.dict()
    SCORER_INSTANCE.reset()
    return {
        "message": "Mission Contract updated successfully. Sequence state reset.",
        "mission_id": GLOBAL_CONTRACT["mission_id"]
    }


@app.post("/v1/drift/score", tags=["Scoring Engine"])
def evaluate_agent_step(request_data: StepEvaluationRequest):
    """
    Evaluates an agent step in real-time using the exact 3-component formula:
      Total Drift Score = (0.55 * Semantic) + (0.25 * Policy) + (0.20 * Sequence)
    
    Returns HTTP status code matching enforcement decision:
      - 200 OK: ALLOW
      - 299 Warning: WARN
      - 402 Payment Required / Approval Required: HUMAN APPROVAL
      - 403 Forbidden: BLOCK / ESCALATE (Hard Containment)
    """
    step_dict = request_data.dict()
    
    # Run evaluation through the mathematical engine
    result = SCORER_INSTANCE.score_step(GLOBAL_CONTRACT, step_dict, step_dict["step_id"])
    
    status_code = result["status_code"]
    
    # Return JSON with appropriate HTTP status code
    return JSONResponse(status_code=status_code, content=result)


@app.post("/v1/drift/approve", tags=["Human-in-the-Loop"])
def approve_step_exception(approval: HumanApprovalRequest):
    """
    Grants a one-time human supervisor policy exception for a specific step.
    Unblocks the agent workflow and logs the operator ID.
    """
    SCORER_INSTANCE.approve_exception(approval.step_id)
    return {
        "status": "APPROVED",
        "step_id": approval.step_id,
        "operator": approval.operator_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "message": f"Step {approval.step_id} exception granted. Trajectory unpaused."
    }


@app.post("/v1/drift/reset", tags=["Scoring Engine"])
def reset_session():
    """Resets the sequence tracker for a new agent mission trajectory."""
    SCORER_INSTANCE.reset()
    return {"message": "Session tracker reset to initial state (Step 0)."}


# -----------------------------------------------------------------------------
# Main Entry Point for Standalone Execution
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    print("[*] Starting ZetaCore IntentDecay Sidecar API on http://0.0.0.0:8000...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
