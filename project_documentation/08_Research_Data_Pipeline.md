# 08 — Research Data Pipeline

The relational model separates sources, materials, test types, datasets, specimens, observations, metrics, extraction logs, tags, files, and archive records. The active research endpoint queries records by test and optional material/geometry/conditions with pagination/sorting. `backend/composite_testing/ingestion.py` parses CSV, XLSX, JSON, BibTeX, PDF, ZIP, Markdown, TXT, HTML, URL, and DOCX sources, with conservative numeric-column selection and safe/bounded archive handling. It is a parser utility, not a public upload/relational ingestion workflow; arbitrary PDF figures are not automatically digitized into validated curves.

## Snapshot inventory

| Record type | Count |
|---|---:|
| Research bibliography sources | 34 |
| Imported archive records | 6 |
| Relational datasets | 0 |
| Observation rows | 0 |
| Usable CF/epoxy experimental curves | 0 |
| Searchable research procedure IDs | 18 |
| Destructive manual calculation families | 9 |

Thus eligible graphable CF/epoxy datasets are zero for each research procedure. Archive records or empty CSV templates are not datasets. This says nothing about the total scientific literature.

Each dataset should be test-specific and preserve material system, geometry, orientation, conditioning, temperature, source and units. Keep raw observations; label derived quantities with formula and inputs. Never borrow flexural data for compression because the material matches. Synthetic fixtures stay explicitly synthetic. If no suitable data exist, report absence.
