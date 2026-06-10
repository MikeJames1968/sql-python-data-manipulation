class OutOfStockError(Exception):
    pass

class Inventory:
    def __init__(self):
        self.invent_dict = {}

    def __str__(self):
        return f"Inventory: {self.invent_dict}"
    
    def add_item(self, name, qty):
        if name in self.invent_dict:
            self.invent_dict[name] += qty
            return f"{name} stock increased by {qty} to {self.invent_dict[name]} items"
        else:
            self.invent_dict[name] = qty
            return f"{name} stock entry created with {qty} items"

    def remove_item(self, name, qty):
        try:
            if name not in self.invent_dict:
                raise KeyError(f"stock item {name} not in inventory")
            else:
                if self.invent_dict[name] < qty:
                    raise OutOfStockError(f"stock item {name} has only {self.invent_dict[name]} left, not possible to remove {qty}")
                else:
                    self.invent_dict[name] -= qty
                    return f"{name} stock decreased by {qty} to {self.invent_dict[name]} items"
        except Exception as e:
            return f"Error: {e}"

    def get_stock(self, name):
        try:
            if name not in self.invent_dict:
                raise KeyError(f"{name} not found")
            else:
                return f"{name} stock is {self.invent_dict[name]} items"
        except Exception as e:
            return f"Error: {e}"
        

# Tests
I=Inventory()
print(I.add_item("Apples", 10))
print(I.add_item("Bananas", 5))
print(I.add_item("Oranges", 20))

print(I.add_item("Bananas", 7))
print(I.remove_item("Apples", 2))
print(I.remove_item("Oranges", 21))
print(I.remove_item("Lemons", 1))

print(I.get_stock("Apples"))
print(I.get_stock("Bananas"))
print(I.get_stock("Oranges"))

print(I)