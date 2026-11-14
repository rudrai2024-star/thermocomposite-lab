# ThermoComposite Lab — Master Project Dossier

**Audit snapshot:** 14 November 2026. **Scope:** source-based documentation; application implementation was not modified.

## Executive summary

ThermoComposite Lab is a local-first engineering application for exploratory thermal response estimates, classical laminate calculations, basic quantity planning, and composite testing/research workflows. The primary path is a React/TypeScript frontend with FastAPI. A separate legacy Streamlit interface remains in `app.py`.

At this snapshot the research database has 34 source records and six archive records, but zero datasets and zero observations. There are therefore no graphable experimental response curves, including for Carbon Fibre / Epoxy. Manual calculations require user supplied measurements. Synthetic curves are deterministic software fixtures, not empirical evidence.

## Dossier navigation

1. [Project overview](01_Project_Overview.md) · [Technology stack](02_Complete_Technology_Stack.md) · [Architecture](03_System_Architecture.md) · [Modules and status](04_Module_By_Module_Documentation.md)
2. [Scientific equations](05_Scientific_Methodology_and_Equations.md) · [CLT](06_Classical_Laminate_Theory.md) · [Testing lab](07_Composite_Testing_Laboratory.md) · [Research pipeline](08_Research_Data_Pipeline.md)
3. [Database](09_Database_Schema_and_ERD.md) · [API](10_API_Documentation.md) · [Algorithms](11_Algorithms_and_Data_Processing.md) · [Security](12_Security_and_Reliability_Audit.md)
4. [QA](13_Testing_and_Quality_Assurance.md) · [Deployment](14_Deployment_and_Configuration.md) · [Results](15_Results_and_Verification.md) · [Limitations](16_Limitations_and_Research_Gaps.md)
5. [Future scope](17_Future_Scope.md) · [History](18_Project_Development_History.md) · [Evidence index](19_Evidence_and_Source_Code_References.md)

## Feature summary

| Feature | Status | Verified boundary |
|---|---|---|
| Thermal simulation | Implemented and verified | Analytical calculation and persisted runs; simplified assumptions |
| CLT laminate | Implemented and verified | Linear elastic CLT core and numerical tests |
| Thermal curves | Implemented; export test not run | API/UI paths exist; export writes files |
| Materials | Partial | Six core reference records; active endpoint scope is narrower |
| Material builder | Partial | Configuration UI, no material authoring persistence |
| Quantity planner | Implemented and verified | Unit conversion, volume/mass estimate, usage transactions |
| Research search | Partial | Relational query exists; zero experimental observations |
| Manual testing | Implemented and verified | Nine destructive calculation families from user values |
| Synthetic testing | Implemented and verified | Seeded software fixtures; not experimental results |
| NDT | Partial | Eight procedure categories searchable; no NDT engine or dataset |
| Comparison/reports | Partial | Stored-run listing; React report export not wired |
| Login/register | UI only | Placeholder; no account/auth routes |
| Streamlit | Deprecated/secondary | Legacy interface, separate from primary React build |

## Academic report and presentation guidance

Describe an engineering software prototype, not a validated materials database or substitute for physical testing. Clearly distinguish calculated estimates, user-entered measurements, synthetic fixtures, and published observations. The fourth category currently has zero numerical observations. The audited software checks were 83 backend passes and five frontend passes; these are not model accuracy or experimental validation metrics.

Suggested 18-slide presentation: title; motivation; problem; objectives/scope; workflows; architecture; stack; persistence; material model; thermal equations; CLT; testing modes; research provenance; feature status; software checks; limitations; roadmap; conclusion/demo.

Do not claim populated experimental data, validated prediction accuracy, full NDT processing, online accounts, or active API support for every core material. Do not call synthetic curves measured behavior. The thermal export test was not exercised in this audit because it writes persistent artifacts.
