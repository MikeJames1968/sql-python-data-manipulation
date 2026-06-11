class BankAccount:
    def __init__(self):
        self.owner = ""
        self.balance = 0
        self.trans_history = []

    def __repr__(self):
        return f"Account owner: {self.owner}, current balance: {self.balance}"
    
    def deposit(self, amount):
        if amount < 0:
            raise ValueError ("Not possible to deposit negative amounts")
        self.balance += amount
        self.trans_history.append({"date/time:" : self.stamp(), "deposit" : amount, "new balance" : self.balance})
        return f"{amount} succesfully deposited. New balance: {self.balance}"
    
    def withdraw(self, amount):
        if amount < 0:
            raise ValueError ("Not possible to withdraw negative amounts")
        elif amount > self.balance:
            raise RuntimeError (f"Available balance is {self.balance}. Insufficient funds for withdrawal")
        self.balance -= amount
        self.trans_history.append({"date/time:" : self.stamp(), "withdrawal" : amount, "new balance" : self.balance})
        return f"{amount} successfully withdrawn New balance: {self.balance}"
    
    def transfer(self, other_account, amount):
        if amount < 0:
            raise ValueError ("Not possible to transfer negative amounts")
        elif amount > self.balance:
            raise RuntimeError (f"Available balance is {self.balance}. Insufficient funds for transfer")
        elif not isinstance(other_account, BankAccount):
            raise TypeError (f"transfer destination {other_account} is not a valid bank account")
        other_account.deposit(amount)   # deposit to other account
        self.balance -= amount          # deduct from this account
        self.trans_history.append({"date/time:" : self.stamp(), "transfer" : amount, "new balance" : self.balance})
        return f"{amount} successfully transferred to account {other_account} New balance: {self.balance}"
    
    def transactions(self):
        return self.trans_history
    
    def stamp(self):
        from datetime import datetime
        return datetime.now().strftime("%I:%M:%S %p on %d %B %Y")
   
# Setup accounts

acc1 = BankAccount()
acc1.owner = "Mike"
acc2 = BankAccount()
acc2.owner = "Geoff"
noaccount = ""

# Test deposit, withdrawal and transfer

acc1.deposit(100)
print(acc1)
acc1.withdraw(50)
print(acc1)
acc1.transfer(acc2, 10)
print(acc1)
print(acc2)

for trans in acc1.transactions():
    print (trans)

for trans in acc2.transactions():
    print (trans)

# Test exceptions

# acc1.deposit(-20)
# acc1.withdraw(-30)
# acc1.transfer(acc2, -60)
# acc1.withdraw(50)         ## Bal should be 40
# acc1.transfer(acc2, 50)   ## Bal should be 40
# acc1.transfer(noaccount, 5)
