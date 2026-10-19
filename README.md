# ThermoComposite Lab

ThermoComposite Lab is a Streamlit application for preliminary, transparent
thermal and Classical Laminate Theory (CLT) calculations for fibre-reinforced
composites. It is an educational and early-design tool, not a finite-element
solver or a certification method.

The interface is organized as a dark analytics workspace with Dashboard,
Material Explorer, Material Builder, Thermal Simulator, Laminate Designer,
Simulation Comparison, Results & Reports, and About & Sources views. Cards and
charts are populated from actual simulation results; before the first run the
dashboard shows an explicit empty state.

## Run locally

### React + FastAPI workspace

Start the API and frontend in separate terminals from the project root:

```bash
# Terminal 1
.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8010

# Terminal 2
cd frontend
npm ci
npm run dev -- --host 127.0.0.1 --port 5173
```

Open `http://127.0.0.1:5173`. The frontend expects the API at
`http://127.0.0.1:8010/api/v1` by default. Confirm the API is running with:

```bash
curl http://127.0.0.1:8010/api/v1/health
```

### Legacy Streamlit workspace

```bash
source .venv/bin/activate
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

Run the verification suite with `.venv/bin/pytest -q tests backend/tests`.

## Supported model

The application currently includes:

- carbon/epoxy, glass/epoxy, aramid/epoxy, basalt/epoxy, carbon/PEEK and
  aluminium/silicon-carbide reference systems;
- rule-of-mixtures longitudinal modulus and a reciprocal transverse modulus;
- directional thermal strain and fully restrained uniaxial thermal stress;
- plane-stress Classical Laminate Theory with transformed ply stiffness,
  laminate A/B/D matrices, thermal resultants, mid-plane response, and ply
  stress recovery;
- JSON report downloads with units, model metadata, provenance, and author attribution.

Reference properties are engineering estimates intended for educational
exploration. They are not a material allowables database. Inputs outside the
declared ranges are rejected rather than silently extrapolated.

## Limitations

Transient heat transfer, spatial temperature fields, nonlinear constitutive
behaviour, delamination, progressive failure, impact damage, creep, fatigue,
moisture, and experimental validation are not implemented. A passing
calculation is not a universal safety claim.

## Deployment

The repository is compatible with Streamlit Community Cloud: select `app.py`
as the entry point and `requirements.txt` as the dependency manifest. No
credentials or external data files are required.
