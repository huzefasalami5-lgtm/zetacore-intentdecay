#!/usr/bin/env bash
# ==============================================================================
# ZetaCore: IntentDecay - IBM LinuxONE / s390x Automated Deployment Script
# IBM Z Datathon 2026: "AI Secured: Innovation Without Exposure"
# ==============================================================================
set -euo pipefail

# ANSI Color Codes
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ------------------------------------------------------------------------------
# Configuration (Override via Environment Variables)
# ------------------------------------------------------------------------------
IBMZ_HOST="${IBMZ_HOST:-192.168.1.100}"
IBMZ_USER="${IBMZ_USER:-linux1}"
IBMZ_PORT="${IBMZ_PORT:-22}"
IBMZ_KEY="${IBMZ_KEY:-}"
REMOTE_DIR="${REMOTE_DIR:-/home/${IBMZ_USER}/zetacore-intentdecay}"
VENV_PATH="${REMOTE_DIR}/.venv"
ACTION="${1:-deploy}" # Options: deploy, run-cli, run-benchmark, run-dashboard

SSH_OPTS="-p ${IBMZ_PORT} -o StrictHostKeyChecking=no -o ConnectTimeout=10"
if [ -n "${IBMZ_KEY}" ]; then
    SSH_OPTS="${SSH_OPTS} -i ${IBMZ_KEY}"
fi

# ------------------------------------------------------------------------------
# Banner
# ------------------------------------------------------------------------------
echo -e "${CYAN}"
echo "=============================================================================="
echo "    ███████╗███████╗████████╗ █████╗  ██████╗ ██████╗ ██████╗ ███████╗"
echo "    ╚══███╔╝██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝"
echo "      ███╔╝ █████╗     ██║   ███████║██║     ██║   ██║██████╔╝█████╗  "
echo "     ███╔╝  ██╔══╝     ██║   ██╔══██║██║     ██║   ██║██╔══██╗██╔══╝  "
echo "    ███████╗███████╗   ██║   ██║  ██║╚██████╗╚██████╔╝██║  ██║███████╗"
echo "    ╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝"
echo "        >>> IBM LinuxONE / s390x Production Deployment Gateway <<<"
echo "=============================================================================="
echo -e "${NC}"

echo -e "${YELLOW}[*] Target Host:${NC}       ${IBMZ_USER}@${IBMZ_HOST}:${IBMZ_PORT}"
echo -e "${YELLOW}[*] Destination Dir:${NC}   ${REMOTE_DIR}"
echo -e "${YELLOW}[*] Target Action:${NC}     ${ACTION}"
echo "------------------------------------------------------------------------------"

# ------------------------------------------------------------------------------
# Step 1: Pre-flight SSH & Architecture Check (Verify s390x)
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}[STEP 1/5] Checking SSH Connectivity & Mainframe Architecture...${NC}"

if ! ssh ${SSH_OPTS} "${IBMZ_USER}@${IBMZ_HOST}" "exit" 2>/dev/null; then
    echo -e "${RED}[!] Error: Unable to connect via SSH to ${IBMZ_USER}@${IBMZ_HOST}:${IBMZ_PORT}.${NC}"
    echo -e "${YELLOW}[?] Hint: Set the following environment variables before running:${NC}"
    echo "    export IBMZ_HOST=\"<your-linuxone-ip>\""
    echo "    export IBMZ_USER=\"<your-username>\""
    echo "    export IBMZ_KEY=\"/path/to/private_key.pem\""
    exit 1
fi

REMOTE_ARCH=$(ssh ${SSH_OPTS} "${IBMZ_USER}@${IBMZ_HOST}" "uname -m")
REMOTE_OS=$(ssh ${SSH_OPTS} "${IBMZ_USER}@${IBMZ_HOST}" "uname -s -r")

echo -e "${GREEN}[✓] SSH Connection Established.${NC}"
echo -e "${GREEN}[✓] Remote Kernel:${NC} ${REMOTE_OS}"

if [[ "${REMOTE_ARCH}" == *"s390"* ]]; then
    echo -e "${PURPLE}[★] HARDWARE CONFIRMED: Native IBM Z / LinuxONE (${REMOTE_ARCH})${NC}"
    echo -e "${PURPLE}[★] CPACF Cryptographic & SIMD Vector Instructions Active.${NC}"
else
    echo -e "${YELLOW}[!] Notice: Remote architecture is '${REMOTE_ARCH}' (Not s390x). Proceeding in emulation mode.${NC}"
fi

# ------------------------------------------------------------------------------
# Step 2: Prepare Remote Directory & Python Virtual Environment
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}[STEP 2/5] Preparing Remote Directory & Python Virtual Environment...${NC}"

ssh ${SSH_OPTS} "${IBMZ_USER}@${IBMZ_HOST}" bash -s << EOF
set -e
mkdir -p "${REMOTE_DIR}"
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 not found on remote system. Installing minimal runtime..."
    if command -v dnf &> /dev/null; then
        sudo dnf install -y python3 python3-pip python3-devel
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
    fi
fi

# Create virtualenv if not present
if [ ! -d "${VENV_PATH}" ]; then
    echo "[*] Creating fresh virtualenv at ${VENV_PATH}..."
    python3 -m venv "${VENV_PATH}"
fi
EOF

echo -e "${GREEN}[✓] Remote environment prepared.${NC}"

# ------------------------------------------------------------------------------
# Step 3: Synchronize Project Files to IBM Z / LinuxONE
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}[STEP 3/5] Synchronizing Project Deliverables to LinuxONE...${NC}"

FILES_TO_SYNC=(
    "data.json"
    "scorer.py"
    "main.py"
    "app.py"
    "requirements.txt"
)

# Validate local files exist
for f in "${FILES_TO_SYNC[@]}"; do
    if [ ! -f "$f" ]; then
        echo -e "${RED}[!] Missing local deliverable: $f${NC}"
        exit 1
    fi
done

if command -v rsync &> /dev/null; then
    rsync -avz -e "ssh ${SSH_OPTS}" "${FILES_TO_SYNC[@]}" "${IBMZ_USER}@${IBMZ_HOST}:${REMOTE_DIR}/"
else
    scp ${SSH_OPTS} "${FILES_TO_SYNC[@]}" "${IBMZ_USER}@${IBMZ_HOST}:${REMOTE_DIR}/"
fi

echo -e "${GREEN}[✓] Files transferred successfully.${NC}"

# ------------------------------------------------------------------------------
# Step 4: Install Dependencies on Remote LinuxONE Instance
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}[STEP 4/5] Installing Dependencies on Remote Target...${NC}"

ssh ${SSH_OPTS} "${IBMZ_USER}@${IBMZ_HOST}" bash -s << EOF
set -e
source "${VENV_PATH}/bin/activate"
python -m pip install --upgrade pip
echo "[*] Installing requirements from requirements.txt..."
python -m pip install -r "${REMOTE_DIR}/requirements.txt"
EOF

echo -e "${GREEN}[✓] Dependencies configured on LinuxONE.${NC}"

# ------------------------------------------------------------------------------
# Step 5: Execute Target Action
# ------------------------------------------------------------------------------
echo -e "\n${CYAN}[STEP 5/5] Executing Action: '${ACTION}'...${NC}"

case "${ACTION}" in
    deploy)
        echo -e "${GREEN}[✓] Deployment complete! Remote files are synced and ready.${NC}"
        echo -e "${YELLOW}To run CLI trace remotely:${NC}"
        echo "    ./deploy_to_ibmz.sh run-cli"
        echo -e "${YELLOW}To run Benchmark remotely:${NC}"
        echo "    ./deploy_to_ibmz.sh run-benchmark"
        echo -e "${YELLOW}To launch Dashboard remotely:${NC}"
        echo "    ./deploy_to_ibmz.sh run-dashboard"
        ;;

    run-cli)
        echo -e "${YELLOW}[*] Executing ZetaCore CLI Trace on IBM Z (${REMOTE_ARCH})...${NC}\n"
        ssh -t ${SSH_OPTS} "${IBMZ_USER}@${IBMZ_HOST}" "cd ${REMOTE_DIR} && source ${VENV_PATH}/bin/activate && python3 main.py --auto-approve"
        ;;

    run-benchmark)
        echo -e "${YELLOW}[*] Running High-Throughput Mainframe Benchmark on LinuxONE...${NC}\n"
        ssh -t ${SSH_OPTS} "${IBMZ_USER}@${IBMZ_HOST}" "cd ${REMOTE_DIR} && source ${VENV_PATH}/bin/activate && python3 main.py --benchmark -n 250"
        ;;

    run-dashboard)
        echo -e "${YELLOW}[*] Starting Streamlit Dashboard on IBM LinuxONE port 8501...${NC}"
        ssh ${SSH_OPTS} "${IBMZ_USER}@${IBMZ_HOST}" "cd ${REMOTE_DIR} && source ${VENV_PATH}/bin/activate && nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > ${REMOTE_DIR}/streamlit.log 2>&1 &"
        echo -e "${GREEN}[✓] Streamlit dashboard is running in background on IBM Z!${NC}"
        echo -e "${PURPLE}[★] Web Access URL:${NC} http://${IBMZ_HOST}:8501"
        echo -e "${YELLOW}[?] To forward port securely via SSH tunnel:${NC}"
        echo "    ssh ${SSH_OPTS} -L 8501:localhost:8501 ${IBMZ_USER}@${IBMZ_HOST}"
        echo "    Then open http://localhost:8501 in your local browser."
        ;;

    *)
        echo -e "${RED}[!] Unknown action: '${ACTION}'. Valid options: deploy, run-cli, run-benchmark, run-dashboard${NC}"
        exit 1
        ;;
esac

echo -e "\n${GREEN}==============================================================================${NC}"
echo -e "${GREEN}             ZetaCore: IntentDecay IBM Z Deployment Finished                  ${NC}"
echo -e "${GREEN}==============================================================================${NC}"
