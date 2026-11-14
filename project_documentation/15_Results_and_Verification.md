# 15 — Results and Verification

Source paths exist for thermal simulation, CLT, nine manual test calculations, seeded synthetic fixtures, quantity planning, research querying, and thermal curve/export functionality. Audit tests: 83 backend passes with one file-writing test excluded, and five frontend passes.

Research snapshot: 34 source records, six archive records, zero datasets, zero observations. Thus there is no experimental response curve to graph for Carbon Fibre / Epoxy. Bibliography and archive records are not datasets.

Software tests demonstrate asserted code behavior only. They do not show agreement with laboratory measurements, predictive accuracy, certified properties, standards compliance, or production performance. Thermal export is present in source/UI but the file-writing test was not executed. Audit date 2026-11-14; tests used an isolated temporary DB. No application source/config/database was changed.
