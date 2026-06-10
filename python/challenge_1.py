# define custom exception if all entries invalid
class AllInvalid(Exception):
    pass

data = ["42", 17, "N/A", None, "  81 ", "error", 55]

def clean_scores(data):
    clean = []
    invalid = []

    for item in data:
        match item:
            case int():
                clean.append(item)
            case float():
                clean.append(int(item))
            case str():
                str_item = item.strip()
                try:
                    # try float conversion
                    flt_item = float(str_item)
                    # try integer conversion
                    int_item = int(flt_item)
                    # valid integer
                    clean.append(int_item)                
                except ValueError:
                    # string is not a valid integer
                    invalid.append(str_item)
            case _:
                # item is not integer, float, or a valid integer string
                invalid.append(item)

     # check if all entries are invalid
    if len(clean) == 0 and len(invalid) > 0:
        raise AllInvalid("All data entries in list are invalid")
    
   # calculate average
    average = None
    if len(clean) > 0:
        average = float(sum(clean) / len(clean))
    
    # construct return dictionary
    return {"clean" : clean, "invalid" : invalid, "average" : average}

# call it
print (clean_scores(data))