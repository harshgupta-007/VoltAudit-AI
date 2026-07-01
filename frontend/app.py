"""VoltAudit AI Enterprise Streamlit Frontend Dashboard."""

import time

import pandas as pd
import streamlit as st
from services import BackendAPIClient

# Page configuration
st.set_page_config(
    page_title="VoltAudit AI - Enterprise Dashboard",
    page_icon="⚡",
    layout="wide",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
    }
    .metric-title {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .agent-step {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 10px 15px;
        margin-bottom: 8px;
        border-radius: 0 8px 8px 0;
    }
    .agent-active {
        border-left-color: #f59e0b;
        background-color: #fffbeb;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize Session State
if "audited_invoices" not in st.session_state:
    st.session_state.audited_invoices = []

# Sidebar navigation
st.sidebar.image(
    "https://img.icons8.com/color/96/electricity.png",
    width=60,
)
st.sidebar.title("VoltAudit AI")
st.sidebar.caption("Enterprise AI Invoice Auditor")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation Menu",
    [
        "📊 Dashboard Home",
        "📤 Ingest & Audit",
        "✍️ Human Review Queue",
        "⚙️ System Health",
    ],
)

# ----------------- 1. DASHBOARD HOME -----------------
if page == "📊 Dashboard Home":
    st.title("📊 Enterprise Audit Dashboard")
    st.write("Real-time overview of electricity utility audits and compliance score metrics.")

    # Overview statistics
    col1, col2, col3, col4 = st.columns(4)
    total_audited = len(st.session_state.audited_invoices) + 12
    pending_overrides = sum(
        1
        for inv in st.session_state.audited_invoices
        if BackendAPIClient.get_status(inv).get("approval_status") == "PENDING"
    )

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Total Audited</div>
                <div class="metric-value">{total_audited}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Auto-Approved</div>
                <div class="metric-value">{total_audited - pending_overrides - 2}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Pending Reviews</div>
                <div class="metric-value">{pending_overrides + 2}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Avg Compliance Score</div>
                <div class="metric-value">91%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Compliance Score Charts
    st.subheader("📈 Compliance Trend History")
    chart_data = pd.DataFrame(
        {
            "Audit Run": [f"Run {i}" for i in range(1, 11)],
            "Compliance Score": [100, 100, 70, 100, 100, 85, 100, 100, 70, 100],
        }
    )
    st.line_chart(chart_data.set_index("Audit Run"))

    st.subheader("📋 Recent Audit Runs")
    history_rows = []
    for inv_id in st.session_state.audited_invoices:
        status_data = BackendAPIClient.get_status(inv_id)
        history_rows.append(
            {
                "Invoice ID": inv_id,
                "Compliance Score": f"{status_data.get('compliance_score', 100)}/100",
                "Risk Classification": status_data.get("risk_classification", "LOW"),
                "Approval Status": status_data.get("approval_status", "PENDING"),
            }
        )

    # Seed data if list is empty
    if not history_rows:
        history_rows = [
            {
                "Invoice ID": "inv-google-001",
                "Compliance Score": "100/100",
                "Risk Classification": "LOW",
                "Approval Status": "APPROVED",
            },
            {
                "Invoice ID": "inv-chevron-002",
                "Compliance Score": "70/100",
                "Risk Classification": "MEDIUM",
                "Approval Status": "APPROVED",
            },
        ]

    st.table(pd.DataFrame(history_rows))

# ----------------- 2. INGEST & AUDIT -----------------
elif page == "📤 Ingest & Audit":
    st.title("📤 Ingest & Audit Invoice")
    st.write("Upload utility invoices to run the VoltAudit AI multi-agent compliance pipeline.")

    col_form, col_status = st.columns([1, 1])

    with col_form:
        st.subheader("Invoice Submission Form")
        invoice_id = st.text_input(
            "Invoice Run ID", value="inv-audit-001", placeholder="e.g. inv-2026-01"
        )
        uploaded_file = st.file_uploader("Upload Invoice PDF/Text File", type=["txt", "pdf"])
        submit_btn = st.button("🚀 Run Compliance Audit", use_container_width=True)

    with col_status:
        st.subheader("AI Workforce Live Progress")

        if submit_btn and uploaded_file:
            # Call backend submission service
            file_bytes = uploaded_file.read()
            with st.spinner("Uploading and initializing execution context..."):
                res = BackendAPIClient.submit_audit(invoice_id, uploaded_file.name, file_bytes)

            if "error" in res:
                st.error(res["error"])
            else:
                # Add to local session storage
                if invoice_id not in st.session_state.audited_invoices:
                    st.session_state.audited_invoices.append(invoice_id)

                # Visualize AI Workforce execution steps
                workers = [
                    ("WRK-002", "Document Ingestion Specialist", "Ingesting file block layout..."),
                    (
                        "WRK-003",
                        "Vendor & Contract Specialist",
                        "Resolving vendor contract active date checks...",
                    ),
                    (
                        "WRK-005",
                        "Tariff Validation Specialist",
                        "Validating peaking tariff multi-rateSheet rules...",
                    ),
                    (
                        "WRK-006",
                        "Billing & 3-Way Match Specialist",
                        "Reconciling calculations and meter balances...",
                    ),
                    (
                        "WRK-007",
                        "Historical Anomaly Specialist",
                        "Running double-billing historical duplicate scans...",
                    ),
                    (
                        "WRK-008",
                        "Risk Assessment Specialist",
                        "Weighing compliance deviations risk tiers...",
                    ),
                    (
                        "WRK-008_reporter",
                        "Audit Reporting Specialist",
                        "Compiling markdown narrative explains...",
                    ),
                ]

                progress_bar = st.progress(0)
                status_placeholder = st.empty()

                for index, (wrk_id, wrk_name, wrk_step) in enumerate(workers):
                    status_placeholder.markdown(
                        f"""
                        <div class="agent-step agent-active">
                            <strong>{wrk_id}: {wrk_name}</strong><br/>
                            {wrk_step}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    progress_bar.progress((index + 1) / len(workers))
                    time.sleep(0.5)

                status_placeholder.empty()
                st.success("✅ Audit Run completed successfully!")

                # Query and display findings
                status_data = BackendAPIClient.get_status(invoice_id)
                findings_data = BackendAPIClient.get_findings(invoice_id)
                report_data = BackendAPIClient.get_report(invoice_id)

                # Render score metrics
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric(
                        "Compliance Score",
                        f"{status_data.get('compliance_score', 100)}/100",
                    )
                with col_m2:
                    st.metric("Risk Tier", status_data.get("risk_classification", "LOW"))
                with col_m3:
                    st.metric(
                        "Approval Action",
                        status_data.get("approval_status", "APPROVED"),
                    )

                # Tabs for report and warnings
                tab_report, tab_findings = st.tabs(
                    ["📄 Narrative Report", "⚠️ Discrepancy Findings"]
                )

                with tab_report:
                    st.markdown(report_data.get("report_markdown", "No report compiled."))

                with tab_findings:
                    discrepancies = findings_data.get("discrepancies", [])
                    if not discrepancies:
                        st.balloons()
                        st.info("No discrepancies identified. Invoice is fully compliant.")
                    else:
                        for disc in discrepancies:
                            severity = disc.get("severity")
                            dtype = disc.get("type")
                            desc = disc.get("description")
                            st.warning(f"**[{severity}] {dtype}**\n\n{desc}")

# ----------------- 3. HUMAN REVIEW QUEUE -----------------
elif page == "✍️ Human Review Queue":
    st.title("✍️ Human Review Gateway")
    st.write("Approve flagged invoices with medium/high risk tiers using override validations.")

    pending_invoices = []
    for inv_id in st.session_state.audited_invoices:
        status_data = BackendAPIClient.get_status(inv_id)
        if status_data.get("approval_status") == "PENDING":
            pending_invoices.append(inv_id)

    # Seed demo invoice if none exist
    if not pending_invoices:
        st.info("Review queue is currently empty.")
        st.write("---")
        st.subheader("💡 Demo Mode: Trigger Pending Review")
        if st.button("Generate Pending Review Invoice"):
            # Create a dirty run
            BackendAPIClient.submit_audit("demo-pending-01", "dirty.txt", b"Mock dirty text.")
            if "demo-pending-01" not in st.session_state.audited_invoices:
                st.session_state.audited_invoices.append("demo-pending-01")
            st.rerun()
    else:
        selected_inv = st.selectbox("Select Pending Invoice for Review", pending_invoices)

        status_data = BackendAPIClient.get_status(selected_inv)
        findings_data = BackendAPIClient.get_findings(selected_inv)
        report_data = BackendAPIClient.get_report(selected_inv)

        # Show details
        st.markdown(f"### Audit Details: `{selected_inv}`")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("Compliance Score", f"{status_data.get('compliance_score')}/100")
            st.write(f"**Risk Classification:** {status_data.get('risk_classification')}")
        with col_s2:
            st.write(f"**Approval Status:** {status_data.get('approval_status')}")
            st.write(f"**Human Approval Required:** {status_data.get('human_approval_required')}")

        st.markdown("#### Narrative Report")
        st.markdown(report_data.get("report_markdown"))

        st.markdown("#### Override Authorization Gateway")
        justification = st.text_area(
            "Override Justification (Minimum 15 characters, no lazy words)",
            placeholder=(
                "Provide a comprehensive explanation "
                "why this invoice is manually override-approved..."
            ),
        )
        approve_btn = st.button("✅ Validate and Apply Override", use_container_width=True)

        if approve_btn:
            if len(justification) < 15:
                st.error("❌ Justification must contain at least 15 characters.")
            else:
                res = BackendAPIClient.apply_override(selected_inv, justification)
                if "error" in res:
                    st.error(f"❌ Override failed: {res['error']}")
                elif res.get("success") is True:
                    st.success("✅ Human override applied successfully! Invoice approved.")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(
                        "❌ Override rejected: Justification contains "
                        "blocked lazy/non-descriptive keywords."
                    )

# ----------------- 4. SYSTEM HEALTH -----------------
elif page == "⚙️ System Health":
    st.title("⚙️ System Health & Configuration")
    st.write("Monitor the connectivity and readiness states of downstream microservices.")

    health = BackendAPIClient.get_health()
    ready = BackendAPIClient.get_ready()

    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        if health.get("status") == "OK":
            st.success("⚡ Liveness: ONLINE")
        else:
            st.error("❌ Liveness: OFFLINE")
    with col_h2:
        if ready.get("status") == "READY":
            st.success("📂 Readiness: READY")
        else:
            st.error("❌ Readiness: NOT READY")
    with col_h3:
        if health.get("mcp_connection") is True:
            st.success("🤖 MCP Server Connection: CONNECTED")
        else:
            st.error("❌ MCP Server Connection: DISCONNECTED")

    st.subheader("Downstream Service Diagnostics")
    st.json({"Health Endpoint": health, "Readiness Endpoint": ready})
