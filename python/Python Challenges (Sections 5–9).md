# 🧩 Python Challenges (Sections 5–9)

A compact set of Python exercises designed to consolidate:

- **Section 5:** Data types  
- **Section 6:** Loops  
- **Section 7:** Functions  
- **Section 8:** Exceptions  
- **Section 9:** Classes  

Each challenge includes a stretch goal.  
You can complete the whole pack in **1–2 days**.

---

## 1. [Mini Data Cleaner](ca://s?q=Challenge_1_Build_a_Mini_Data_Cleaner)

Write a function:

```python
clean_scores(data)
```

Where:

- `data` is a list containing mixed values, e.g.:

  ```python
  ["42", 17, "N/A", None, "  81 ", "error", 55]
  ```

Your function must:

- convert valid numeric strings to integers  
- strip whitespace  
- ignore invalid entries  
- return a dictionary:

  ```python
  {
      "clean": [...],
      "invalid": [...],
      "average": <float or None>
  }
  ```

- handle empty clean lists safely

**Stretch:**  
Raise a custom exception if *all* values are invalid.

---

## 2. [Simple Inventory System](ca://s?q=Challenge_2_A_Simple_Inventory_System)

Create an `Inventory` class with:

- internal storage: `{"item_name": quantity}`
- methods:
  - `add_item(name, qty)`
  - `remove_item(name, qty)`
  - `get_stock(name)`
  - `total_items()`

Rules:

- raise a custom `OutOfStockError` if removal exceeds stock  
- raise `KeyError` if item doesn’t exist  

**Stretch:**  
Implement `__str__` to print a clean summary.

---

## 3. [Temperature Converter](ca://s?q=Challenge_3_Temperature_Converter)

Write a function:

```python
convert_temp(value, unit)
```

Where:

- `unit` is `"C"` or `"F"`
- convert Celsius ↔ Fahrenheit
- raise `ValueError` for invalid units
- raise `TypeError` for non‑numeric values
- return a tuple `(converted_value, new_unit)`

**Stretch:**  
Add Kelvin support.

---

## 4. [Class‑Based Bank Account](ca://s?q=Challenge_4_Class_Based_Bank_Account)

Create a `BankAccount` class with:

- attributes: `owner`, `balance`
- methods:
  - `deposit(amount)`
  - `withdraw(amount)`
  - `transfer(other_account, amount)`

Rules:

- raise `ValueError` for negative amounts  
- raise `RuntimeError` for insufficient funds  
- implement `__repr__` for debugging  

**Stretch:**  
Add a transaction history list of dicts.

---

## 5. [Word Frequency Counter](ca://s?q=Challenge_5_Word_Frequency_Counter)

Write a function:

```python
word_count(text)
```

That:

- lowercases text  
- strips punctuation  
- splits into words  
- returns a dict `{word: frequency}`  
- returns a sorted list of `(word, count)` tuples  

**Stretch:**  
Ignore stopwords such as `"the"`, `"and"`, `"of"`.

---

## 6. [Mini JSON Validator](ca://s?q=Challenge_6_Mini_JSON_Validator)

Write a function:

```python
validate_json(data)
```

Where `data` is a Python dict representing JSON.

Validate:

- all keys are strings  
- values are only: `str`, `int`, `float`, `bool`, `None`, `list`, `dict`  
- lists contain only valid JSON types  
- nested dicts are validated recursively  

Return:

```python
{
    "valid": True/False,
    "errors": [list of error messages]
}
```

**Stretch:**  
Raise a custom `JSONValidationError`.

---

## 7. [Simple CLI Menu System](ca://s?q=Challenge_7_Simple_CLI_Menu_System)

Build a text‑based menu:

```
1. Add item
2. Remove item
3. List items
4. Quit
```

Use a list as storage.  
Handle invalid input gracefully.  

**Stretch:**  
Integrate a function to print the new menu after every addition or deletion

