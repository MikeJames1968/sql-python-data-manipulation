## `Test Harness Outputs`

This cell contains outputs from the test harness above, in the order executed
The test dataframes are printed once each, as they do not change with different config dictionaries

### `Config Dictionary Map Validation Tests`

```python
print(df_config_map_test)
```
```text
   status   gender    region  
0     open        m        uk  
1   closed        f   england  
2  pending  unknown  scotland  
```
```python
test_config = config_map_valid
print(test_config)
```
```text
{'categories':
 {'col_list': ['status', 'gender', 'region'],  
  'strategy': 'lower',  
  'map': {'status': {'open': 'Open', 'closed': 'Closed', 'pending': 'Pending'},  
          'gender': {'m': 'Male', 'f': 'Female', 'unknown': 'Unknown'},  
          'region': {'uk': 'United Kingdom', 'england': 'England', 'scotland': 'Scotland'}}}}
```
```python
clean_pipeline(df=df_config_map_test, config=test_config);
```
*No errors raised*

```python
test_config = config_map_not_dict
print(test_config)
```
```text
{'categories':
 {'col_list': ['status'],
  'strategy': 'lower',
  'map': 123}}
```
```python    
clean_pipeline(df=df_config_map_test, config=test_config);
```
*ValueError: Invalid parameter values found in config: ['function categories parameter map must be a dictionary, not int']*

```python
test_config = config_map_bad_outer_key
print(test_config)
```
```text
{'categories':
 {'col_list': ['status'],
  'strategy': 'lower',
  'map': {'ghost_col': {'open': 'Open'}}}}
```
```python
clean_pipeline(df=df_config_map_test, config=test_config);
```
*ValueError: Invalid parameter values found in config: ["function categories parameter map contains columns not in scope: ['ghost_col']"]*

```python
test_config = config_map_outer_value_not_dict
print(test_config)
```
```text
{'categories':
 {'col_list': ['status'],
  'strategy': 'lower',
  'map': {'status': 'Open'}}}
```
```python
clean_pipeline(df=df_config_map_test, config=test_config);
```
*ValueError: Invalid parameter values found in config: ["function categories parameter map contains non-dict mappings for columns: ['status']"]*

```python
test_config = config_map_empty_inner
print(test_config)
```
```text
{'categories':
 {'col_list': ['status'],
  'strategy': 'lower',
  'map': {'status': {}}}}
```  
```python
clean_pipeline(df=df_config_map_test, config=test_config);
```
*ValueError: Invalid parameter values found in config: ['function categories parameter map column status has an empty mapping dictionary']*

```python
test_config = config_map_mismatched_types
print(test_config)
```
```text
{'categories':
 {'col_list': ['status'],
  'strategy': 'lower',
  'map': {'status': {'open': 1, 'closed': 'Closed'}}}}
```
```python
clean_pipeline(df=df_config_map_test, config=test_config);
```
*ValueError: Invalid parameter values found in config: ['function categories parameter map column status has mismatched key/value types: str → int', 'function categories parameter map column status must map strings to strings']*

```python
test_config = config_map_non_string_key
print(test_config)
```
```text
{'categories':
 {'col_list': ['status'],
  'strategy': 'lower',
  'map': {'status': {1: 'Open', 'closed': 'Closed'}}}}
```
```python
clean_pipeline(df=df_config_map_test, config=test_config);
```
*ValueError: Invalid parameter values found in config: ['function categories parameter map column status has mismatched key/value types: int → str', 'function categories parameter map column status must map strings to strings']*

```python
test_config = config_map_non_string_value
print(test_config)
```
```text
{'categories':
 {'col_list': ['status'],
  'strategy': 'lower',
  'map': {'status': {'open': 1, 'closed': 'Closed'}}}}
```
```python
clean_pipeline(df=df_config_map_test, config=test_config);
```
*ValueError: Invalid parameter values found in config: ['function categories parameter map column status has mismatched key/value types: str → int', 'function categories parameter map column status must map strings to strings']*

```python
test_config = config_map_multiple_errors
print(test_config)
```
```text
{'categories':
 {'col_list': ['status', 'gender'],
  'strategy': 'lower',
  'map': {'status': {'open': 1, 2: 'Closed'}, 'gender': {}}}}
```
```python
clean_pipeline(df=df_config_map_test, config=test_config);
```
*ValueError: Invalid parameter values found in config:*
   *['function categories parameter map column status has mismatched key/value types: str → int',*
    *'function categories parameter map column status has mismatched key/value types: int → str',*
    *'function categories parameter map column gender has an empty mapping dictionary']*

```python
test_config = config_map_extra_columns
print(test_config)
```
```text
{'categories':
 {'col_list': ['status', 'gender'],
  'strategy': 'lower',
  'map': {'status': {'open': 'Open'}, 'gender': {'m': 'Male'}, 'region': {'uk': 'United Kingdom'}}}}
```
```python
clean_pipeline(df=df_config_map_test, config=test_config);
```
*ValueError: Invalid parameter values found in config: ["function categories parameter map contains columns not in scope: ['region']"]*

```python
test_config = config_map_inner_not_dict
print(test_config)
```
```text
{'categories':
 {'col_list': ['status', 'gender'],
  'strategy': 'lower',
   'map': {'status': {'open': 'Open'}, 'gender': 'Male'}}}
```
```python
clean_pipeline(df=df_config_map_test, config=test_config);
```
*ValueError: Invalid parameter values found in config: ["function categories parameter map contains non-dict mappings for columns: ['gender']"]*

### `Config Dictionary General Validation Tests`

```python
print(df_config_test_small)
```
```text
     num_col str_col
  0        1       a
  1        2       b
  2        3       c
```
```python
test_config = config_bad_tags
print(test_config)
```
```text
{'string':
 {'strategy': 'strip'},
  'dates': {'strategy': 'median'},
  'not_a_tag': {'foo': 'bar'},
  'missing': {'col_dict': {'num_col': 'number'}}}
```
```python
clean_pipeline(df=df_config_test_small, config=test_config);
```
*ValueError: Invalid cleaning function tags found: {'not_a_tag': 'parameter not_a_tag is not a valid cleaning function tag'}*

```python
test_config = config_bad_param_types
print(test_config)
```
```text
{'string': 'strip',
 'dates': 123,
 'missing': {'col_dict': {'num_col': 'number'}},
 'numeric': None}
```
```python
clean_pipeline(df=df_config_test_small, config=test_config);
```
*TypeError: Invalid parameter types found - must be dicts: {'string': 'parameter strip is type str', 'dates': 'parameter 123 is type int', 'numeric': 'parameter None is type NoneType'}*

```python
test_config = config_bad_param_names
print(test_config)
```
```text
{'string': {'strategy': 'strip', 'wrong_param': True},
 'dates': {'strategy': 'median', 'invalid': 123},
 'missing': {'col_dict': {'num_col': 'number'}, 'badname': 'oops'},
 'numeric': {'col_list': ['num_col'], 'empty': 'not_valid'}}
```
```python
clean_pipeline(df=df_config_test_small, config=test_config);
```
*ValueError: functions have invalid parameter names: {'string': ['wrong_param'], 'dates': ['invalid'], 'missing': ['badname'], 'numeric': ['empty']}*

```python
print(df_config_test_stress)
```
```text
  num_col str_col   date_col bool_col
0       1   Hello 2020-01-01     True
1       2     N/A 1970-01-01    False
2    1000     ??? 2026-09-16     True
3    -999   world        NaT     None

```
```python
print(config_stress_clean)
```
```text
{'duplicates': {'col_list': ['ghost_col']},
 'string': {'strategy': 'explode'}, 'dates': {'strategy': 123},
 'missing': {'col_dict': {'ghost_col':
 'number'}, 'strat_dict': {'number': 'warpdrive'}, 'val_dict': {'number': ['oops']}},
 'numeric': {'col_list': ['str_col'], 'strategy': 'void', 'outlier': 999},
 'outliers': {'col_list': ['date_col'], 'method': 'unknown'},
 'categories': {'col_list': ['num_col'], 'strategy': 'reverse'},
 'scaling': {'col_list': ['str_col'], 'strategy': 'log'}}
```
```python
clean_pipeline(df=df_config_test_stress, config=config_stress_clean);
```
*ValueError: Invalid parameter values found in config: ["function duplicates col list contains columns not in dataframe: ['ghost_col']", 'function string parameter strategy contains invalid parameters: explode', 'function dates parameter strategy contains invalid parameters: 123', "function missing col dict contains columns not in dataframe: ['ghost_col']", 'function missing parameter strat_dict contains invalid replacement types for missing number types: warpdrive', "function missing parameter val_dict contains incorrect token types for number: ['oops']", "No numeric columns found in function numeric col list: ['str_col']", 'function numeric parameter strategy contains invalid parameters: void', 'function numeric parameter outlier contains invalid parameters: 999', "No numeric columns found in function outliers col list: ['date_col']", 'function outliers parameter method contains invalid parameters: unknown', "No string/category columns found in function categories col list: ['num_col']", 'function categories parameter strategy contains invalid parameters: reverse', "No numeric columns found in function scaling col list: ['str_col']", 'function scaling parameter strategy contains invalid parameters: log']*

```python
print(df_processing_test)
```
```text
      name   signup_date  score mixed_num  outlier_col category  scale_me     notes
0    Alice    2024-01-01   10.0        10           10      Red         1        ok
1      BOB    01/02/2024    NaN      20.5           12      RED         2      fine
2      NaN           NaN   30.0       NaN           11     blue         3     check
3  charlie  March 3 2024    NaN   invalid            9      NaN         4       NaN
4     DAVE    not a date   50.0        40          500     Blue         5      done
5    Alice    2024-01-01   10.0        10           10      Red         1        ok
```
```python
print(config_processing_test)
```
```text
{'string': {'strategy': 'lower'},
 'dates': {'strategy': 'median'},
 'missing': {'strat_dict': {'number': 'median', 'string': '', 'date': 'today', 'bool': False}},
 'numeric': {'strategy': 'mean', 'outlier': 3},
 'outliers': {'method': 'iqr', 'col_list': ['outlier_col']},
 'categories': {'strategy': 'lower', 'map': {'category': {'red': 'Red', 'blue': 'Blue'}}},
 'scaling': {'strategy': 'minmax'},
 'duplicates': {'col_list': ['name']}}
```
```python
df_clean, summary = clean_pipeline(df=df_processing_test, config=config_processing_test)
print(df_clean)
```
```text
      name   signup_date  score mixed_num  outlier_col category  scale_me   notes
0    alice    2024-01-01    0.0        10     0.333333      Red  0.000000      ok
1      bob    01/02/2024    1.0      20.5     1.000000      Red  0.333333    fine
2     <NA>          <NA>    1.0      <NA>     0.666667     Blue  0.666667   check
3  charlie  march 3 2024    1.0   invalid     0.000000     <NA>  1.000000     <NA>
```
```python
print(format_pipeline_summary(summary))
```
```text
=== CLEANING PIPELINE SUMMARY ===

Steps executed:
  • duplicates
  • string
  • dates
  • missing
  • numeric
  • outliers
  • categories
  • scaling

Steps skipped:

--- PARAMETERS PASSED ---

[string]
  strategy: lower

[dates]
  strategy: median

[missing]
  strat_dict: {'number': 'median', 'string': '', 'date': 'today', 'bool': False}

[numeric]
  strategy: mean
  outlier: 3

[outliers]
  method: iqr
  col_list: ['outlier_col']

[categories]
  strategy: lower
  map: {'category': {'red': 'Red', 'blue': 'Blue'}}

[scaling]
  strategy: minmax

[duplicates]
  col_list: ['name']

--- CLEANING FUNCTION OUTPUTS ---

[duplicates]
  messages: Fully duplicated rows in dataset (first 10 only shown):
    name signup_date  score mixed_num  outlier_col category  scale_me notes
5  Alice  2024-01-01   10.0        10           10      Red         1    ok

 Total 1

All fully duplicated rows removed
There are no rows duplicated on  ['name']  in dataset


[string]
  (no output recorded)

[dates]
  (no output recorded)

[missing]
  summary:
    Columns in scope and type to enforce: {'name': 'string', 'signup_date': 'string', 'score': 'number', 'mixed_num': 'string', 'outlier_col': 'number', 'category': 'string', 'scale_me': 'number', 'notes': 'string'}
    Missing values per column: {'name': 1, 'signup_date': 1, 'score': 2, 'mixed_num': 1, 'outlier_col': 0, 'category': 1, 'scale_me': 0, 'notes': 1}
    Total missing values:: 7
    Strategy applied: {'number': 'median', 'string': '', 'date': 'today', 'bool': False}

[numeric]
  (no output recorded)

[outliers]
  messages: Outliers in numeric columns by values < q1-(1.5 x iqr) or > q3+(1.5 x iqr) (ranked by distance):
   name signup_date  score mixed_num  outlier_col category  scale_me notes
4  dave  not a date   50.0        40          500     blue         5  done
Total rows removed: 1


[categories]
  summary:
    Columns processed: ['name', 'signup_date', 'score', 'mixed_num', 'outlier_col', 'category', 'scale_me', 'notes']
    Capitalization Strategy: lower
    Mappings applied: {'category': {'red': 'Red', 'blue': 'Blue'}}
    category: {'unique values before normalization': {'red', 'blue', <NA>}, 'unique values after normalization': {'Blue', 'Red', <NA>}, 'normalized value counts':          Normalized Count
Original                 
red             Red   [2]
blue           Blue   [1], 'unmapped categories': {<NA>}}

[scaling]
  summary:
    Columns processed: ['score', 'outlier_col', 'scale_me']
    Strategy: minmax
    score: {'Minimum': 10.0, 'Maximum': 30.0}
    outlier_col: {'Minimum': 9, 'Maximum': 12}
    scale_me: {'Minimum': 1, 'Maximum': 4}

Final dataframe shape:
  rows: 4
  cols: 8