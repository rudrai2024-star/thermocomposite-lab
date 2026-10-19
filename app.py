"""ThermoComposite Lab analytics workspace."""

from __future__ import annotations

from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from thermo_composite.materials import MATERIALS, ValidationError
from thermo_composite.clt import NumericalError
from thermo_composite.background import render_composite_background
from thermo_composite.reporting import result_to_json
from thermo_composite.simulation import LaminateInput, SimulationInput, run_simulation


st.set_page_config(page_title="ThermoComposite Lab", page_icon="◌", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --ink:#f4f5ee; --muted:#929798; --panel:#1d2024; --panel2:#24282d; --line:#30353a; --lime:#d7ff3f; --orange:#ff9b55; }
html, body, [class*="css"] { font-family: 'Manrope', sans-serif; }
.stApp { background:#101214; color:var(--ink); }
[data-testid="stAppViewContainer"] { position:relative; z-index:1; }
.tc-background { position:fixed; inset:0; z-index:0; overflow:hidden; pointer-events:none;
                 contain:strict; background:#101214; }
.tc-background__island { position:absolute; inset:-12%; opacity:.075; background:rgb(52,65,73);
                         filter:url(#tc-octave-one) brightness(1.4) contrast(1.15); }
.tc-background__island--secondary { opacity:.045; background:rgb(67,81,87);
                                    filter:url(#tc-octave-two) brightness(1.25) contrast(1.1); }
.tc-background__filters { position:absolute; width:0; height:0; overflow:hidden; }
.tc-welcome-shell { min-height:calc(100vh - 3rem); display:grid; place-items:center; padding:3rem 1.5rem; }
.tc-welcome-form { width:min(100%, 470px); padding:30px; background:rgba(29,32,36,.94); border:1px solid #30363a;
                   border-radius:18px; box-shadow:0 22px 70px rgba(0,0,0,.28); }
.tc-welcome-kicker { color:var(--lime); font:500 10px 'DM Mono',monospace; letter-spacing:.14em; text-transform:uppercase; }
.tc-welcome-title { color:var(--ink); font-size:30px; font-weight:800; letter-spacing:-.05em; line-height:1.1; margin:12px 0 8px; }
.tc-welcome-copy { color:#929798; font-size:13px; line-height:1.7; margin:0 0 24px; }
.tc-welcome-form [data-testid="stFormSubmitButton"] button { width:100%; margin-top:14px; }
.tc-welcome-meta { color:#687174; font:10px 'DM Mono',monospace; letter-spacing:.08em; text-align:center; margin-top:22px; }
[data-testid="stSidebar"] { background:#141617; border-right:1px solid #25292c; }
[data-testid="stSidebar"] > div:first-child { padding:1rem .85rem 1.25rem; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap:.35rem; }
.st-key-brand_home button { width:100%; min-height:58px; padding:0 10px; background:transparent !important; border:0 !important; color:var(--ink) !important; box-shadow:none !important; text-align:left; font-size:13px; letter-spacing:.12em; font-weight:800; }
.st-key-brand_home button:hover { background:#1c2022 !important; color:var(--ink) !important; }
.st-key-brand_home button:focus-visible { outline:2px solid var(--lime); outline-offset:2px; }
.eyebrow { color:var(--lime); font:500 11px 'DM Mono', monospace; text-transform:uppercase; letter-spacing:.1em; }
h1 { letter-spacing:-.055em !important; font-size:42px !important; line-height:1.05 !important; }
h2, h3 { letter-spacing:-.035em; }
.hero { background:linear-gradient(120deg,#1b1e21 0%,#151719 70%); border:1px solid var(--line); border-radius:22px; padding:28px 32px; margin-bottom:18px; }
.hero-copy { max-width:720px; }
.hero p { color:#aeb4b2; font-size:14px; line-height:1.7; max-width:680px; }
.status { display:inline-flex; gap:8px; align-items:center; color:#b9c0bd; font:11px 'DM Mono',monospace; }
.dot { width:7px; height:7px; border-radius:50%; background:var(--lime); box-shadow:0 0 0 4px #d7ff3f18; }
.card { background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:19px; min-height:100%; }
.card-label { color:var(--muted); text-transform:uppercase; letter-spacing:.08em; font:10px 'DM Mono',monospace; }
.card-value { font-size:25px; font-weight:700; letter-spacing:-.04em; margin-top:12px; }
.card-note { color:#78907e; font-size:11px; margin-top:6px; }
.section-title { font-size:18px; font-weight:700; margin:24px 0 12px; }
.tag { display:inline-block; color:var(--lime); border:1px solid #d7ff3f55; border-radius:20px; padding:4px 9px; font:10px 'DM Mono',monospace; margin-right:5px; }
.warning { background:#2a241c; border:1px solid #765835; color:#e8c897; border-radius:12px; padding:12px 14px; font-size:12px; line-height:1.6; }
.empty { border:1px dashed #3a4145; border-radius:16px; padding:36px; color:var(--muted); text-align:center; }
div[data-testid="stMetric"] { background:var(--panel); border:1px solid var(--line); padding:15px; border-radius:14px; }
div[data-testid="stMetricLabel"] { color:var(--muted); }
div[data-testid="stMetricValue"] { color:var(--ink); }
button[kind="primary"] { background:var(--lime) !important; color:#101214 !important; border:0 !important; }
.stButton button, .stDownloadButton button { border-radius:9px; }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; }
[data-testid="stSidebar"] [role="radiogroup"] { gap:3px; }
[data-testid="stSidebar"] [role="radiogroup"] label { min-height:34px; padding:0 9px; border-radius:7px; transition:background .15s ease, color .15s ease; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background:#1c2022; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) { background:#202528; color:var(--ink); box-shadow:inset 2px 0 0 var(--lime); }
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { transform:scale(.72); transform-origin:center; }
[data-testid="stSidebar"] [role="radiogroup"] p { font-size:12px; }
[data-testid="stSidebar"] hr { margin:10px 0; border-color:#25292c; }
.st-key-sidebar_toggle { display:flex; justify-content:flex-end; }
.st-key-sidebar_toggle button { position:relative; width:40px; min-width:40px; height:40px; padding:0; border:1px solid #30363a !important; border-radius:9px; background:#1a1e20 !important; color:transparent !important; overflow:hidden; }
.st-key-sidebar_toggle button::before,
.st-key-sidebar_toggle button::after,
.st-key-sidebar_toggle button > div::before { content:""; position:absolute; left:10px; width:18px; height:2px; border-radius:2px; background:var(--lime); transition:transform .35s ease, opacity .2s ease, top .35s ease; }
.st-key-sidebar_toggle button::before { top:12px; }
.st-key-sidebar_toggle button > div::before { top:18px; }
.st-key-sidebar_toggle button::after { top:24px; }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) .st-key-sidebar_toggle button::before { top:18px; transform:rotate(45deg); }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) .st-key-sidebar_toggle button::after { top:18px; transform:rotate(-45deg); }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) .st-key-sidebar_toggle button > div::before { opacity:0; transform:scaleX(0); }
.st-key-sidebar_toggle button:focus-visible { outline:2px solid var(--lime); outline-offset:2px; }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) { width:78px !important; min-width:78px !important; }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) > div:first-child { padding-left:.7rem; padding-right:.7rem; }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) .st-key-brand_home button { overflow:hidden; white-space:nowrap; font-size:0; padding:0; }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) .st-key-brand_home button::first-letter { font-size:18px; }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) [data-testid="stMarkdownContainer"] { overflow:hidden; white-space:nowrap; }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) [data-testid="stMarkdownContainer"] p { font-size:0; }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) [role="radiogroup"] label { justify-content:center; padding:0; }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) [role="radiogroup"] label > div:last-child { display:none; }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) [role="radiogroup"] label > div:first-child { margin:auto; }
section[data-testid="stSidebar"]:has(.sidebar-collapsed) [data-testid="stCaptionContainer"] { display:none; }
@media (max-width: 768px) {
  [data-testid="stSidebar"] { width: min(86vw, 320px) !important; min-width: min(86vw, 320px) !important; }
  section[data-testid="stSidebar"]:has(.sidebar-collapsed) { width:0 !important; min-width:0 !important; }
  section[data-testid="stSidebar"]:has(.sidebar-collapsed) > div:first-child { padding:0; overflow:hidden; }
  section[data-testid="stSidebar"]:has(.sidebar-collapsed) * { visibility:hidden; }
  .st-key-sidebar_toggle { position:fixed; top:12px; right:12px; z-index:100; }
}
@media (prefers-reduced-motion: reduce) {
  .st-key-sidebar_toggle button::before,
  .st-key-sidebar_toggle button::after,
  .st-key-sidebar_toggle button > div::before { transition:none; }
}
</style>
""", unsafe_allow_html=True)

render_composite_background()


def chart_layout(fig: go.Figure, height: int = 300) -> go.Figure:
    fig.update_layout(height=height, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="#1d2024", font_color="#b8bfbd",
                      margin=dict(l=12, r=12, t=22, b=12),
                      xaxis=dict(gridcolor="#30353a", zeroline=False),
                      yaxis=dict(gridcolor="#30353a", zeroline=False),
                      legend=dict(orientation="h", y=1.1, x=0))
    return fig


def metric(label: str, value: str, note: str = "") -> None:
    st.markdown(f'<div class="card"><div class="card-label">{label}</div>'
                f'<div class="card-value">{value}</div><div class="card-note">{note}</div></div>',
                unsafe_allow_html=True)


def run_config(material_name: str, vf: float, ref_c: float, op_c: float,
               angles: tuple[float, ...], thickness_mm: float, boundary: str):
    material = MATERIALS[material_name]
    return run_simulation(SimulationInput(
        material_name, vf, ref_c + 273.15, op_c + 273.15,
        LaminateInput(angles, thickness_mm / 1000),
        boundary_condition=boundary,
        # Keep the material provenance in the exported result.
        material_source=material.source,
    ))


def toggle_sidebar() -> None:
    st.session_state.sidebar_expanded = not st.session_state.sidebar_expanded


def complete_welcome() -> None:
    st.session_state.welcome_complete = True


if "runs" not in st.session_state:
    st.session_state.runs = []
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "sidebar_expanded" not in st.session_state:
    st.session_state.sidebar_expanded = True
if "welcome_complete" not in st.session_state:
    st.session_state.welcome_complete = False
if "_jump" in st.session_state:
    st.session_state.navigation = st.session_state.pop("_jump")

if not st.session_state.welcome_complete:
    st.markdown(
        '<main class="tc-welcome-shell"><section class="tc-welcome-form">'
        '<div class="tc-welcome-kicker">THERMOCOMPOSITE LAB / WORKSPACE SETUP</div>'
        '<div class="tc-welcome-title">Welcome to your materials workspace.</div>'
        '<p class="tc-welcome-copy">Set a lightweight workspace context before exploring '
        'thermal response, material systems and laminate behaviour. This is not an '
        'account or authentication step.</p>',
        unsafe_allow_html=True,
    )
    with st.form("workspace_welcome_form"):
        st.text_input("Workspace label", value="ThermoComposite Lab")
        st.text_input("Primary engineering focus", value="Thermal and laminate response")
        st.form_submit_button(
            "Enter workspace →",
            type="primary",
            on_click=complete_welcome,
        )
    st.markdown(
        '<div class="tc-welcome-meta">PRELIMINARY ENGINEERING ESTIMATES · '
        'Rudrajyoti Paul</div></section></main>',
        unsafe_allow_html=True,
    )
    st.stop()

with st.sidebar:
    sidebar_marker = "sidebar-expanded" if st.session_state.sidebar_expanded else "sidebar-collapsed"
    st.markdown(f'<div class="{sidebar_marker}" aria-hidden="true"></div>', unsafe_allow_html=True)
    toggle_label = "Collapse workspace sidebar" if st.session_state.sidebar_expanded else "Expand workspace sidebar"
    st.button(toggle_label, key="sidebar_toggle", help=toggle_label,
              use_container_width=False, on_click=toggle_sidebar)
    if st.button("∞  THERMO  /  COMPOSITE LAB", key="brand_home", help="Return to the dashboard", use_container_width=True):
        st.session_state.navigation = "Dashboard"
        st.rerun()
    st.markdown('<div class="card-label" style="padding:0 8px 8px">WORKSPACE</div>', unsafe_allow_html=True)
    page = st.radio("Navigation", [
        "Dashboard", "Material Explorer", "Material Builder", "Thermal Simulator",
        "Laminate Designer", "Simulation Comparison", "Results & Reports", "About & Sources",
    ], key="navigation", label_visibility="collapsed")
    st.divider()
    st.markdown('<div class="status"><span class="dot"></span> ENGINE ONLINE</div>', unsafe_allow_html=True)
    st.caption("Linear elastic • SI units • v0.1")


def page_header(kicker: str, title: str, description: str) -> None:
    st.markdown(f'<div class="eyebrow">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f'<p style="color:#929798;max-width:760px">{description}</p>', unsafe_allow_html=True)


def simulation_form(default_material: str = "Carbon fibre / epoxy", include_laminate: bool = True):
    col1, col2, col3 = st.columns(3)
    with col1:
        material_name = st.selectbox("Material system", list(MATERIALS),
                                     index=list(MATERIALS).index(default_material))
        vf = st.slider("Fibre / reinforcement volume fraction", 0.0, 0.8, 0.6, .01)
    with col2:
        ref_c = st.number_input("Reference temperature (°C)", value=20.0)
        op_c = st.number_input("Operating temperature (°C)", value=80.0)
    with col3:
        boundary = st.selectbox("Boundary condition", ["Free expansion", "Fully restrained (uniaxial estimate)"])
        st.caption("Temperature difference is calculated from the two temperatures.")
    angles_text, thickness = "0, 90, 90, 0", .125
    if include_laminate:
        a, b = st.columns([2, 1])
        with a:
            angles_text = st.text_input("Stacking sequence (°)", angles_text)
        with b:
            thickness = st.number_input("Ply thickness (mm)", min_value=.01, value=.125)
    return material_name, vf, ref_c, op_c, boundary, angles_text, thickness


if page == "Dashboard":
    st.markdown('<div class="hero"><div class="eyebrow">ENGINEERING WORKSPACE / 01</div><div class="hero-copy"><h1>Understand how materials respond.</h1><p>Explore temperature-driven behaviour, build laminate configurations, and compare transparent engineering estimates — all grounded in the same validated calculation engine.</p><div class="status"><span class="dot"></span> READY FOR A NEW SIMULATION</div></div></div>', unsafe_allow_html=True)
    result = st.session_state.last_result
    if result:
        p = result.effective_properties
        st.markdown('<div class="section-title">Current simulation</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        with cols[0]: metric("E1 / longitudinal", f"{p.e1_pa/1e9:.1f} GPa", "effective property")
        with cols[1]: metric("E2 / transverse", f"{p.e2_pa/1e9:.1f} GPa", "reciprocal estimate")
        with cols[2]: metric("Thermal strain", f"{result.thermal_strain_1:.2e}", f"ΔT {result.delta_temperature_k:.1f} K")
        with cols[3]:
            stress = (
                "Not applicable"
                if result.restrained_stress_1_pa is None
                else f"{result.restrained_stress_1_pa/1e6:.1f} MPa"
            )
            metric("Restrained stress", stress, result.inputs["boundary_condition"])
        x = np.linspace(0, result.delta_temperature_k, 25)
        fig = go.Figure(go.Scatter(x=x, y=p.alpha1_per_k*x, mode="lines", name="α₁ ΔT",
                                   line=dict(color="#d7ff3f", width=3)))
        fig.update_layout(title="Temperature response · directional strain", xaxis_title="Temperature change (K)", yaxis_title="Strain")
        st.plotly_chart(chart_layout(fig), use_container_width=True)
    else:
        st.markdown('<div class="empty"><div class="eyebrow">NO RUNS YET</div><h3>Start with a thermal simulation</h3><p>Use the simulator to create the first real result for this workspace. Summary cards and response charts will appear here.</p></div>', unsafe_allow_html=True)
        if st.button("Open Thermal Simulator", type="primary"):
            st.session_state._jump = "Thermal Simulator"
            st.rerun()
    st.markdown('<div class="section-title">Quick actions</div>', unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        st.markdown('<div class="card"><div class="eyebrow">01 / EXPLORE</div><h3>Material catalogue</h3><p style="color:#929798">Search supported systems, provenance and model capabilities.</p></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card"><div class="eyebrow">02 / DESIGN</div><h3>Laminate designer</h3><p style="color:#929798">Define a stacking sequence and inspect A/B/D response.</p></div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="card"><div class="eyebrow">03 / COMPARE</div><h3>Compare systems</h3><p style="color:#929798">Run the same thermal case across supported materials.</p></div>', unsafe_allow_html=True)

elif page == "Material Explorer":
    page_header("CATALOGUE / 02", "Material intelligence, without the black box.",
                "Browse the versioned reference catalogue. Estimates are labeled, traceable, and never presented as certified allowables.")
    search = st.text_input("Search materials", placeholder="Try carbon, glass, epoxy, metal…")
    families = ["All families"] + sorted({m.family for m in MATERIALS.values()})
    family = st.selectbox("Filter by family", families)
    rows = []
    for name, m in MATERIALS.items():
        if search.lower() not in name.lower() and search.lower() not in m.reinforcement.lower():
            continue
        if family != "All families" and m.family != family:
            continue
        rows.append({"Material system": name, "Family": m.family, "Reinforcement": m.reinforcement,
                     "Matrix": m.matrix, "Form": m.form, "Models": ", ".join(m.supported_models),
                     "Data status": m.status, "Valid range": f"{m.valid_temperature_range_k[0]-273.15:.0f} to {m.valid_temperature_range_k[1]-273.15:.0f} °C"})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.markdown('<div class="warning">Reference properties are engineering estimates for educational exploration. Verify supplier data, processing route, test condition and temperature dependence before using any result for design.</div>', unsafe_allow_html=True)

elif page == "Material Builder":
    page_header("CONFIGURATION / 03", "Build a material configuration.",
                "Choose a supported system, inspect its assumptions, and validate the inputs before the model is allowed to run.")
    name = st.selectbox("Base material", list(MATERIALS))
    m = MATERIALS[name]
    a, b, c = st.columns(3)
    with a: vf = st.slider("Volume fraction", 0.0, .8, .6, .01)
    with b: st.text_input("Reinforcement", m.reinforcement, disabled=True)
    with c: st.text_input("Matrix", m.matrix, disabled=True)
    st.markdown(f'<div class="card"><span class="tag">{m.family}</span><span class="tag">{m.form}</span><span class="tag">{m.status}</span><span class="tag">{" • ".join(m.supported_models)}</span><h3>{name}</h3><p style="color:#929798">{m.source}</p><p class="card-label">Temperature range</p><p>{m.valid_temperature_range_k[0]-273.15:.0f} °C — {m.valid_temperature_range_k[1]-273.15:.0f} °C</p></div>', unsafe_allow_html=True)
    try:
        m.validate_fraction(vf)
        supported = ", ".join(m.supported_models)
        st.success(f"Configuration is valid for the supported models: {supported}.")
    except ValidationError as exc:
        st.error(str(exc))

elif page in ("Thermal Simulator", "Laminate Designer"):
    page_header("SIMULATION / 04", "Thermal response" if page == "Thermal Simulator" else "Laminate designer",
                "Set the physical conditions, run the model, and inspect outputs with their units and assumptions.")
    material_name, vf, ref_c, op_c, boundary, angles_text, thickness = simulation_form(include_laminate=True)
    if st.button("Run validated simulation", type="primary"):
        try:
            angles = tuple(float(value.strip()) for value in angles_text.split(",") if value.strip())
            result = run_config(material_name, vf, ref_c, op_c, angles, thickness, boundary)
            st.session_state.last_result = result
            st.session_state.runs.append({"time": datetime.now().strftime("%H:%M"), "material": material_name,
                                          "delta": result.delta_temperature_k, "result": result})
            st.success("Simulation completed. Outputs below are from the scientific engine.")
        except (ValidationError, NumericalError, ValueError) as exc:
            st.error(str(exc))
    result = st.session_state.last_result
    if result:
        p = result.effective_properties
        st.markdown('<div class="section-title">Results overview</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        with cols[0]: metric("Temperature change", f"{result.delta_temperature_k:.1f} K")
        with cols[1]: metric("α₁", f"{p.alpha1_per_k:.2e} /K")
        with cols[2]: metric("Thermal strain", f"{result.thermal_strain_1:.2e}")
        with cols[3]:
            stress = (
                "Not applicable"
                if result.restrained_stress_1_pa is None
                else f"{result.restrained_stress_1_pa/1e6:.1f} MPa"
            )
            metric("σ₁ restrained", stress, result.inputs["boundary_condition"])
        st.markdown('<div class="section-title">Laminate response</div>', unsafe_allow_html=True)
        if result.laminate:
            c1, c2 = st.columns(2)
            with c1: st.dataframe(pd.DataFrame(result.laminate.midplane_strain.reshape(1, -1), columns=["εx", "εy", "γxy"]), use_container_width=True, hide_index=True)
            with c2: st.dataframe(pd.DataFrame(result.laminate.curvature.reshape(1, -1), columns=["κx", "κy", "κxy"]), use_container_width=True, hide_index=True)
            stress_rows = [{"Ply": item["ply"], "Angle": item["angle_deg"], "Surface": item["surface"],
                            "σx (MPa)": item["stress_pa"][0]/1e6, "σy (MPa)": item["stress_pa"][1]/1e6}
                           for item in result.laminate.ply_stresses]
            st.dataframe(pd.DataFrame(stress_rows), use_container_width=True, hide_index=True)
        st.markdown('<div class="warning">Assumptions: uniform temperature through thickness, small strain, linear elasticity, perfect bonding and plane stress. This is CLT, not finite-element analysis.</div>', unsafe_allow_html=True)
        st.download_button("Download simulation JSON", result_to_json(result), "thermocomposite-report.json", "application/json")

elif page == "Simulation Comparison":
    page_header("COMPARISON / 05", "Compare material response.",
                "A consistent case is evaluated through the same model for each selected system. Rankings are descriptive, not safety claims.")
    selected = st.multiselect("Material systems", list(MATERIALS), default=list(MATERIALS)[:3])
    vf = st.slider("Shared volume fraction", 0.0, .8, .6, .01)
    dt = st.slider("Temperature change (K)", -100, 200, 60)
    if selected:
        rows = []
        for name in selected:
            material = MATERIALS[name]
            result = run_simulation(SimulationInput(
                name, vf, 293.15, 293.15 + dt, laminate=None,
                boundary_condition="Fully restrained (uniaxial estimate)",
                material_source=material.source,
            ))
            rows.append({"Material": name, "E1 (GPa)": result.effective_properties.e1_pa/1e9,
                         "α1 (µε/K)": result.effective_properties.alpha1_per_k*1e6,
                         "Strain (µε)": result.thermal_strain_1*1e6,
                         "Restrained stress (MPa)": result.restrained_stress_1_pa/1e6})
        frame = pd.DataFrame(rows)
        st.dataframe(frame, use_container_width=True, hide_index=True)
        fig = go.Figure()
        for row in rows:
            fig.add_trace(go.Bar(name=row["Material"], x=["Thermal strain (µε)", "Restrained stress (MPa)"],
                                 y=[row["Strain (µε)"], abs(row["Restrained stress (MPa)"])]))
        fig.update_layout(barmode="group", title="Response comparison · absolute magnitude")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

elif page == "Results & Reports":
    page_header("RESULTS / 06", "Your simulation record.",
                "Results remain tied to the actual run in this browser session. Export them for reproducibility.")
    result = st.session_state.last_result
    if not result:
        st.markdown('<div class="empty">No simulation results yet. Run a case from the Thermal Simulator.</div>', unsafe_allow_html=True)
    else:
        st.json(result_to_json(result))
        st.download_button("Download JSON report", result_to_json(result), "thermocomposite-report.json", "application/json")
        st.markdown("### Model warnings")
        for warning in result.warnings:
            st.warning(warning)

elif page == "About & Sources":
    page_header("SYSTEM / 07", "Transparent by design.",
                "ThermoComposite Lab separates the interface from a small, testable scientific engine.")
    st.markdown('<div class="card"><div class="eyebrow">CAPABILITIES</div><h3>Available now</h3><p>Effective longitudinal and transverse properties, directional thermal strain, fully restrained uniaxial stress estimates, and plane-stress Classical Laminate Theory with A/B/D matrices, thermal resultants and ply stress recovery.</p><div class="eyebrow">NOT IMPLEMENTED</div><p>Transient heat transfer, spatial gradients, nonlinear response, delamination, progressive failure, impact damage, creep, fatigue and experimental validation.</p></div>', unsafe_allow_html=True)
    st.markdown("### Material data provenance")
    st.write("Catalogue entries are explicitly labeled engineering reference estimates. Their source field directs users to verify supplier or publication data; no entry is presented as a certified allowable.")
    st.markdown("### Reproducibility")
    st.code("pytest\nstreamlit run app.py", language="bash")

st.markdown(
    '<div style="border-top:1px solid #30353a;margin-top:42px;padding:18px 0 8px;'
    'color:#929798;font:11px \'DM Mono\',monospace;text-align:center">'
    'THERMOCOMPOSITE LAB · PRELIMINARY ENGINEERING ESTIMATES<br>'
    '<span style="color:#d7ff3f">Rudrajyoti Paul</span></div>',
    unsafe_allow_html=True,
)
