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

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run the verification suite with `pytest`.

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
