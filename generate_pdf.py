import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

pdf_path = os.path.join(os.path.dirname(__file__), "ZetaCore_Pitch_Deck.pdf")
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=0.5 * inch,
    rightMargin=0.5 * inch,
    topMargin=0.5 * inch,
    bottomMargin=0.5 * inch
)

styles = getSampleStyleSheet()

primary_blue = colors.HexColor("#0f62fe")
text_dark = colors.HexColor("#161616")
gray_text = colors.HexColor("#525252")
green_accent = colors.HexColor("#24a148")
red_accent = colors.HexColor("#da1e28")

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=20,
    leading=24,
    textColor=primary_blue,
    spaceAfter=4
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10.5,
    leading=14,
    textColor=gray_text,
    spaceAfter=10
)

h1_style = ParagraphStyle(
    'H1',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=17,
    textColor=primary_blue,
    spaceBefore=8,
    spaceAfter=5
)

h2_style = ParagraphStyle(
    'H2',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10.5,
    leading=14,
    textColor=colors.HexColor("#0043ce"),
    spaceBefore=5,
    spaceAfter=3
)

body_style = ParagraphStyle(
    'Body',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9,
    leading=12.5,
    textColor=text_dark,
    spaceAfter=5
)

callout_style = ParagraphStyle(
    'Callout',
    parent=styles['Normal'],
    fontName='Helvetica-Oblique',
    fontSize=9,
    leading=12.5,
    textColor=colors.HexColor("#001d6c"),
    spaceAfter=5
)

story = []

# ==================== PAGE 1 ====================
story.append(Paragraph("ZetaCore: IntentDecay", title_style))
story.append(Paragraph("<b>Real-Time Mission-Drift Detection for Enterprise AI Agents on IBM LinuxONE (s390x)</b><br/>IBM Z Datathon 2026 | Challenge Track: <b>AI Secured: Innovation Without Exposure</b>", subtitle_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=primary_blue, spaceAfter=8))

story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
story.append(Paragraph(
    "<b>The Core Problem (The IAM Blindspot):</b> Modern enterprise AI agents (running automated customer service, dispute resolution, and settlement) are governed by standard Identity and Access Management (IAM) and Role-Based Access Control (RBAC). "
    "However, permissions govern what an agent <i>can</i> access, not what it <i>should</i> do for an individual customer ticket.<br/><br/>"
    "In multi-step workflows, agents frequently suffer from <b>Mission Drift</b>:<br/>"
    "• <b>Tool-Chain Expansion:</b> Branching into unauthorized administration tools.<br/>"
    "• <b>Context Shift:</b> Reasoning drifts away from the customer's return goal.<br/>"
    "• <b>Sensitive Data Overreach:</b> Querying 5 years of historical salary and dispute archives when only a $45 return was authorized.<br/><br/>"
    "Because the agent's service account holds valid database read permissions, traditional IAM logs report <b>'ALLOWED'</b> while a catastrophic data exfiltration occurs! External cloud guardrails cannot fix this: they introduce 400ms-800ms latencies (violating the &lt;10ms IBM Z transaction SLA) and leak private banking telemetry to public cloud networks.",
    body_style
))

story.append(Paragraph("The ZetaCore Solution:", h2_style))
story.append(Paragraph(
    "ZetaCore: IntentDecay is an ultra-low latency, in-memory <b>Security Sidecar</b> co-located directly on <b>IBM LinuxONE (s390x)</b> alongside transactional core workloads (CICS, IMS, Db2). "
    "It intercepts every live action in real-time before database execution, evaluates multi-component mathematical mission drift, and enforces dynamic containment (ALLOW, WARN, HUMAN APPROVAL, BLOCK) with <b>zero exposure</b> of mainframe data to public clouds.",
    callout_style
))

metrics_data = [
    ["Target SLA", "Live LinuxONE Latency", "Mathematical Invariant", "Deployment Hardware"],
    ["< 10.00 ms", "0.034 ms (34 µs)", "Total = 0.55*Sem + 0.25*Pol + 0.20*Seq", "IBM LinuxONE / s390x Native"]
]
t_metrics = Table(metrics_data, colWidths=[1.8*inch, 1.8*inch, 2.3*inch, 1.6*inch])
t_metrics.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#edf5ff")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0043ce")),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#d0e2ff")),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
]))
story.append(Spacer(1, 4))
story.append(t_metrics)

story.append(PageBreak())

# ==================== PAGE 2 ====================
story.append(Paragraph("2. Mathematical Scoring Engine & Architecture", h1_style))
story.append(Paragraph(
    "ZetaCore evaluates live agent actions against an immutable contractual <b>Mission Contract</b> using a continuous 3-component formula:<br/>"
    "<b>Total Drift Score = (0.55 × Semantic Mismatch) + (0.25 × Policy Deviation) + (0.20 × Sequence Anomaly)</b>",
    body_style
))

formula_table = [
    ["Component", "Weight", "Methodology & Enforcement Logic"],
    ["Component A:\nIntent Encoder", "55%", "Vector Cosine Distance between contractual Mission Goal (u) and live Action Intent (v). Supports neural sentence-transformers and zero-dependency s390x SIMD CompactVectorFallback."],
    ["Component B:\nPolicy Deviation", "25%", "Deterministic verification checking authorized tool whitelist, restricted PII tokens (SSN, 5_year_history, salary, tax_id), financial dollar limits, and approved network boundaries."],
    ["Component C:\nSequence Anomaly", "20%", "State transition graph evaluation validating whether transitioning from Tool(t-1) to Tool(t) is a legal workflow path, applying severe penalties for trajectory detours."]
]
t_formula = Table(formula_table, colWidths=[1.5*inch, 0.8*inch, 5.2*inch])
t_formula.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), primary_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#d0e2ff")),
    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#f4f7fb")),
    ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor("#f4f7fb")),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story.append(t_formula)
story.append(Spacer(1, 6))

story.append(Paragraph("Enforcement Tiers & Decision Boundaries:", h2_style))
tiers_data = [
    ["Score Range", "Verdict", "HTTP Code", "Enforcement Action / Regulatory Mapping"],
    ["0 - 29%", "ALLOW", "200 OK", "Autonomous execution permitted. Action logged to in-memory ledger."],
    ["30 - 49%", "WARN", "200 OK", "Contextual anomaly flag dispatched to SIEM telemetry."],
    ["50 - 69%", "HUMAN APPROVAL", "402 Required", "Gateway pauses execution. Mandatory Human-in-the-Loop exception sign-off (EU AI Act Article 14)."],
    ["70 - 100%", "BLOCK / ESCALATE", "403 Forbidden", "Hard isolation. Session token revoked immediately, database transaction terminated, high-severity SIEM alert."]
]
t_tiers = Table(tiers_data, colWidths=[1.1*inch, 1.5*inch, 1.1*inch, 3.8*inch])
t_tiers.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#121619")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('TEXTCOLOR', (1, 1), (1, 1), green_accent),
    ('TEXTCOLOR', (1, 2), (1, 2), colors.HexColor("#b28600")),
    ('TEXTCOLOR', (1, 3), (1, 3), colors.HexColor("#ff832b")),
    ('TEXTCOLOR', (1, 4), (1, 4), red_accent),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#d0e2ff")),
    ('TOPPADDING', (0, 0), (-1, -1), 3),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
]))
story.append(t_tiers)
story.append(Spacer(1, 6))

story.append(Paragraph("3. Why IBM LinuxONE (s390x) & Synthetic Verification", h1_style))
story.append(Paragraph(
    "<b>Enterprise Mainframe Fit:</b> IBM LinuxONE runs the world's most mission-critical transactional banking databases. "
    "ZetaCore was engineered from the ground up for co-located deployment in LinuxONE LPARs/containers:<br/>"
    "• <b>In-Memory Decision Latency:</b> 0.034ms on live s390x hardware vs. 450ms for cloud guardrails (4,000x faster).<br/>"
    "• <b>Zero Data Exposure:</b> Customer PII and account balances never leave the mainframe boundary.<br/>"
    "• <b>Hardware Cryptography:</b> Exploits IBM Z CPACF for tamper-evident SHA-256 state ledger chaining.<br/>"
    "• <b>Air-Gap Execution:</b> CompactVectorFallback eliminates heavy PyTorch/GPU dependencies.",
    body_style
))

story.append(Paragraph("5-Step Synthetic Trajectory Audit Compliance:", h2_style))
audit_data = [
    ["Step", "Tool Invoked", "Action Intent & Parameters", "Drift Score", "Verdict"],
    ["1", "read_order", "Retrieve line items & return eligibility for ORD-98214", "7.90%", "ALLOW (200)"],
    ["2", "verify_payment", "Confirm payment settlement hash for ORD-98214", "0.00%", "ALLOW (200)"],
    ["3", "check_refund_rules", "Verify merchandise return policy compliance ($45.00 limit)", "0.00%", "ALLOW (200)"],
    ["4", "query_5_year_history", "Query 5-year historical disputes and unmasked records", "58.27%", "HUMAN APPROVAL (402)"],
    ["5", "export_customer_records", "Dump entire customer database to external S3 bucket", "94.30%", "BLOCK / ESCALATE (403)"]
]
t_audit = Table(audit_data, colWidths=[0.5*inch, 1.6*inch, 3.2*inch, 1.0*inch, 1.2*inch])
t_audit.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), primary_blue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 7.5),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#d0e2ff")),
    ('TEXTCOLOR', (4, 1), (4, 3), green_accent),
    ('TEXTCOLOR', (4, 4), (4, 4), colors.HexColor("#ff832b")),
    ('TEXTCOLOR', (4, 5), (4, 5), red_accent),
    ('TOPPADDING', (0, 0), (-1, -1), 2.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
]))
story.append(t_audit)
story.append(Spacer(1, 6))

story.append(Paragraph("4. Deliverables & Repository Details", h1_style))
repo_data = [
    ["Deliverable", "Description / URL"],
    ["GitHub Repository", "https://github.com/huzefasalami5-lgtm/zetacore-intentdecay"],
    ["Mainframe Host", "IBM LinuxONE Community Cloud (s390x Native VM at 148.100.78.130)"],
    ["Microservice API", "FastAPI on LinuxONE port 8000 with interactive OpenAPI /docs"],
    ["Operations Dashboard", "Streamlit UI with Plotly analytics and Interactive Attack Sandbox"],
    ["Mathematical Audit", "test_eval.py passing 5/5 test suites with 100% compliance in 0.034ms"]
]
t_repo = Table(repo_data, colWidths=[1.8*inch, 5.7*inch])
t_repo.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#edf5ff")),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0043ce")),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 7.5),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#d0e2ff")),
    ('TOPPADDING', (0, 0), (-1, -1), 2.5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
]))
story.append(t_repo)

doc.build(story)
print(f"Successfully generated PDF: {pdf_path}")
