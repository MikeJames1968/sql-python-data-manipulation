# Data Cleaning Pipeline — Canonical Technical Brief

## Overview
`clean_pipeline` is a configurable, modular data‑cleaning engine designed for reproducible preprocessing of tabular datasets. It validates a user‑supplied configuration dictionary, executes only the cleaning steps requested, captures printed output from each function, and returns both the cleaned DataFrame and a structured summary report.

Supported cleaning modules:

- duplicates  
- string  
- dates  
- missing  
- numeric  
- outliers  
- categories  
- scaling  

Each module is optional and activated only when its tag appears in the config.

---

## 1. Configuration Validation

### 1.1 Required Conditions
- `config` must be a non‑empty dictionary  
- `df` must be a `pandas.DataFrame`  
- All top‑level keys must match known cleaning modules  
- Each module must contain a dictionary of parameters  
- Parameter names must match the module’s schema  
- Parameter values must be valid according to the module’s allowed types

### 1.2 Column‑related Validation
For parameters such as `col_list`, `col_dict`, and mapping dictionaries:

- Column names must exist in the DataFrame  
- Column lists must contain at least one column of the required dtype  
- Mapping dictionaries must map strings → strings  
- Missing‑value dictionaries must contain valid replacement tokens

### 1.3 Error Handling
Invalid configuration elements raise descriptive exceptions:

- `ValueError` for invalid tags or parameter values  
- `TypeError` for incorrect parameter types  

---

## 2. Execution Workflow
After validation, the pipeline executes cleaning functions in the following order:

1. duplicates  
2. string  
3. dates  
4. missing  
5. numeric  
6. outliers  
7. categories  
8. scaling  

Each step:

- Receives only the parameters defined in the config  
- Operates on a working copy of the DataFrame  
- Writes printed output into a shared buffer  
- Optionally returns a summary dictionary  
- Is skipped entirely if not present in the config

---

## 3. Why This Pipeline Exists

Modern data projects rarely fail because of modelling — they fail because of inconsistent, messy, or poorly‑documented preprocessing.  
`clean_pipeline` solves that problem by providing:

- A **single, reproducible entry point** for all cleaning operations  
- A **strict configuration validator** that prevents silent errors  
- A **modular architecture** where each cleaning step is optional  
- A **complete audit trail** of every transformation applied  
- A **cleaned DataFrame + structured summary** for downstream use  

This makes the pipeline suitable for ETL workflows, ML preprocessing, analytics, and any environment where data quality and reproducibility matter.

---

## 4. Design Principles

### 4.1 Explicit Over Implicit
Every cleaning step must be explicitly requested in the config.  
If a module is not present, it is not run.  
This prevents accidental transformations and ensures full transparency.

### 4.2 Fail Fast, Fail Loud
The validator rejects:

- invalid module names  
- invalid parameter names  
- invalid parameter values  
- incorrect types  
- missing or mismatched columns  
- incorrect mapping dictionaries  
- malformed missing‑value specifications  

This eliminates silent corruption — a common failure mode in ad‑hoc cleaning scripts.

### 4.3 Modular and Extensible
Each cleaning function is independent.  
Adding a new module requires only:

1. Extending the validator schema  
2. Adding a call block in the pipeline  
3. Returning a summary (optional)

No changes to the core workflow are required.

### 4.4 Full Transparency
All printed output from cleaning functions is captured and stored.  
Every module can return a structured summary.  
The final report shows:

- what ran  
- what didn’t  
- what parameters were used  
- what each module did  
- the final DataFrame shape  

This makes the pipeline ideal for debugging, logging, and reproducible research.

---

## 5. Cleaning Modules (High‑Level Overview)

### 5.1 Duplicates
Removes fully duplicated rows based on a user‑specified column list.

### 5.2 String Cleaning
Applies transformations (`lower`, `upper`, `strip`, `title`) to all string‑typed columns.

### 5.3 Date Cleaning
Normalizes datetime columns using strategies such as `median` or `mode`.

### 5.4 Missing Value Handling
Supports three mechanisms:

- `col_dict` — enforce column types  
- `strat_dict` — fill missing values by type  
- `val_dict` — replace specific tokens  

Reports missing counts per column and total missing values.

### 5.5 Numeric Cleaning
Handles numeric coercion and optional outlier clipping.

### 5.6 Outlier Removal
Supports `iqr` and `zscore` methods.  
Removes rows containing outliers in specified numeric columns.

### 5.7 Category Normalization
Applies casing strategies and optional mapping dictionaries.  
Reports pre‑ and post‑normalization unique values.

### 5.8 Scaling
Supports `minmax`, `zscore`, and `robust` scaling.  
Reports min/max or median/IQR depending on strategy.

---

## 6. Summary Output Structure

The pipeline returns:

### 6.1 Cleaned DataFrame
A fully processed DataFrame reflecting all requested cleaning steps.

### 6.2 Summary Dictionary
A structured report containing:

- **steps run**  
- **steps skipped**  
- **parameters passed**  
- **cleaning function outputs**  
- **cleaned dataframe shape**  

Example:

```python
{
  'steps run': dict_keys([...]),
  'steps skipped': {...},
  'parameters passed': {...},
  'cleaning function outputs': {...},
  'cleaned dataframe shape': (rows, cols)
}
```



## `Test harness for clean_pipeline`

The test harness is a simple set of test data and executions of the code the entire data cleaning toolkit.
It tests every module in the toolkit and is split into 3 sections:

1. Testing the validation in `clean_pipeline` of the `clean_categories 'map'` parameter, which is complex
2. Testing the validation in `clean_pipeline` of other config dictionary parameters
3. A test of the processing in `clean_pipeline`, calling all modules. This uses a sample test set and is far from exhaustive

It contains a function to format the output of the `clean_pipeline` summary dictionary, for easy reading



## `clean_date`

### Purpose
Convert a date column into a consistent `datetime64` format and replace missing or invalid dates using a configurable strategy.

### Description
`clean_date` takes a Pandas Series containing date values and performs two operations:

1. **Type coercion**  
   All values are converted to `datetime` using `pd.to_datetime` with:
   - `format='mixed'` to support heterogeneous date formats  
   - `errors='coerce'` to convert invalid or impossible dates into `NaT`

2. **Missing-value handling**  
   Any `NaT` values are replaced according to the `missing` parameter:
   - `"mode"` (default): fills with the most common date in the column  
   - `"median"`: fills with the median date value

### Signature
```python
clean_date(date_col, strategy)
```



## `clean_string`

### Purpose
Trim and normalise a string column, standardising whitespace and optionally forcing a specific case format.

### Description
`clean_string` takes a Pandas Series containing string values and performs the following operations:

1. **Whitespace trimming**  
   Removes leading and trailing whitespace using `.str.strip()`.

2. **Whitespace normalisation**  
   Collapses multiple internal whitespace characters (spaces, tabs, newlines) into a single space using a regular expression.

3. **Missing-value normalisation**  
   Converts empty strings (`""`) and `None` values into `NaN` for consistent downstream handling.

4. **Case normalisation**  
   Applies an optional case strategy:
   - `"strip"` (default): no case change  
   - `"lower"`: convert to lowercase  
   - `"upper"`: convert to uppercase  
   - `"title"`: capitalise the first character of the string

### Signature
```python
clean_string(str_col, strategy)
```



## `clean_duplicates`

### Purpose
Identify and remove duplicate rows from a dataframe, using either full‑row comparison or a user‑specified subset of columns.  
Provides printed diagnostic output that can be captured by the pipeline engine and included in the final summary.

### Description
`clean_duplicates` examines a dataframe for duplicate rows and performs three operations:

1. **String normalisation**  
   All string columns are trimmed and normalised using `clean_string` to prevent false duplicates caused by inconsistent whitespace or casing.

2. **Full duplicate detection**  
   Detects rows that are identical across all columns.  
   Prints:
   - number of full duplicates  
   - first 10 duplicate rows  
   Removes all full duplicates, keeping the first occurrence.

3. **Partial duplicate detection**  
   If a list of column names is provided, detects rows that are identical across that subset.  
   Prints:
   - number of partial duplicates  
   - first 10 duplicate rows  
   Removes all partial duplicates, keeping the first occurrence.

### Signature
```python
clean_duplicates(df, col_list)
```



## `clean_outliers`

### Purpose
Identify and remove outlier rows from a dataframe using either the iqr method or z‑score thresholding.  
Supports multi‑column outlier detection and ranks outliers by severity.  
Printed diagnostic output is intended to be captured by the pipeline engine.

### Description
`clean_outliers` examines numeric columns in a dataframe and performs the following operations:

1. **Column selection**  
   - If `col_list` is provided, only those columns are used.  
   - Otherwise, all numeric columns are selected automatically.

2. **Outlier detection**  
   Two methods are supported:
   - `"iqr"`: rows with values outside `q1 - 1.5 × iqr` or `q3 + 1.5 × iqr`  
   - `"z"`: rows where any numeric column has `|z| > 3`

   For multi‑column detection, the function computes a per‑row severity score:
   - `"max_dist"` for iqr  
   - `"max_z"` for Z‑scores  
   Outliers are ranked by this score.

3. **Reporting**  
   The function prints:
   - the outlier rows  
   - the ranking metric  
   - the total number of rows removed  

   This output is designed to be captured by the pipeline engine.

4. **Removal**  
   Outlier rows are removed using `df.drop(index=...)`.

### Signature
```python
clean_outliers(df, col_list, method)
```



## `clean_num`

### Purpose
Coerce specified numeric columns to a consistent numeric type, handle missing numeric values according to a chosen strategy, and optionally remove outliers using a standard‑deviation threshold.  
This function was written for the original mini‑project and intentionally avoids strong parameter validation, as validation is handled by the pipeline engine.

---

### Description
`clean_num` processes a list of numeric columns in a dataframe and performs three operations:

1. **Numeric coercion**  
   Each column in `col_list` is converted to numeric using `pd.to_numeric(errors='coerce')`.  
   Any non‑numeric values become `NaN`.

2. **Missing‑value handling**  
   Controlled by the `strategy` parameter:
   - **`"zero"`** — replace `None` and `NaN` with `0`  
   - **`"mean"`** — replace `None` and `NaN` with the column mean  
   - **`"nan"`** — convert `None` to `NaN` and leave existing `NaN` unchanged  

   This behaviour matches the original brief and does not attempt to validate the strategy name.

3. **Outlier removal**  
   Controlled by the `outlier` parameter:
   - **`-1`** — skip outlier removal  
   - **`1–6`** — remove rows where values fall outside  
     `mean ± outlier × std`  
   - Values outside this range default to `3` (three standard deviations)

   Outlier removal is applied using a **combined mask**, ensuring all thresholds are computed on the original data and applied once.  
   This avoids cascading distortions that occur when filtering column‑by‑column.

---

### Signature
```python
clean_num(df, col_list, strategy, outlier)
```



## `clean_missing`

### Purpose
Coerce dataframe columns to declared types, normalise legacy missing-value tokens, and apply type‑specific replacement strategies.  
Supports boolean, numeric, string, and datetime columns, with optional schema validation and strategy control.

---

### Description
`clean_missing` performs missing‑value cleaning using an explicit or inferred column‑type schema.  
It operates on a subset of columns (`col_dict`) or all columns when no schema is provided.

The function performs five main operations:

1. **Column type determination**  
   Builds a `col_type` dictionary using Pandas dtype checkers.  
   If `col_dict` is provided, validates that declared types match existing dtypes (except `object`).  
   If no type is declared for an `object` column, assigns the type specified in `strategy['object']`.

2. **Missing‑token normalisation**  
   Replaces legacy null‑like tokens (e.g., `"N/A"`, `""`, `-999`, sentinel dates) with `NaN`/`NaT` based on column type.

3. **Type coercion**  
   Converts each column to its intended type using best‑practice Pandas methods:
   - **boolean** — explicit token mapping → nullable boolean dtype  
   - **number** — `pd.to_numeric(errors='coerce')`  
   - **date** — `pd.to_datetime(errors='coerce')`  
   - **string** — Pandas `string` dtype

4. **Strategy‑driven missing‑value replacement**  
   Applies replacement rules based on the `strat_dict` dictionary:
   - `"none"` — leave column unchanged  
   - `"drop"` — drop rows with missing values in the column  
   - `"mean"`, `"median"`, `"mode"` — numeric aggregation  
   - `"zero"` — fill with zero  
   - `"today"` — fill with current date  
   - any other literal value — used directly

5. **Summary generation**  
   Produces a dictionary reporting:
   - enforced column types  
   - missing‑value counts per column  
   - total missing values  
   - strategy used

---

### Signature
```python
clean_missing(df, col_dict, strat_dict, val_dict)
```



## `clean_categories`

### Purpose
Normalize categorical or string-based columns by standardizing whitespace, capitalization, and known variant values.  
Supports optional column scoping, optional custom normalization maps, and returns both a cleaned dataframe and a detailed summary of normalization activity.

---

### Description
`clean_categories` processes text or category columns in a dataframe and applies three main operations:

1. **String normalization**  
   Each column in scope is passed through `clean_string`, which:
   - collapses whitespace  
   - trims leading/trailing spaces  
   - applies a capitalization strategy (`"lower"`, `"upper"`, `"title"`, etc.)

2. **Category normalization using a mapping dictionary**  
   A normalization map is used to convert variant forms of categories into canonical values.  
   - Map keys must be **lowercase**, as normalization is applied after converting values to lowercase.

3. **Summary reporting**  
   For each processed column, the function reports:
   - unique values before normalization  
   - unique values after normalization  
   - counts of normalized values  
   - categories that were not mapped  
   - the capitalization strategy  
   - the mapping dictionary used  

The function returns a cleaned dataframe containing the processed columns, plus a full summary dictionary.

---

### Signature
```python
clean_categories(df, col_list, strategy, map)
```



## `scale_numeric`

### Purpose
Apply numeric scaling transformations to selected columns in a dataframe using a configurable strategy.  
Supports z‑score, min‑max, and robust scaling, optional column scoping, and returns both a scaled dataframe and a summary of per‑column statistics.

---

### Description
`scale_numeric` standardizes numeric columns according to a chosen scaling strategy.  
It performs four main operations:

1. **Column scoping**  
   If `col_list` is omitted, all numeric columns are selected.  
   Otherwise, only the specified columns are processed.

2. **Missing and infinite value handling**  
   Infinite values (`np.inf`, `-np.inf`) are converted to `NaN` before scaling.

3. **Scaling transformation**  
   Controlled by the `strategy` parameter:
   - **`"zscore"`**  
     

\[
     x' = \frac{x - \mu}{\sigma}
     \]

  
     Uses column mean and standard deviation.
   - **`"minmax"`**  
     

\[
     x' = \frac{x - \min}{\max - \min}
     \]

  
     Uses column minimum and maximum.
   - **`"robust"`**  
     

\[
     x' = \frac{x - \text{median}}{\text{IQR}}
     \]

  
     Uses median and interquartile range (IQR = Q3 − Q1).

   If the denominator (standard deviation, range, or IQR) is zero, the column is not scaled and a message is recorded in the summary.

4. **Summary reporting**  
   For each column, the function records:
   - the statistics used for scaling  
   - or an explanatory message if scaling was not possible  
   - the overall strategy  
   - the list of processed columns  

The function returns a scaled dataframe containing only the processed columns, plus a summary dictionary.

---

### Signature
```python
scale_numeric(df, col_list, strategy)