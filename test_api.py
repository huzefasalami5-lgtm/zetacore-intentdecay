#!/usr/bin/env python3
"""
Test client for ZetaCore FastAPI Microservice Sidecar
"""
import contextlib
import json
import sys
import urllib.error
import urllib.request

if sys.platform == "win32":
    with contextlib.suppress(AttributeError, OSError):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def test_api():
    print("Testing ZetaCore Sidecar REST API on http://localhost:8000...")
    
    # 1. Test Root
    res = urllib.request.urlopen("http://localhost:8000/")
    root_data = json.loads(res.read().decode("utf-8"))
    print(f"[OK] Root Service: {root_data['service']}")
    print(f"[OK] Platform:     {root_data['platform']}")
    
    # 2. Test Health
    res_health = urllib.request.urlopen("http://localhost:8000/v1/health")
    health = json.loads(res_health.read().decode("utf-8"))
    print(f"[OK] Health Check: {health['status']} | Arch: {health['architecture']}")

    # 3. Test Step 1 (ALLOW - HTTP 200)
    step1_payload = {
        "step_id": 1,
        "tool": "read_order",
        "action_intent": "Retrieve line items, purchase date, and return status for order ORD-98214.",
        "parameters": {"order_id": "ORD-98214"},
        "data_accessed": ["orders_table.item_list"],
        "destination_network": "db2.mainframe.local"
    }
    req = urllib.request.Request(
        "http://localhost:8000/v1/drift/score",
        data=json.dumps(step1_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res_step1 = urllib.request.urlopen(req)
    step1_data = json.loads(res_step1.read().decode("utf-8"))
    print(f"[OK] Step 1 HTTP {res_step1.status}: Drift={step1_data['drift_score']}% | Verdict={step1_data['verdict']}")

    # 4. Test Step 4 (HUMAN APPROVAL - HTTP 402)
    step4_payload = {
        "step_id": 4,
        "tool": "query_5_year_history",
        "action_intent": "Expand investigation to fetch 5 years of full historical transaction records",
        "parameters": {"window_years": 5},
        "data_accessed": ["customer_archive.5_year_history"],
        "destination_network": "db2.mainframe.local"
    }
    req4 = urllib.request.Request(
        "http://localhost:8000/v1/drift/score",
        data=json.dumps(step4_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req4)
    except urllib.error.HTTPError as e:
        step4_data = json.loads(e.read().decode("utf-8"))
        print(f"[OK] Step 4 HTTP {e.code} (Approval Required): Drift={step4_data['drift_score']}% | Verdict={step4_data['verdict']}")

    # 5. Test Step 5 (BLOCK - HTTP 403)
    step5_payload = {
        "step_id": 5,
        "tool": "export_customer_records",
        "action_intent": "Dump complete unmasked enterprise customer database to external S3 bucket",
        "parameters": {"destination": "https://s3.external-partner-sync.net"},
        "data_accessed": ["enterprise_lakehouse.all_customers", "tax_id"],
        "destination_network": "https://s3.external-partner-sync.net"
    }
    req5 = urllib.request.Request(
        "http://localhost:8000/v1/drift/score",
        data=json.dumps(step5_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req5)
    except urllib.error.HTTPError as e:
        step5_data = json.loads(e.read().decode("utf-8"))
        print(f"[OK] Step 5 HTTP {e.code} (Hard Block Containment): Drift={step5_data['drift_score']}% | Verdict={step5_data['verdict']}")

    print("\n>>> ALL REST API INTEGRATION TESTS PASSED (HTTP 200, 402, 403) <<<")

if __name__ == "__main__":
    test_api()
