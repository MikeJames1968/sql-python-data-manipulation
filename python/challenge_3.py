class OutOfRangeError(Exception):
    pass

def convert_temp(value, unit):
    unit = unit.upper()
    if unit not in {"C","F","K"}:
        raise ValueError(f"Unit {unit} not valid ")
    if not isinstance(value, (int,float)):
        raise TypeError(f"{value} is not numeric")
    match unit:
        case "C":
            if value < -273.15:
                raise OutOfRangeError (f"{value} is below the minimum centigrade value of -273.15")
            converted_valuef = (value * 1.8) + 32
            converted_valuek = value + 273.15
            return [ ("fahrenheit", round(converted_valuef,2)), ("kelvin", round(converted_valuek,2)) ]
        case "F":
            if value < -459.67:
                raise OutOfRangeError (f"{value} is below the minimum farenheit value of -459.67")
            converted_valuec = (value - 32) / 1.8
            converted_valuek = converted_valuec + 273.15
            return [ ("centigrade", round(converted_valuec,2)), ("kelvin", round(converted_valuek,2)) ]
        case "K":
            if value < 0:
                raise OutOfRangeError (f"{value} is below the minimum kelvin value of 0")
            converted_valuec = value - 273.15
            converted_valuef = (converted_valuec * 1.8) + 32
            return [ ("centigrade", round(converted_valuec,2)), ("fahrenheit", round(converted_valuef,2))]

# Call it
print(convert_temp(100,"C"))
print(convert_temp(132.5,"F"))
print(convert_temp(300, "K"))

# Test invalid argument exceptions
# print(convert_temp("10","C"))
# print(convert_temp(30,"D"))

# Test out of range exceptions
# print(convert_temp(-274,"C"))
# print(convert_temp(-460,"F"))
# print(convert_temp(-1,"K"))
