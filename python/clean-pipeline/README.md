# Data Cleaning Toolkit — Modular, Validated Preprocessing Engine

## Overview
This repository contains a fully modular, configuration‑driven **data cleaning pipeline** developed as part of my structured Python/Pandas retraining. The project was designed, set, and evaluated by **Microsoft Copilot**, and represents a deliberate progression from simple function design to a complete, validated, reproducible preprocessing engine.

The toolkit includes:

- A strict configuration validator  
- Eight independent cleaning modules  
- A unified pipeline (`clean_pipeline`)  
- A full test harness  
- Structured summary reporting  
- Comprehensive documentation  

It is intended as a portfolio‑ready demonstration of real engineering discipline in data preprocessing.

---

## Training Context
This project sits at a key point in my technical retraining. Earlier exercises focused on individual functions and basic Pandas operations; this toolkit was the first time I had to:

- design a multi‑module architecture  
- enforce strict validation rules  
- coordinate multiple cleaning functions  
- capture and report diagnostic output  
- build a reproducible test harness  

The complexity increased intentionally as the project progressed. Later modules — especially `clean_missing`, `clean_categories`, and `scale_numeric` — required significantly deeper reasoning, more defensive coding, and more careful handling of edge cases.

This pipeline marks the point where my training shifted from “learning Python” to “engineering with Python”.

---

## Exceeding the Brief
Although each task had a defined scope, I frequently extended the implementation when I felt it was worth exploring. Examples include:

- more detailed validation logic  
- richer diagnostic output  
- more robust handling of mixed types  
- clearer summary formatting  
- stricter consistency checks  

These additions weren’t required, but they helped me understand *why* certain patterns are considered best practice, not just *how* to implement them.

---

## What This Project Taught Me
This toolkit taught me as much about **data‑cleaning best practice** as it did about Python:

- why validation must be strict  
- why silent failures are dangerous  
- how to design modular cleaning functions  
- how to structure reproducible preprocessing  
- how to capture and report transformations cleanly  
- how to build meaningful tests that demonstrate correctness  

It reinforced engineering habits: clarity, consistency, defensive coding, and transparency.

---

## Pipeline Architecture
The pipeline supports eight independent cleaning modules:

- **duplicates** — remove full or partial duplicates  
- **string** — whitespace and case normalization  
- **dates** — datetime coercion and missing‑value strategies  
- **missing** — type enforcement and missing‑value replacement  
- **numeric** — numeric coercion, missing handling, optional outlier clipping  
- **outliers** — IQR or z‑score outlier removal  
- **categories** — category normalization and mapping  
- **scaling** — min‑max, z‑score, or robust scaling  

Each module is optional and activated only when its tag appears in the configuration dictionary.

Execution order is fixed and documented for reproducibility.

---

## Configuration Validation
The validator enforces:

- correct module names  
- correct parameter names  
- correct parameter types  
- correct column lists  
- correct mapping dictionaries  
- correct missing‑value strategies  
- correct numeric and category scopes  

Invalid configurations fail fast with descriptive errors.  
This prevents silent corruption — a common failure mode in ad‑hoc cleaning scripts.

---

## Test Harness
The test harness validates:

1. **Complex category‑mapping logic**  
2. **General configuration validation**  
3. **Stress‑testing individual parameters**  
4. **Full end‑to‑end pipeline processing**

All tests are included, with one active at a time for clarity.  
Outputs are formatted using neutral `text` blocks to preserve tabulation and readability.

---

## Repository Structure
```text
clean-pipeline/
│
├── docs/
│   ├── project_brief.md
│   ├── pipeline_code.md
│   └── test_outputs.md
│
├── notebooks/
│   ├── clean_pipeline_development.ipynb
│   └── test_harness.ipynb
│
└── src/
    └── clean_pipeline.py
```

---

## Summary
This project demonstrates:

- real‑world data‑cleaning skills  
- modular design  
- strong validation discipline  
- clear documentation  
- reproducible testing  
- a genuine progression in technical ability  

It is a representative example of the engineering approach I bring to data preprocessing, ETL, and analytics‑focused Python work.
