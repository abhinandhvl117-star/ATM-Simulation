from cryptography.fernet import Fernet
from random import randint
from abc import ABC,abstractmethod
    

class Basic(ABC):
    @abstractmethod
    def __init__(self,account_no,user_pin):
        pass
    
    @abstractmethod
    def check(self):
        pass


#To create a key to encrypt the password
class Key:
    def __init__(self):
        file = open("key.key","rb")
        key = file.read()
        file.close()
        self.fer = Fernet(key)
    
    #KEEP IT COMMENT
    '''def write_key(): 
    key = Fernet.generate_key()
    with open("key.key","wb") as key_file:
        key_file.write(key)'''
    

#create and store details about customer
class Details(Key):
    def __init__(self):
        super().__init__()

        f = open("balance.txt","r") 
        self.old_amount = f.readline()
        f.close()

    def view(self,account):
        with open("details.txt","r") as f:
            for line in f.readlines():
                data = line.rstrip()
                user,account_no,amount,pin = data.strip().split("|")
                decrypt = self.fer.decrypt(pin.encode()).decode()
                if int(account_no) == account:
                    print(f"Name: {user}\nAccount Number: {account_no}\nBalance: {amount}")

    def add(self,name,amount,pin):

        while True:
            account_no = randint(10000000000,99999999999)
            with open("details.txt","r") as f:
                acc = [line.split("|")[1] for line in f]
                if str(account_no) not in acc:
                    break

        with open("details.txt","a") as f:
            encrypt = self.fer.encrypt(pin.encode()).decode()
            f.write(f"{name}|{account_no}|{amount}|{encrypt}\n")

        return account_no
    
    def add_amount(self,amount): 
        new_amount = int(self.old_amount) + int(amount) 

        with open("balance.txt","w") as f:
            f.write(str(new_amount))

        

#admin add money to ATM
#admin login: admin@852, password: 2446
class Add_balance(Basic):
    def __init__(self,user_name,pin):
        self.__user_name = user_name
        self.__pin = pin
        self.access = False

        f = open("balance.txt","r") 
        self.old_amount = f.readline()
        f.close()

    def check(self):
        if self.__user_name == "admin@852" and self.__pin == 2446:
            self.access = True
        return self.access

    def add(self,amount): 
        new_amount = int(self.old_amount) + amount

        with open("balance.txt","w") as f:
            f.write(str(new_amount))


#Access Files 
class Banking(Key):
    def __init__(self,account_no):
        super().__init__()
        self.access = False

        with open("balance.txt","r") as f:
            self.balance = f.read()

        with open("details.txt","r") as f:
            self.lines = f.readlines()
            for line in self.lines:
                name,account_number,amount,pin = line.strip().split("|")
                if account_no == account_number[-4:]:
                    self.access = True
                    self._name = name
                    self._account_number = account_number
                    self._amount = amount
                    self._pin = pin
                    self._dpin = self.fer.decrypt(pin.encode()).decode()
                    break
                    
        
class Deposit(Banking,Basic):
    def __init__(self,account_no,user_pin):
        super().__init__(account_no)
        self.user_pin = user_pin

        with open("balance.txt","r") as f:
            self.balance = f.read()
  
    def check(self):
        if self.access and self._dpin == self.user_pin:
                return True
        else:
            return False
    
    def deposit(self,amount):
        new_amount = int(self._amount) + int(amount)
        new_balance = int(self.balance) + int(amount)

        with open("details.txt","w") as f:
            for line in self.lines:
                name,account_number,amount,pin = line.strip().split("|")

                if self._account_number == account_number:
                    f.write(f"{self._name}|{self._account_number}|{str(new_amount)}|{self._pin}\n")
                else:
                    f.write(f"{name}|{account_number}|{amount}|{pin}\n")
        
        with open("balance.txt","w") as f:
            f.write(str(new_balance))

        
class Withdraw(Banking,Basic):
    def __init__(self,account_no,user_pin):
        super().__init__(account_no)
        self.user_pin = user_pin


    def check(self):
        if self.access and self._dpin == self.user_pin:
                return True
        else:
            return False

    def withdraw(self,amount):
        if amount < int(self.balance):
                if amount <= int(self._amount):
                    
                    new_amount = int(self._amount) - amount
                    new_balance = int(self.balance) - amount
                   
                    with open("details.txt","w") as f:
                        for line in self.lines:
                            name,account_number,amount,pin = line.strip().split("|")
                            if self._account_number == account_number:
                                f.write(f"{self._name}|{self._account_number}|{str(new_amount)}|{self._pin}\n")
                            else:
                                f.write(f"{name}|{account_number}|{amount}|{pin}\n")

                    with open("balance.txt","w") as f:
                        f.write(str(new_balance))


                else:
                    print("insufficient balance")
        else:
            print("insufficient amount at the moment")


class Balance(Banking,Basic):
    def __init__(self, account_no,user_pin):
        super().__init__(account_no)
        self.user_pin = user_pin

    def check(self):
        if self.access and self._dpin == self.user_pin:
                return True
        else:
            return False

    def view(self):
        user_details = {line.split("|")[1]:line.split("|")[2] for line in self.lines}

        for account_number,bal in user_details.items():
            if self._account_number == account_number:
                return bal



while True:
    print("Welcome".center(50))
    print("1.Create\n2.Deposite\n3.Withdraw\n4.Balance\n5.Admin\n6.Exit")
    user = int(input("Enter Here: "))
    
    if user == 6:
        break

    #Create New Account
    elif user == 1:
        print()
        name = input("Name: ")

        while True:
            pin = input("Create a pin: ")
            if not pin.isdigit() or len(pin) != 4:
                print("PIN must be 4 digits")
                continue
            else:
                break
            
        print("deposite limit 50000".title())
        while True:
            opening = input("Opening deposit: ")
            if int(opening) > 50000:
                print("amount passed the limit".title())
                continue
            else:
                break

        
        details = Details()
        acc = details.add(name,opening,pin)
        details.add_amount(opening)
        print()
        print("account added successfully".title())
        print()
        details.view(acc)

    #Deposit
    elif user == 2:

        print()
        acc_no = input("enter last 4 digit of your account number: ".title())
        pin = input("enter pin: ".title())

        deposit = Deposit(acc_no,pin)
        check = deposit.check()

        if check:
            print("deposite limit 50000".title())
            while True:
                new_amount = input("enter amount: ".title())
                if int(new_amount) > 50000:
                    print("amount passed the limit".title())
                    continue
                else:
                    deposit.deposit(new_amount)
                    break

        else:
            print("Invalid Input")

    #withdraw    
    elif user == 3:

        print()
        acc_no = input("enter last 4 digit of your account number: ".title())
        pin = input("enter pin: ".title())
        
        withdraw = Withdraw(acc_no,pin)
        check = withdraw.check()

        if check:
            print("withdraw limit 50000".title())
            while True:
                amount = int(input("enter amount: ".title()))
                if amount > 50000:
                    print("amount passed the limit".title())
                    continue
                else:
                    break
            withdraw.withdraw(amount)
        else:
            print("Invalid Input")

    #balance
    elif user == 4:
        
        print()
        acc_no = input("enter last 4 digit of your account number: ".title())
        pin = input("enter pin: ".title())

        balance = Balance(acc_no,pin)
        check = balance.check()

        if check:
            bal = balance.view()
            print(bal)
        else:
            print("Invalid input")

    #admin
    elif user == 5:
        print()
        admin = input("Enter Admin ID: ")
        pin = int(input("Enter pin: "))

        add_balance = Add_balance(admin,pin)
        check = add_balance.check()

        if check:
            amount = int(input("Enter Amount: "))
            add_balance.add(amount)
        else:
            print("Invalid Input")
    
    else:
        print("Invalid Input")