# Task 9 - final cleaning engine
# The config parameter is not optional - the function does nothing if it is not passed

import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype, is_datetime64_any_dtype, is_string_dtype, is_object_dtype
import contextlib
import io
from datetime import date

def clean_pipeline(df, config):

    # Section 1 - Validate Config File

   
    # Take no action if config is empty
    if (not config) or (config is None):
        raise ValueError('No config dictionary passed')
    
    # Check dataframe type
    if not isinstance(df, pd.DataFrame):
        raise TypeError('No valid dataframe passed')

    # Check the config parameter is a dictionary
    if not isinstance(config, dict):
        raise TypeError('Config object is not a dictionary')

    # Setup config dictionary validator
    validator = {   'dates'      : {'strategy'   : ['mode',   'median']},
                    'string'	 : {'strategy'   : ['strip',  'title', 'lower', 'upper']},
                    'missing'    : {'col_dict'   : ['bool',   'number', 'string', 'date', 'object'],
                                    'strat_dict' : {'bool'   : [True, False, 'drop', 'none'],
                                                    'number' : ['mean', 'mode','median', 'zero', 'drop', 'none'],
                                                    'string' : ['', 'drop', 'none'],
                                                    'date'   : ['today', 'drop', 'none'],
                                                    'object' : ['string', 'number', 'drop', 'none']},
                                    'val_dict'   : ['number', 'date', 'string']},
                    'duplicates' :  {'col_list'  : 'any'},
                    'outliers'   :  {'col_list'  : 'num',     'method'   : ['iqr', 'zscore']},
                    'numeric'    :  {'col_list'  : 'num',     'strategy' : ['zero', 'mean', 'nan'], 'outlier' : [-1,1,2,3,4,5,6]},
                    'categories' :  {'col_list'  : 'str/cat', 'strategy' : ['strip','title','lower','upper'], 'map' : 'map'},
                    'scaling'    :  {'col_list'  : 'num',     'strategy' : ['zscore','minmax','robust']} }

    # Check for invalid config functions
    valid_fns = list(validator)
    invalid_fns = {par : f'parameter {par} is not a valid cleaning function tag' for par in config if par not in valid_fns}

    if invalid_fns:
        raise ValueError(f'Invalid cleaning function tags found: {invalid_fns}')

    # Check functions have parameter dictionaries
    invalid_ptypes = {fun : f'parameter {par} is type {type(par).__name__}' for fun, par in config.items() if not isinstance(par, dict)}
    
    if invalid_ptypes:
        raise TypeError(f'Invalid parameter types found - must be dicts: {invalid_ptypes}')

    # Check function parameter dictionaries contain only valid parameter names
    bad_pnames = {fun : [key for key in config[fun] if key not in validator[fun]] for fun in config}

    if any(bad_pnames.values()):
        bad_pnames = {key : val for key, val in bad_pnames.items() if val != []}
        raise ValueError(f'functions have invalid parameter names: {bad_pnames}')

    # Validate function dictionary parameters
    invalid_pvals = []
    
    for fun, pdict in config.items():

        for pname, pvalue in pdict.items():

            # Check column list parameter
            if pname == 'col_list':

                # Check type
                if not isinstance(pvalue, list):
                    invalid_pvals.append(f'function {fun} parameter {pname} is type {type(pvalue).__name__}, must be a list')
                else:
                    # Check list is of valid col names
                    bad_cnames = [par for par in pvalue if par not in df.columns]

                    if bad_cnames:
                        invalid_pvals.append(f'function {fun} col list contains columns not in dataframe: {bad_cnames}')
                    else:
                        # Check if list of col names include specified types
                        match validator[fun][pname]:
                            case 'num':
                                if not any(col in pvalue for col in df.select_dtypes(include = 'number').columns):
                                    invalid_pvals.append(f'No numeric columns found in function {fun} col list: {pvalue}')
                            case 'str/cat':
                                if not any(col in pvalue for col in df.select_dtypes(include = ['string', 'category']).columns):
                                    invalid_pvals.append(f'No string/category columns found in function {fun} col list: {pvalue}')
                            case 'any':
                                pass

            # Check column dictionary parameter (clean_missing_function)
            elif pname == 'col_dict':

                # Check type
                if not isinstance(pvalue, dict):
                    invalid_pvals.append(f'function {fun} parameter {pname} is type {type(pvalue).__name__}, must be a dictionary')
                else:
                    # Check dictionary keys are valid col names
                    bad_cnames = [key for key in pvalue if key not in df.columns]

                    if bad_cnames:
                        invalid_pvals.append(f'function {fun} col dict contains columns not in dataframe: {bad_cnames}')
                    else:                        
                        bad_cotypes = {col : val for col, val in pvalue.items() if val not in validator[fun][pname]}

                        if any(bad_cotypes.values()):
                            invalid_pvals.append(f'function {fun} parameter {pname} contains invalid coerce types: {bad_cotypes}')
            
            # Check strategy dictionary parameters (clean_missing_function)
            elif pname == 'strat_dict':

                # Check type
                if not isinstance(pvalue, dict):
                    invalid_pvals.append(f'function {fun} parameter {pname} is type {type(pvalue).__name__}, must be a dictionary')
                else:
                    # Check dictionary keys are valid types
                    bad_ctypes = [key for key in pvalue if key not in validator[fun][pname]]

                    if bad_ctypes:
                        invalid_pvals.append(f'function {fun} parameter {pname} contains invalid types: {bad_ctypes}')
                    else:
                        # Check dictionary values are valid missing value replacements
                        bad_repls = {ctype : val for ctype, val in pvalue.items() if val not in validator[fun][pname][ctype]}

                        for ctype, bad in bad_repls.items():
                            invalid_pvals.append(f'function {fun} parameter {pname} contains invalid replacement types for missing {ctype} types: {bad}')

            # Check value dictionary parameters (clean_missing_function)
            elif pname == 'val_dict':

                # Check type
                if not isinstance(pvalue, dict):
                    invalid_pvals.append(f'function {fun} parameter {pname} is type {type(pvalue).__name__}, must be a dictionary')
                else:
                    bad_vtypes = [key for key in pvalue if key not in validator[fun][pname]]
                                        
                    if bad_vtypes:
                        invalid_pvals.append(f'function {fun} parameter {pname} contains invalid missing value types: {bad_vtypes}')
                    else:   
                        # Check dictionary values are lists
                        bad_vttypes = {vtype : val for vtype, val in pvalue.items() if not isinstance(val, list)}

                        for vtype, bad in bad_vttypes.items():
                            invalid_pvals.append(f'function {fun} parameter {pname} entry {vtype} is type {type(bad).__name__}, must be a list')
                        else:
                            # Check dictionary token lists contain only the specified token types
                            bad_toktypes = {}

                            for t_type, t_list in pvalue.items():
                                bad_toktypes[t_type] = [token for token in t_list if not isinstance(token, (int, float) if t_type == 'number' else (date if t_type == 'date' else str)) ]

                                if bad_toktypes[t_type]:
                                    invalid_pvals.append(f'function {fun} parameter {pname} contains incorrect token types for {t_type}: {bad_toktypes[t_type]}')

            # Check mappings dictionary parameter (clean_categories function)
            elif pname == 'map':

                # Must be a dictionary
                if not isinstance(pvalue, dict):
                    invalid_pvals.append(f'function {fun} parameter {pname} must be a dictionary, not {type(pvalue).__name__}')
                else:

                    # Outer keys must be valid column names
                    allowed_cols = pdict['col_list'] if 'col_list' in pdict else df.columns
                    bad_outer_cols = [col for col in pvalue if col not in allowed_cols]

                    if bad_outer_cols:
                        invalid_pvals.append(f'function {fun} parameter {pname} contains columns not in scope: {bad_outer_cols}')
                    else:

                        # Outer values must be dicts
                        bad_inner_dicts = {col: inner for col, inner in pvalue.items() if not isinstance(inner, dict)}
                        if bad_inner_dicts:
                            invalid_pvals.append(f'function {fun} parameter {pname} contains non-dict mappings for columns: {list(bad_inner_dicts)}')
                        else:

                            # Validate each inner mapping dict
                            for col, inner in pvalue.items():

                                # Inner dict must not be empty
                                if not inner:
                                    invalid_pvals.append(f'function {fun} parameter {pname} column {col} has an empty mapping dictionary')
                                else:

                                    # Keys and values must be same type
                                    for raw, canon in inner.items():
                                        if type(raw) is not type(canon):
                                            invalid_pvals.append(f'function {fun} parameter {pname} column {col} has mismatched key/value types: '
                                                                 f'{type(raw).__name__} → {type(canon).__name__}')

                                        # Optional: enforce string-only mappings (common in category cleaning)
                                        elif not all(isinstance(k, str) and isinstance(v, str) for k, v in inner.items()):
                                            invalid_pvals.append(f'function {fun} parameter {pname} column {col} must map strings to strings')

            # Check simple parameters
            elif pvalue not in validator[fun][pname]:
                invalid_pvals.append(f'function {fun} parameter {pname} contains invalid parameters: {pvalue}')

    if invalid_pvals:
        raise ValueError(f'Invalid parameter values found in config: {invalid_pvals}')

    # Section 2 - Processing

    # Redirect printed messages from cleaning functions into buffer to keep output neat

    messages = io.StringIO()
    with contextlib.redirect_stdout(messages):
    
        # Sub-function to add entries to message dictionary
        def add_output(func, mess_obj, summ = None):
            mess_dict[func] = {}

            # Add printed output if there is any
            if mess_obj.tell() != 0:
                mess_dict[func]['messages'] = mess_obj.getvalue()
                mess_obj.seek(0)
                mess_obj.truncate(0)
        
            # Add summary if there is one
            if summ:
                mess_dict[func]['summary'] = summ
                        
        # Call cleaning functions if tagged in config

        df_clean = df.copy()
        mess_dict = {}
        
        if 'duplicates' in config:
            df_clean = clean_duplicates(df = df_clean, col_list = config['duplicates'].get('col_list'))
            add_output( 'duplicates', messages )

        if 'string' in config:

            # Extract all string columns and process each
            str_cols = df_clean.select_dtypes(include='string').columns.to_list()

            for col in str_cols:
                df_clean[col] = clean_string(df_clean[col], strategy=config['string'].get('strategy'))
            add_output( 'string', messages )

        if 'dates' in config:

            # Extract all date columns and process each
            date_cols = df_clean.select_dtypes(include='datetime64').columns.to_list()
            for col in date_cols:
                df_clean[col] = clean_date(df_clean[col], strategy=config['dates'].get('strategy'))
            add_output( 'dates', messages )

        if 'missing' in config:
            df_clean, summary_m = clean_missing(df = df_clean, col_dict = config['missing'].get('col_dict'),
                                                            strat_dict = config['missing'].get('strat_dict'),
                                                            val_dict = config['missing'].get('val_dict'))
            add_output( 'missing', messages, summary_m )

        if 'numeric' in config:
            df_clean = clean_num(df = df_clean, col_list = config['numeric'].get('col_list'),
                                                strategy = config['numeric'].get('strategy'),
                                                outlier = config['numeric'].get('outlier'))
            add_output( 'numeric', messages )

        if 'outliers' in config:
            df_clean = clean_outliers(df = df_clean, col_list = config['outliers'].get('col_list'),
                                                    method=config['outliers'].get('method'))
            add_output( 'outliers', messages )

        if 'categories' in config:
            df_clean, summary_c = clean_categories(df = df_clean, col_list=config['categories'].get('col_list'),
                                                                strategy=config['categories'].get('strategy'),
                                                                map=config['categories'].get('map'))
            add_output( 'categories', messages, summary_c )

        if 'scaling' in config:
            df_clean, summary_s = scale_numeric(df = df_clean, col_list = config['scaling'].get('col_list'),
                                                                strategy = config['scaling'].get('strategy'))
            add_output( 'scaling', messages, summary_s )

    # Construct summary report
    summary = {'steps run' : mess_dict.keys()}
    steps_skipped = set(validator.keys()) - set(mess_dict.keys())
    summary['steps skipped'] = steps_skipped
    summary['parameters passed'] = config
    summary['cleaning function outputs'] = mess_dict
    summary['cleaned dataframe shape'] = df_clean.shape
    
    return df_clean, summary

# Task 1 - clean a date column
# The optional paramter missing defaults to 'mode' (most common practice)

def clean_date(date_col, strategy):
    strategy = 'mode' if strategy is None else strategy
    
    # Force all formats to datetime
    # Note using errors = 'coerce' converts impossible dates to nan, which is industry standard practice
    date_col = pd.to_datetime(date_col, format='mixed', errors='coerce')

    # Convert NaT entries to either mode or median date
    if strategy == 'median':
        to_date = date_col.median()
    else:
        to_date = date_col.mode()[0]

    date_col = date_col.fillna(to_date)

    return date_col

# Task 2 - trim and normalise string columns
# The optional parameter intocase defaults to 'strip' (don't change case)

def clean_string(str_col, strategy):
    strategy = 'strip' if strategy is None else strategy

    # Strip whitespace first
    str_col = str_col.str.strip()

    # Remove embedded whitespace
    str_col = str_col.str.replace(r'\s+', ' ', regex=True)

    # Replace empty and null columns with NaN
    str_col = str_col.replace(['', None], np.nan)

    # Force upper, lower or title case if requested
    match strategy:
        case 'title':
            str_col = str_col.str.capitalize()
        case 'lower':
            str_col = str_col.str.lower()
        case 'upper':
            str_col = str_col.str.upper()

    return str_col

# Task 3 - handle duplicate rows
# Note the optional parameter col_list defaults to all string columns in passed dataframe

def clean_duplicates(df, col_list):
    # Create working dataframe
    df_clean = df.copy()
    
    # Remove whitespace and standardize capitalization for string columns
    string_cols = df_clean.select_dtypes(include='string').columns.tolist()
    for string_col in string_cols:
        df_clean[string_col] = clean_string(str_col = df_clean[string_col], strategy='strip')
    
    # Report fully duplicated rows
    dup_mask = df_clean.duplicated()
    tot_full_dups = dup_mask.sum()
    if tot_full_dups > 0:
        print('Fully duplicated rows in dataset (first 10 only shown):')
        print(df_clean[dup_mask].head(10))
        print('\n Total', tot_full_dups)
        df_clean = df_clean.drop_duplicates()
        print('\nAll fully duplicated rows removed')
    else:
        print('There are no fully duplicated rows in dataset')

    # Report partially duplicated rows if list of columns passed
    # Note no error checking employed - if a list of column names is passed, it is assumed to be accurate

    if col_list:
        part_dup_mask = df_clean.duplicated(subset = col_list)
        tot_part_dups = part_dup_mask.sum()
        if tot_part_dups > 0:
            print('Partially duplicated rows on:', col_list, ' (first 10 only shown):')
            print(df_clean[part_dup_mask].head(10))
            print('\n Total', part_dup_mask.sum())
            df_clean = df_clean.drop_duplicates(subset = col_list)
            print('\nAll partially  duplicated rows removed')
        else:
            print('There are no rows duplicated on ', col_list, ' in dataset')

    return df_clean

# Task 4 - clean outliers
# Note the optional parameters col_list and method default to all columns in dataframe and 'iqr' respectively

def clean_outliers(df, col_list, method):
    col_list = df.columns.to_list() if not col_list else col_list
    method = 'iqr' if method is None else method

    # Create working dataframe
    df_num = df[col_list].select_dtypes(include='number')
    
    # Identify outliers by iqr
    if method == 'iqr':

        # Create series for q1, q3, iqr and upper/lower bounds for all columns
        q1 = df_num.quantile(0.25)
        q3 = df_num.quantile(0.75)
        iqr = q3 - q1
        upper = q3 + 1.5 * iqr
        lower = q1 - 1.5 * iqr

        # Create dataframe of max iqr distances exceeding the bounds
        max_dist = np.maximum(lower - df_num, df_num - upper).clip(lower=0)

        # Collapse dataframe to a series of max values to sort by
        outlier_index = max_dist.max(axis=1)
        outlier_index = outlier_index[outlier_index > 0].sort_values(ascending=False).index

        # Report outliers
        out_text = 'Outliers in numeric columns by values < q1-(1.5 x iqr) or > q3+(1.5 x iqr) (ranked by distance):'

    # Identify outliers by |z| > 3
    else:

        # Create series of max Z-scores
        max_zscores = (((df_num - df_num.mean()) / df_num.std()).abs()).max(axis=1)

        # Create index from series
        outlier_index = max_zscores[max_zscores > 3].sort_values(ascending=False).index

        # Report outliers
        out_text = 'Outliers in numeric columns by|z| > 3 (ranked by |z| value):'
        
    # Print outliers and totals
    print(out_text)
    print(df.loc[outlier_index])
    print(f'Total rows removed: {len(outlier_index)}')

    # Create return dataframe with outliers removed
    df_clean = df.drop(index=outlier_index)
    return df_clean

# Task 5 - clean numeric columns
# The optional paramters repl_nan & ouliers default to 'Z' (zeroes) & 3 (3 x standard deviation is accepted benchmark; 6 is 6-sigma limit) respectively
# Note the brief originally kept outliers to simple numbers, but I missed that and coded a standard deviation which was harder!

def clean_num(df, col_list, strategy, outlier):
    col_list = df.select_dtypes(include='number').columns.to_list() if not col_list else col_list
    strategy = 'nan' if strategy is None else strategy
    outlier = 3 if outlier is None else outlier

    # Process all columns in scope
    df_clean = df.copy()
    outlier_mask = pd.Series(True, index = df_clean.index)

    for col in col_list:
        # Convert integers to floats

        if df_clean[col].dtype != 'float64':
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

        # Replace empty and null columns with zero or mean or nan
        if strategy == 'zero':
            df_clean[col] = df_clean[col].replace([None, np.nan], 0)
        elif strategy == 'mean':
            df_clean[col] = df_clean[col].replace([None, np.nan], df_clean[col].mean())
        elif strategy == 'nan':
            df_clean[col] = df_clean[col].replace([None], np.nan)

        # Remove outliers according to outlier parameter
        if outlier != -1:
            lower = df_clean[col].mean() - (df_clean[col].std() * outlier)
            upper = df_clean[col].mean() + (df_clean[col].std() * outlier)
            outlier_mask &= df_clean[col].between(lower, upper)
        
    df_clean = df_clean[outlier_mask]
    
    return df_clean

# Task 6 - clean missing values
# The optional parameters col_dict and strat_dict default to {} and a supplied default_strategy respectively

default_strategy = {'bool' : False, 'number' : 'median', 'string' : '', 'date' : 'today', 'object' : 'string'}

# Note the default value dict is a sample only for demonstration purposes
 
default_values = {
'number' : [-999],
'string' : ['', ' ', '-', '.', '?', 'N/A', 'n/a', 'NA', 'na', 'NULL', 'null', 'NaN', 'nan', 'None', 'NoneType' '\t', '\n'],
'date'   : [pd.to_datetime('1970-01-01'), pd.to_datetime('9999-12-31')] }

def clean_missing(df, col_dict, strat_dict, val_dict):
    col_dict = {} if not col_dict else col_dict
    strat_dict = default_strategy if not strat_dict else strat_dict
    val_dict = default_values if not val_dict else val_dict

    # Create list of columns in scope and dictionary of corresponding dataframe column types
    col_list = df.columns.to_list() if not col_dict else list(col_dict)
    dtypes = {is_bool_dtype : 'bool', is_numeric_dtype : 'number', is_datetime64_any_dtype : 'date', is_string_dtype : 'string', is_object_dtype : 'object'}
    col_type = {col : next(dtypes[dtype] for dtype in dtypes if dtype(df[col])) for col in col_list}

    # Initialize working dataframe, column rule dictionary and column no rule list
    df_clean = df.copy()
    rule = {}
    no_rule = []

    # Process columns in scope
    
    for col in col_list:

        # Add all columns and existing types to dictionary if missing (except object types)

        if col not in col_dict:

            # If column is type object, force dictionary type to that specified in strategy (usually string)

            if col_type[col] == 'object':
                col_dict[col] = strat_dict['object']
            else:
                col_dict[col] = col_type[col]

        # If column in dictionary, check the type matches the dataframe type (except object type)

        elif (col_type[col] != 'object') and (col_dict[col] != col_type[col]):
            raise TypeError(f'passed column type for {col} is {col_dict[col]}, but column is of type {col_type[col]}')
               
        # Coerce columns to intended type using 'best practice' methods
               
        match col_dict[col]:

            # Coercion is granular to avoid creating object-type columns; boolean columns must be coerced before numeric

            case 'bool':

                # Object columns need special treatment to coerce to boolean!

                if is_object_dtype(df_clean[col]):
                    df_clean[col] = df_clean[col].astype(str).str.strip().str.lower()
    
                df_clean[col] = df_clean[col].map({'true': True, '1': True, 'false': False, '0': False}).astype('boolean')
            case 'number':
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                df_clean[col] = df_clean[col].replace(val_dict['number'],np.nan)
            case 'date':
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                df_clean[col] = df_clean[col].replace(val_dict['date'],np.nan)
            case 'string':
                df_clean[col] = df_clean[col].astype('string')
                df_clean[col] = df_clean[col].replace(val_dict['string'],np.nan)

        # Set up rules for .fillna() based on strategy - no rule is required if strategy is 'none' or 'drop'

        match strat_dict[col_dict[col]]:
            case 'none':
                no_rule.append(col)
            case 'drop':
                pass
            case 'mean':
                rule[col] = df_clean[col].mean()
            case 'median':
                rule[col] = df_clean[col].median()
            case 'mode':
                rule[col] = df_clean[col].mode().iloc[0]
            case 'zero':
                rule[col] = 0
            case 'today':
                rule[col] = np.datetime64('today', 'D')
            case other:                                 # other literal value
                rule[col] = other
        
    # Create summary dictionary: columns in scope, missing values per column, total missing values & strategy applied
    
    summary = {'Columns in scope and type to enforce' : col_dict}
    na_counts = {col : df_clean[col].isna().sum() for col in col_dict}
    summary['Missing values per column'] = na_counts
    summary['Total missing values:'] = sum(na_counts.values())
    summary['Strategy applied'] = strat_dict
    
    # Return any columns with strategy 'none' to their original state
    
    for col in no_rule:
        df_clean[col] = df[col].copy()
        
    # Process remaining columns
    rem_cols = set(col_list) - set(no_rule)
    
    for col in rem_cols:

        if strat_dict[col_dict[col]] == 'drop':
            df_clean = df_clean.dropna(subset=col, how='any')
        else:
            df_clean[col] = df_clean[col].fillna(value=rule[col])

    return df_clean, summary

# Task 7 - clean categories (text or category types)
# Note the optional parameters col_list, strategy and map default to all columns, 'lower' and {} (no map) respectively

def clean_categories(df, col_list, strategy, map):
    col_list = df.columns.to_list() if not col_list else col_list
    strategy = 'lower' if strategy is None else strategy
    map = {} if not map else map
    
    # Create inital summary dictionary entries
    summary = { 'Columns processed' : 'all columns in dataframe' if col_list is None else col_list }
    summary['Capitalization Strategy'] = strategy
    summary['Mappings applied'] = 'default' if map is None else map
        
    # Create working dataframe
    df_clean = df.copy()

    # Process all string and category columns
    cols = df_clean.select_dtypes(include=['category', 'string']).columns.tolist()
    for col in cols:

        # Call clean_string to remove/collapse whitespace and change capitalization, according to passed strategy
        df_clean[col] = clean_string(str_col=df_clean[col], strategy=strategy)

        # map the column if a map is passed

        if col in map:

            # Create summary report entries pre-normalization - note the function expects map keys to be lower case
            
            vals_pre_rep = set(df_clean[col])
            col_lc = df_clean[col].str.lower()
            vals_pre = set(col_lc.str.lower())
            map_keys = set(map[col].keys())
            vals_norm = map_keys.intersection(vals_pre)
            stats_dict = {val: [map[col][val], [col_lc.value_counts()[val]]] for val in vals_norm}
            stats_df = pd.DataFrame.from_dict(stats_dict, orient='index', columns=['Normalized', 'Count']).rename_axis('Original')

            # Replace variants according to map (note match on lower case)
            df_clean[col] = col_lc.replace(map[col])
            
            # Add entries to summary report dictionary for column
            vals_post_rep = set(df_clean[col])
            vals_post = set(df_clean[col].str.lower())
            map_vals = set(pd.Series(list(map[col].values())).str.lower().tolist())
            col_stats = {'unique values before normalization' : vals_pre_rep}
            col_stats['unique values after normalization'] = vals_post_rep
            col_stats['normalized value counts'] = stats_df
            col_stats['unmapped categories'] = 0 if len(vals_post - map_vals) == 0 else vals_post - map_vals

            # Add columns stats summary dictionary to overall summary
            summary[col] = col_stats
    return df_clean, summary

# Task 8 - scale numeric columns
# The optional parameters col_list and strategy default to all number columns and zscore respectively

def scale_numeric(df, col_list, strategy):
    col_list = df.select_dtypes(include='number').columns.to_list() if not col_list else col_list
    strategy = 'zscore' if strategy is None else strategy

    # Create inital summary dictionary entries
    summary = { 'Columns processed' : col_list}
    summary['Strategy'] = strategy

    # Create working dataframe
    df_clean = df.copy()

    # Replace inf values with NaN
    df_clean[col_list] = df_clean[col_list].replace([np.inf, -np.inf], np.nan)

    # Process all columns in scope
    for col in col_list:

        match strategy:
            case 'zscore':

                # Create new scaled column
                mean = df_clean[col].mean(skipna = True)
                std_dev = df_clean[col].std(skipna = True)

                # Check for div by zero
                if std_dev != 0:
                    df_clean[col] = (df_clean[col] - mean) / std_dev
                    col_stats = {'Mean' : mean}
                    col_stats['Standard deviation'] = std_dev
                else:
                    col_stats = 'Cannot scale column, standard deviation is zero!'
            
            case 'minmax':

                # Create new scaled column
                min = df_clean[col].min(skipna = True)
                max = df_clean[col].max(skipna = True)
                range = max - min

                # Check for div by zero
                if range != 0:
                    df_clean[col] = (df_clean[col] - min) / range
                    col_stats = {'Minimum' : min}
                    col_stats['Maximum'] = max
                else:
                    col_stats = 'Cannot scale column, range is zero!'

            case 'robust':

                # Create new scaled column
                median = df_clean[col].median(skipna = True)
                q1 = df_clean[col].quantile(0.25)
                q3 = df_clean[col].quantile(0.75)
                iqr = q3 - q1

                # Check for div by zero
                if iqr != 0:
                    df_clean[col] = (df_clean[col] - median) / iqr
                    col_stats = {'Median' : median}
                    col_stats['Q1 (25th percentile)'] = q1
                    col_stats['Q3 (75th percentile)'] = q3
                    col_stats['IQR = Q3 - Q1'] = iqr
                else:
                    col_stats = 'Cannot scale column, IQR is zero!'

        # Add columns stats dictionary to overall summary
        summary[col] = col_stats

    return df_clean, summary