from datetime import datetime

import streamlit as st

from inference.prediction_freight import predict_freight_cost
from inference.predict_invice_flag import predict_invoice_flag

# ---------------------------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Vendor Invoice Intelligence Portal",
    page_icon="📦",
    layout="wide",
)

# ---------------------------------------------------------------------------
# DESIGN TOKENS + GLOBAL CSS  (colors / type taken from the Stitch export)
# ---------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --bg: #f8f9ff;
  --surface: #ffffff;
  --surface-low: #eff4ff;
  --surface-high: #dce9ff;
  --ink: #0b1c30;
  --ink-soft: #464555;
  --outline: #777587;
  --primary: #3525cd;
  --primary-hover: #4f46e5;
  --teal: #006b5f;
  --teal-tint: #d9f5f0;
  --error: #ba1a1a;
  --error-tint: #ffe9e6;
  --navy: #213145;
}

html, body, [class*="css"], .stApp, .stMarkdown, button, input, label {
  font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif !important;
}
.material-symbols-outlined {
  font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important;
  font-weight: normal; font-style: normal; line-height: 1;
  letter-spacing: normal; text-transform: none; display: inline-block;
  white-space: nowrap; word-wrap: normal; direction: ltr;
  font-feature-settings: 'liga'; -webkit-font-smoothing: antialiased;
  vertical-align: middle;
}

.stApp { background: var(--bg); color: var(--ink); }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1240px; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] { background: var(--navy); border-right: none; position: relative; }
[data-testid="stSidebar"] * { color: #eaf1ff; }
[data-testid="stSidebar"] [role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
  padding: 10px 14px; border-radius: 8px; cursor: pointer;
  transition: background .15s ease; width: 100%;
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child,
[data-testid="stSidebar"] [role="radiogroup"] label > div > div:first-child:not(:only-child) { display: none !important; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: rgba(211,228,254,.10); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
  background: var(--primary-hover); box-shadow: 0 1px 2px rgba(0,0,0,.25);
}
[data-testid="stSidebar"] [role="radiogroup"] label p { font-size: 15px; font-weight: 500; color: #dbe6f7; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p { color: #fff; font-weight: 600; }

.brand { display: flex; align-items: center; gap: 12px; padding: 4px 4px 22px; }
.brand-logo {
  width: 40px; height: 40px; border-radius: 10px; background: var(--primary-hover);
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.brand-logo .material-symbols-outlined { color: #fff; font-size: 22px; }
.brand-title { font-size: 16px; font-weight: 700; letter-spacing: -.01em; line-height: 1.25; color: #fff !important; }
.brand-sub { font-size: 13px; color: #dbe6f7 !important; display: flex; align-items: center; gap: 8px; }
.brand-badge {
  background: #3323cc; color: #fff !important; font-size: 11px; font-weight: 700;
  letter-spacing: .04em; padding: 3px 8px; border-radius: 6px;
}

/* Business impact card, pinned to the bottom of the sidebar */
[data-testid="stSidebar"] [data-testid="stElementContainer"]:has([data-testid="stRadio"]) { width: 100% !important; }
[data-testid="stSidebar"] [data-testid="stRadio"],
[data-testid="stSidebar"] [role="radiogroup"],
[data-testid="stSidebar"] [role="radiogroup"] > div { width: 100% !important; }
[data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.impact) { position: static !important; height: 0; }
.impact {
  position: absolute; left: 20px; right: 20px; bottom: 16px;
  padding: 16px; border-radius: 12px;
  background: rgba(211,228,254,.10); border: 1px solid rgba(160,170,195,.30);
}
.impact-title {
  display: flex; align-items: center; gap: 8px;
  font-size: 13px; font-weight: 500; letter-spacing: .06em; text-transform: uppercase;
  color: #71f8e4 !important; margin-bottom: 12px;
}
.impact-title .material-symbols-outlined { font-size: 18px; color: #71f8e4 !important; }
.impact-item { display: flex; align-items: center; gap: 10px; font-size: 13px; padding: 4px 0; color: #eaf1ff !important; }
.impact-item .material-symbols-outlined { font-size: 17px; color: #71f8e4 !important; }

/* ---------- Hero ---------- */
.hero h1 {
  font-size: 34px; line-height: 1.15; font-weight: 700; letter-spacing: -.025em;
  color: var(--ink); margin: 0; padding: 0;
}
.hero p { font-size: 16px; color: var(--ink-soft); margin: 6px 0 14px; }
.chips { display: flex; flex-wrap: wrap; gap: 10px; }
.chip {
  display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 999px;
  background: var(--surface); font-size: 13px; font-weight: 500; color: var(--ink);
  box-shadow: 0 1px 2px rgba(11,28,48,.08);
}
.chip .material-symbols-outlined { font-size: 18px; }

.section-head { margin: 34px 0 18px; }
.section-head h2 { font-size: 26px; font-weight: 600; letter-spacing: -.02em; margin: 0 0 4px; color: var(--ink); padding: 0; }
.section-head p { font-size: 14px; color: var(--ink-soft); margin: 0; max-width: 820px; }

/* ---------- Cards ---------- */
.card {
  background: var(--surface); border-radius: 16px; padding: 24px;
  box-shadow: 0 1px 3px rgba(11,28,48,.07); height: 100%;
}
.card-title { font-size: 18px; font-weight: 600; letter-spacing: -.01em; color: var(--ink); margin: 0; }
.card-sub { font-size: 13px; color: var(--ink-soft); margin: 2px 0 0; }
.card-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-bottom: 16px; }

.badge {
  display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 999px;
  font-size: 12px; font-weight: 600; white-space: nowrap;
}
.badge::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.badge.ok { background: var(--teal-tint); color: var(--teal); }
.badge.bad { background: var(--error); color: #fff; }
.badge.idle { background: var(--surface-low); color: var(--outline); }

.metric-box { background: var(--surface-low); border-radius: 12px; padding: 22px; margin-top: 8px; }
.metric-label { font-size: 12px; font-weight: 600; color: var(--ink-soft); }
.metric-value { font-size: 44px; line-height: 1.1; font-weight: 700; letter-spacing: -.025em; color: var(--ink); margin: 4px 0 6px; font-variant-numeric: tabular-nums; }
.metric-note { font-size: 14px; color: var(--ink-soft); }
.metric-note b { color: var(--ink); }

.empty { text-align: center; padding: 46px 16px; color: var(--outline); }
.empty .material-symbols-outlined { font-size: 40px; background: var(--primary); border-radius: 12px; padding: 8px; color: #fff; }
.empty h4 { font-size: 16px; font-weight: 600; color: var(--ink); margin: 14px 0 4px; }
.empty p { font-size: 13px; margin: 0; }

.ratio { display: flex; justify-content: space-between; align-items: center; padding: 11px 14px; border-radius: 12px; background: var(--surface-low); margin-bottom: 10px; }
.ratio .k { font-size: 13px; color: var(--ink-soft); }
.ratio .v { font-size: 14px; font-weight: 700; color: var(--ink); font-variant-numeric: tabular-nums; }

/* ---------- Result banners ---------- */
.banner { display: flex; align-items: center; gap: 16px; border-radius: 16px; padding: 22px 24px; box-shadow: 0 1px 3px rgba(11,28,48,.07); }
.banner .icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.banner .icon .material-symbols-outlined { font-size: 28px; color: #fff; }
.banner h4 { margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -.01em; padding: 0; }
.banner p { margin: 4px 0 0; font-size: 14px; }
.banner.bad { background: var(--error-tint); }
.banner.bad .icon { background: var(--error); }
.banner.bad h4 { color: #93000a; }
.banner.bad p { color: #93000a; opacity: .85; }
.banner.ok { background: var(--teal-tint); }
.banner.ok .icon { background: var(--teal); }
.banner.ok h4 { color: var(--ink); }
.banner.ok p { color: var(--ink-soft); }
.banner.idle { background: var(--surface); }
.banner.idle .icon { background: var(--surface-high); }
.banner.idle .icon .material-symbols-outlined { color: var(--primary); }
.banner.idle h4 { color: var(--ink); }
.banner.idle p { color: var(--ink-soft); }

.block-title { font-size: 18px; font-weight: 600; letter-spacing: -.01em; color: var(--ink); margin: 30px 0 12px; }

/* ---------- Table ---------- */
.tbl-wrap { overflow-x: auto; }
table.tbl { width: 100%; border-collapse: collapse; font-size: 14px; border: none; }
table.tbl th, table.tbl td { border-left: none !important; border-right: none !important; border-top: none !important; }
table.tbl thead th {
  background: var(--surface-low); color: var(--outline); font-size: 12px; font-weight: 600;
  text-align: left; padding: 12px 16px;
}
table.tbl thead th:first-child { border-radius: 8px 0 0 8px; }
table.tbl thead th:last-child { border-radius: 0 8px 8px 0; }
table.tbl tbody td { padding: 13px 16px; border-bottom: 1px solid var(--surface-low); color: var(--ink); font-variant-numeric: tabular-nums; }
table.tbl tbody tr:last-child td { border-bottom: none; }

/* ---------- Forms (the input cards) ---------- */
[data-testid="stForm"] {
  background: var(--surface); border: none; border-radius: 16px; padding: 24px;
  box-shadow: 0 1px 3px rgba(11,28,48,.07);
}
[data-testid="stWidgetLabel"] p { font-size: 13px; font-weight: 600; color: var(--ink); }

/* Number inputs: force the grey box in BOTH light and dark system themes.
   Streamlit's real background wrapper is stNumberInputContainer -
   not data-baseweb="input"/"base-input", which is why the previous rule never matched. */
[data-testid="stNumberInputContainer"] {
  background-color: #eff4ff !important; border: none !important; border-radius: 8px !important;
}
[data-testid="stNumberInput"] input {
  color: #0b1c30 !important; background-color: transparent !important;
  font-weight: 500; font-variant-numeric: tabular-nums;
}
[data-testid="stNumberInputContainer"]:focus-within {
  background-color: #fff !important; box-shadow: 0 0 0 2px rgba(53,37,205,.25) !important;
}
[data-testid="stNumberInput"] button {
  background: transparent !important; color: #777587 !important;
}
[data-testid="stNumberInput"] button svg { fill: #777587 !important; }
[data-testid="stNumberInput"] button:hover {
  color: #4f46e5 !important; background: #dce9ff !important;
}
[data-testid="stNumberInput"] button:hover svg { fill: #4f46e5 !important; }

[data-testid="stFormSubmitButton"] button {
  width: 100%; height: 48px; border: none; border-radius: 8px;
  background: var(--primary); color: #fff; font-weight: 600; font-size: 15px;
  box-shadow: 0 1px 2px rgba(11,28,48,.2); transition: background .15s ease, transform .05s ease;
}
[data-testid="stFormSubmitButton"] button p { color: #fff; font-size: 15px; font-weight: 600; }
[data-testid="stFormSubmitButton"] button:hover { background: var(--primary-hover); border: none; color: #fff; }
[data-testid="stFormSubmitButton"] button:active { transform: scale(.99); }
[data-testid="stFormSubmitButton"] button:focus-visible { outline: 3px solid rgba(53,37,205,.35); outline-offset: 2px; }

[data-testid="stAlert"] { border-radius: 12px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def html(markup):
    """Render an HTML snippet (collapsed to one line so Markdown never treats it as code)."""
    flat = " ".join(line.strip() for line in markup.strip().splitlines())
    st.markdown(flat, unsafe_allow_html=True)


def icon(name, color=None):
    style = f' style="color:{color}"' if color else ""
    return f'<span class="material-symbols-outlined"{style}>{name}</span>'


# ---------------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------------
st.session_state.setdefault("freight_result", None)
st.session_state.setdefault("flag_result", None)
st.session_state.setdefault("flag_history", [])

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
NAV = {
    "Freight Cost Prediction": (":material/local_shipping:", "Freight Cost Prediction"),
    "Invoice Manual Approval Flag": (":material/verified_user:", "Invoice Approval Flag"),
}

with st.sidebar:
    html(
        f"""
        <div class="brand">
          <div class="brand-logo">{icon("receipt_long")}</div>
          <div>
            <div class="brand-title">Vendor Invoice</div>
            <div class="brand-sub">Intelligence <span class="brand-badge">PORTAL</span></div>
          </div>
        </div>
        """
    )
    selected_model = st.radio(
        "Choose a model to use:",
        list(NAV.keys()),
        format_func=lambda name: f"{NAV[name][0]}  {NAV[name][1]}",
        label_visibility="collapsed",
    )
    html(
        f"""
        <div class="impact">
          <div class="impact-title">{icon("auto_awesome")} Business impact</div>
          <div class="impact-item">{icon("check_circle")} Improves cost forecasting</div>
          <div class="impact-item">{icon("check_circle")} Reduces fraud &amp; anomalies</div>
          <div class="impact-item">{icon("check_circle")} Faster finance operations</div>
        </div>
        """
    )

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
html(
    f"""
    <div class="hero">
      <h1>Vendor Invoice Intelligence Portal</h1>
      <p>AI-driven vendor invoice risk assessment and freight cost prediction</p>
      <div class="chips">
        <span class="chip">{icon("trending_up", "#3525cd")} Forecast freight costs accurately</span>
        <span class="chip">{icon("verified_user", "#006b5f")} Detect risky or abnormal invoices</span>
        <span class="chip">{icon("savings", "#4f46e5")} Reduce financial leakage and manual workload</span>
      </div>
    </div>
    """
)

# ===========================================================================
# FREIGHT COST PREDICTION
# ===========================================================================
if selected_model == "Freight Cost Prediction":
    html(
        """
        <div class="section-head">
          <h2>Freight Cost Prediction</h2>
          <p>Predict freight cost for a vendor invoice based on invoice dollars to support
          budgeting, forecasting and vendor negotiations.</p>
        </div>
        """
    )

    left, right = st.columns(2, gap="large")

    with left:
        with st.form("freight_form"):
            dollars = st.number_input(
                "Invoice Dollars ($)",
                min_value=1.0,
                value=18500.0,
                step=1000.0,
                format="%.2f",
                help="Total billed invoice amount",
            )
            submit_freight = st.form_submit_button(
                "Predict Freight Cost", type="primary", icon=":material/auto_awesome:"
            )

    if submit_freight:
        try:
            with st.spinner("Running freight model..."):
                input_data = {"Dollars": [dollars]}
                prediction = predict_freight_cost(input_data)["Predict_Freight"]
                freight_value = float(prediction[0])
            st.session_state.freight_result = {
                "dollars": dollars,
                "freight": freight_value,
                "time": datetime.now().strftime("%H:%M:%S"),
                "error": None,
            }
        except Exception as exc:  # noqa: BLE001
            st.session_state.freight_result = {"error": str(exc)}

    with right:
        result = st.session_state.freight_result
        if result is None:
            html(
                f"""
                <div class="card">
                  <div class="card-head"><div>
                    <div class="card-title">Estimated Freight Cost</div>
                    <div class="card-sub">Predicted output</div></div>
                    <span class="badge idle">Awaiting input</span>
                  </div>
                  <div class="empty">{icon("local_shipping")}
                    <h4>No prediction yet</h4>
                    <p>Enter an invoice amount and click <b>Predict Freight Cost</b>.</p>
                  </div>
                </div>
                """
            )
        elif result.get("error"):
            html(
                f"""
                <div class="card">
                  <div class="card-head"><div>
                    <div class="card-title">Estimated Freight Cost</div>
                    <div class="card-sub">Predicted output</div></div>
                    <span class="badge bad">Prediction failed</span>
                  </div>
                  <div class="banner bad"><div class="icon">{icon("error")}</div>
                    <div><h4>Something went wrong</h4><p>{result["error"]}</p></div>
                  </div>
                </div>
                """
            )
        else:
            pct = result["freight"] / result["dollars"] * 100
            html(
                f"""
                <div class="card">
                  <div class="card-head"><div>
                    <div class="card-title">Estimated Freight Cost</div>
                    <div class="card-sub">Predicted at {result["time"]}</div></div>
                    <span class="badge ok">Prediction completed</span>
                  </div>
                  <div class="metric-box">
                    <div class="metric-label">Expected freight cost</div>
                    <div class="metric-value">${result["freight"]:,.2f}</div>
                    <div class="metric-note"><b>{pct:.2f}%</b> of the ${result["dollars"]:,.2f} invoice total</div>
                  </div>
                </div>
                """
            )

# ===========================================================================
# INVOICE MANUAL APPROVAL FLAG
# ===========================================================================
else:
    html(
        """
        <div class="section-head">
          <h2>Invoice Manual Approval Flag</h2>
          <p>Predict whether a vendor invoice requires manual approval based on abnormal
          cost, freight, or delivery patterns.</p>
        </div>
        """
    )

    form_col, ratio_col = st.columns([2, 1], gap="large")

    with form_col:
        with st.form("invoice_flag_form"):
            html(
                """
                <div class="card-title">Invoice Parameter Assessment</div>
                <div class="card-sub" style="margin-bottom:14px">
                  Enter the five invoice metrics to evaluate anomaly likelihood</div>
                """
            )
            c1, c2, c3 = st.columns(3)
            with c1:
                invoice_quantity = st.number_input(
                    "Invoice Quantity", min_value=1, value=50, step=1,
                    help="Units on the invoice",
                )
            with c2:
                freight = st.number_input(
                    "Freight Cost ($)", min_value=0.0, value=1.73, step=1.0, format="%.2f",
                    help="Reported carrier freight fee",
                )
            with c3:
                invoice_dollars = st.number_input(
                    "Invoice Dollars ($)", min_value=1.0, value=352.95, step=25.0, format="%.2f",
                    help="Total gross amount billed",
                )

            c4, c5, _ = st.columns(3)
            with c4:
                total_item_quantity = st.number_input(
                    "Total Item Quantity", min_value=1, value=162, step=5,
                    help="Sum of items received",
                )
            with c5:
                total_item_dollars = st.number_input(
                    "Total Item Dollars ($)", min_value=0.0, value=2476.0, step=100.0, format="%.2f",
                    help="Aggregated item value",
                )

            submit_flag = st.form_submit_button(
                "Evaluate Invoice Risk", type="primary", icon=":material/manage_search:"
            )

    if submit_flag:
        try:
            with st.spinner("Evaluating invoice..."):
                input_data = {
                    "invoice_quantity": [invoice_quantity],
                    "invoice_dollars": [invoice_dollars],
                    "Freight": [freight],
                    "total_item_quantity": [total_item_quantity],
                    "total_item_dollars": [total_item_dollars],
                }
                flag_prediction = predict_invoice_flag(input_data)["flag_invoice"]
                is_flagged = bool(flag_prediction[0])

            record = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "invoice_quantity": invoice_quantity,
                "freight": freight,
                "invoice_dollars": invoice_dollars,
                "total_item_quantity": total_item_quantity,
                "total_item_dollars": total_item_dollars,
                "flagged": is_flagged,
                "error": None,
            }
            st.session_state.flag_result = record
            st.session_state.flag_history.insert(0, record)
            st.session_state.flag_history = st.session_state.flag_history[:10]
        except Exception as exc:  # noqa: BLE001
            st.session_state.flag_result = {"error": str(exc)}

    res = st.session_state.flag_result

    # ---- Ratios computed from the last evaluated invoice (no model involved) ----
    with ratio_col:
        if res and not res.get("error"):
            freight_per_unit = res["freight"] / res["invoice_quantity"]
            freight_pct = res["freight"] / res["invoice_dollars"] * 100
            items_vs_invoice = res["total_item_dollars"] / res["invoice_dollars"]
            qty_delta = res["total_item_quantity"] - res["invoice_quantity"]
            rows = [
                ("Freight per unit", f"${freight_per_unit:,.2f}"),
                ("Freight as % of invoice", f"{freight_pct:.2f}%"),
                ("Item $ / Invoice $", f"{items_vs_invoice:,.2f}x"),
                ("Quantity difference", f"{qty_delta:+,d}"),
            ]
            body = "".join(
                f'<div class="ratio"><span class="k">{k}</span><span class="v">{v}</span></div>'
                for k, v in rows
            )
            sub = f"From the invoice evaluated at {res['time']}"
        else:
            body = (
                f'<div class="empty" style="padding:30px 8px">{icon("insights")}'
                "<h4>No data yet</h4><p>Ratios appear after you evaluate an invoice.</p></div>"
            )
            sub = "Derived from your inputs"
        html(
            f"""
            <div class="card">
              <div class="card-head"><div>
                <div class="card-title">Input Ratios</div>
                <div class="card-sub">{sub}</div></div>
              </div>
              {body}
            </div>
            """
        )

    # ---- Evaluation output ----
    html('<div class="block-title">Evaluation Output</div>')

    if res is None:
        html(
            f"""
            <div class="banner idle"><div class="icon">{icon("manage_search")}</div>
              <div><h4>Awaiting evaluation</h4>
              <p>Fill in the invoice details above and click <b>Evaluate Invoice Risk</b>.</p></div>
            </div>
            """
        )
    elif res.get("error"):
        html(
            f"""
            <div class="banner bad"><div class="icon">{icon("error")}</div>
              <div><h4>Evaluation failed</h4><p>{res["error"]}</p></div>
            </div>
            """
        )
    elif res["flagged"]:
        html(
            f"""
            <div class="banner bad"><div class="icon">{icon("warning")}</div>
              <div><h4>Invoice requires MANUAL APPROVAL</h4>
              <p>This invoice was flagged for review based on its cost, freight, or quantity pattern.</p></div>
            </div>
            """
        )
    else:
        html(
            f"""
            <div class="banner ok"><div class="icon">{icon("check_circle")}</div>
              <div><h4>Invoice is SAFE for AUTO approval</h4>
              <p>No abnormal cost, freight, or quantity pattern was detected.</p></div>
            </div>
            """
        )

    # ---- Recent evaluations (this session) ----
    if st.session_state.flag_history:
        head_l, head_r = st.columns([5, 1])
        with head_l:
            html('<div class="block-title">Recent Evaluations</div>')
        with head_r:
            st.write("")
            st.write("")
            if st.button("Clear", key="clear_history"):
                st.session_state.flag_history = []
                st.rerun()

        rows_html = ""
        for h in st.session_state.flag_history:
            pill = (
                '<span class="badge bad">Manual review</span>'
                if h["flagged"]
                else '<span class="badge ok">Auto approved</span>'
            )
            rows_html += (
                f"<tr><td>{h['time']}</td><td>{h['invoice_quantity']:,}</td>"
                f"<td>${h['invoice_dollars']:,.2f}</td><td>${h['freight']:,.2f}</td>"
                f"<td>{h['total_item_quantity']:,}</td><td>${h['total_item_dollars']:,.2f}</td>"
                f"<td>{pill}</td></tr>"
            )
        html(
            f"""
            <div class="card"><div class="tbl-wrap"><table class="tbl">
              <thead><tr><th>Time</th><th>Invoice qty</th><th>Invoice $</th><th>Freight</th>
              <th>Item qty</th><th>Item $</th><th>Result</th></tr></thead>
              <tbody>{rows_html}</tbody>
            </table></div></div>
            """
        )