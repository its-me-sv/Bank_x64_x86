from os import path, makedirs, system, remove
from hashlib import sha512
from pickle import dump, load
from datetime import datetime
from stdiomask import getpass
from time import perf_counter
import requests

class InvalidOption(Exception):
    """This Exception Is Raised When The User
    Inputs Invalid Option."""
    pass

class UsernameAlreadyTaken(Exception):
    """This Exception Is Raised When The User
    Inputs Username Which Is Already In Use."""
    pass

class PhoneNumberAlreadyTaken(Exception):
    """This Exception Is Raised When The User
    Inputs Phone Number Which Is Already Taken."""
    pass

class InvalidUsername(Exception):
    """This Exception Is Raised When The User
    Inputs Incorrect Username."""
    pass

class InvalidPassword(Exception):
    """This Exception Is Raised When The User
    Inputs Incorrect Password."""
    pass

class InvalidPhoneNumber(Exception):
    """This Exception Is Raised When The User
    Inputs Invalid Phone Number."""
    pass

class InsufficientFunds(Exception):
    """This Exception Is Raised When The User
    Has Insufficient Amount To Make Transactions."""
    
class SameUser(Exception):
    """This Exception Is Raised When The User
    Inputs His Username To Transfer Money."""
    
class NoUserAvailable(Exception):
    """This Exception Is Raised When There
    Is No User Is Available To Recieve Money."""

def Initialise():
    if not path.exists("C:\\Projects\\Python\\Banking"):
        makedirs("C:\\Projects\\Python\\Banking")
    
    if not path.exists("C:\\Projects\\Python\\Banking\\usernames.svbk"):
        file = open("C:\\Projects\\Python\\Banking\\usernames.svbk", 'ab+')
        file.write(bytearray("USERNAMES\n", 'utf-8'))
        file.close()
        del file
        
    if not path.exists("C:\\Projects\\Python\\Banking\\passwords.svbk"):
        file = open("C:\\Projects\\Python\\Banking\\passwords.svbk", 'ab+')
        file.write(bytearray("PASSWORDS\n", 'utf-8'))
        file.close()
        del file
        
    if not path.exists("C:\\Projects\\Python\\Banking\\phone_no.svbk"):
        file = open("C:\\Projects\\Python\\Banking\\phone_no.svbk", 'ab+')
        file.write(bytearray("PHONE_NUMBERS\n", 'utf-8'))
        file.close()
        del file
        
def Encrypt(TEXT):
    duplicate = TEXT[::-1]
    duplicate = sha512(duplicate.encode('utf-8')).hexdigest()
    duplicate = sha512(duplicate[::2].encode('utf-8')).hexdigest()
    return duplicate[:]

class Passbook():
    def __init__(self):
       self.__transaction_no = int()
       self.__date_of_transaction = str()
       self.__type_of_transaction = str()
       self.__source = str()
       self.__amount = str()
       self.__balance_after_transaction = str()
   
    def Assign(self, TRANSACTION_NO, DATE_OF_TRANSACTION, TYPE_OF_TRANSACTION, SOURCE, AMOUNT, BALANCE_AFTER_TRANSACTION):
        self.__transaction_no = TRANSACTION_NO
        self.__date_of_transaction = DATE_OF_TRANSACTION
        self.__type_of_transaction = TYPE_OF_TRANSACTION
        self.__source = SOURCE
        self.__amount = AMOUNT
        self.__balance_after_transaction = BALANCE_AFTER_TRANSACTION
            
    def File_Write(self, USERNAME):
        file_name = "C:\\Projects\\Python\\Banking\\Passbook" + Encrypt(USERNAME) + ".txt"
        file = open(file_name, 'a+')
        text_to_write = "{} {}      {}      {}      {} Rs      {} Rs".format(self.__transaction_no, self.__date_of_transaction, self.__type_of_transaction,
                                         self.__source, self.__amount, self.__balance_after_transaction)
        file.write(text_to_write + '\n')
        file.close()
        del file, file_name, text_to_write

class Details():
    def __init__(self):
        self.__username = str()
        self.__password = str()
        self.__phone_no = str()
        
    def From_File_Username(self, USERNAME):
        found = False
        file = open("C:\\Projects\\Python\\Banking\\usernames.svbk", "rb")
        for line in file.readlines():
            if line.rstrip().decode() == Encrypt(USERNAME):
                found = True
                break
        file.close()
        del file
        return found
    
    def From_File_Password(self, PASSWORD):
        found = False
        file = open("C:\\Projects\\Python\\Banking\\passwords.svbk", "rb")
        for line in file.readlines():
            if line.rstrip().decode() == Encrypt(PASSWORD):
                found = True
                break
        file.close()
        del file
        return found
    
    def From_File_Phone_No(self, PHONE_NO):
        found = False
        file = open("C:\\Projects\\Python\\Banking\\phone_no.svbk", "rb")
        for line in file.readlines():
            if line.rstrip().decode() == Encrypt(PHONE_NO):
                found = True
                break
        file.close()
        del file
        return found
    
    def Assign(self, USERNAME, PASSWORD, PHONE_NO):
        self.__username = USERNAME
        self.__password = PASSWORD
        self.__phone_no = PHONE_NO
        
    def File_Write(self):
        file = open("C:\\Projects\\Python\\Banking\\usernames.svbk", "ab+")
        file.write(bytearray(Encrypt(self.__username) + '\n', 'utf-8'))
        file.close()
        del file
        
        file = open("C:\\Projects\\Python\\Banking\\passwords.svbk", "ab+")
        file.write(bytearray(Encrypt(self.__password) + '\n', 'utf-8'))
        file.close()
        del file
        
        file = open("C:\\Projects\\Python\\Banking\\phone_no.svbk", "ab+")
        file.write(bytearray(Encrypt(self.__phone_no) + '\n', 'utf-8'))
        file.close()
        del file
        
    def Modifying(self, value, option, old):
        if option == 1:
            file_name = "C:\\Projects\\Python\\Banking\\usernames.svbk"
        elif option == 2:
            file_name = "C:\\Projects\\Python\\Banking\\phone_no.svbk"
        elif option == 3:
            file_name = "C:\\Projects\\Python\\Banking\\passwords.svbk"
        file = open(file_name, 'rb')
        contents = list()
        for line in file.readlines():
            text_in_file = line.rstrip().decode()[:]
            if text_in_file == Encrypt(old):
                contents.append(Encrypt(value))
            else:
                contents.append(text_in_file)
        file.close()
        del file
        file = open(file_name, 'wb')
        for lines in contents:
            file.write(bytearray(lines + '\n', 'utf-8'))
        file.close()
        del file, file_name
          
class User():
    def __init__(self):
        self.__name = str()
        self.__phone_no = str()
        self.__username = str()
        self.__password = str()
        self.__balance = int()
        self.__transactions = int()
        self.__acc_creation_date = str()
        
    def Assign(self, NAME, PHONE_NO, USERNAME, PASSWORD, BALANCE, TRANSACTIONS, ACCOUNT_CREATION_DATE):
        self.__name = NAME
        self.__phone_no = PHONE_NO
        self.__username = USERNAME
        self.__password = PASSWORD
        self.__balance = BALANCE
        self.__transactions = TRANSACTIONS
        self.__acc_creation_date = ACCOUNT_CREATION_DATE
        
    def File_Write(self):
        file_name = "C:\\Projects\\Python\\Banking\\" + Encrypt(self.__username) + ".bku"
        file = open(file_name, 'wb')
        dump(self, file)
        file.close()
        del file
       
    def Show_Details(self):
        print("Name : {}".format(self.__name))
        print("Username : {}".format(self.__username))
        print("Member Since : {}".format(self.__acc_creation_date))
        print("Transactions Made : {}".format(self.__transactions))
        print("*" * 14)
        print()
        
    def Show_Modifiable(self):
        print()
        print("[1]. Name : {}".format(self.__name))
        print("[2]. Username : {}".format(self.__username))
        print("[3]. Phone Number : {}".format(self.__phone_no))
        print("[4]. Password : {}".format(self.__password))
        print("[5]. EXIT")
        
    def Modify(self, value, option):
        if option == 1:
            self.__name = value
        elif option == 2:
            self.__username = value
        elif option == 3:
            self.__phone_no = value
        elif option == 4:
            self.__password = value
        elif option == 5:
            self.__balance = value
        elif option == 6:
            self.__transactions = value
            
    def Ret_Value(self, option):
        if option == 1:
            return self.__username
        elif option == 2:
            return self.__phone_no
        elif option == 3:
            return self.__password
        elif option == 4:
            return self.__balance
        elif option == 5:
            return self.__transactions
        elif option == 6:
            return self.__name
        
def Send_Message(option, name, amount, current_balance, number, name2 = ""):
    if option == 1:
        msg_to_send = "Dear {},\n{} Rs Has Been Deposited To Your Account.\n Your Current Account Balance Is {} Rs".format(name, amount, current_balance)
    elif option == 2:
        msg_to_send = "Dear {},\n{} Rs Has Been Withdrawn From Your Account.\n Your Current Account Balance Is {} Rs".format(name, amount, current_balance)
    elif option == 3:
        msg_to_send = "Dear {},\n{} Rs Has Been Transferred From Your Account.\n Your Current Account Balance Is {} Rs".format(name, amount, current_balance)
    elif option == 4:
        msg_to_send = "Dear {},\n{} Rs Has Been Transfered To {} From Your Account.\n Your Current Account Balance Is : {} Rs".format(name, amount, name2, current_balance)
    elif option == 5:
        msg_to_send = "Dear {},\n{} Rs Has Been Recieved From {}.\n Your Current Account Balance Is : {} Rs".format(name, amount, name2, current_balance)
    elif option == 6:
        msg_to_send = "Dear {},\n Thank You For Creating An Account In Our Bank.\nYour Account Balance Is : {} Rs.\nYou Can Add Money To Your Balance Using Our Payment Methods.\n \nRegards,\nSuraj Vijay".format(name, current_balance)           
    try:
        url = "https://www.fast2sms.com/dev/bulk"
        
        querystring = {
            "authorization":"GET YOUR API KEY FROM fast2sms",
            "sender_id":"FSTSMS",
            "message":msg_to_send,
            "language":"english",
            "route":"p",
            "numbers":number}
        
        headers = {
            'cache-control': "no-cache"
        }
        
        response = requests.request("GET", url, headers=headers, params=querystring)
    except:
        pass
    finally:
        print()
        
def Change_Name(obj):
    name = input("Enter The Name To Replace With : ")
    obj.Modify(name[:], 1)
    obj.File_Write()
    del name

def Change_Username(obj):
    while True:
        try:
            system("cls")
            obj1 = Details()
            new_username = input("Enter Username To Replace With : ")
            if obj1.From_File_Username(new_username):
                raise UsernameAlreadyTaken
        except UsernameAlreadyTaken:
            input("The Username Is Already In Use")
        else:
            break
    obj1.Modifying(new_username, 1, obj.Ret_Value(1))
    remove("C:\\Projects\\Python\\Banking\\" + Encrypt(obj.Ret_Value(1)) + ".bku")
    del obj1
    obj.Modify(new_username, 2)
    obj.File_Write()
    return Encrypt(new_username[:])

def Change_Phone_No(obj):
    while True:
        try:
            system("cls")
            obj1 = Details()
            new_username = input("Enter Phone Number To Replace With : ")
            if obj1.From_File_Phone_No(new_username):
                raise UsernameAlreadyTaken
        except UsernameAlreadyTaken:
            input("The Phone Number Is Already In Use")
        else:
            break
    obj1.Modifying(new_username[:], 2, obj.Ret_Value(2))
    del obj1
    obj.Modify(new_username[:], 3)
    obj.File_Write()
    
def Change_Password(obj):
    system("cls")
    obj1 = Details()
    new_username = input("Enter Password To Replace With : ")
    obj1.Modifying(new_username[:], 3, obj.Ret_Value(3))
    del obj1
    obj.Modify(new_username[:], 4)
    obj.File_Write()

def Settings(username):
    while True:
        while True:
            try:
                system("cls")
                print("Settings")
                menu = "12345"
                file_name = "C:\\Projects\\Python\\Banking\\" + username + ".bku"
                file = open(file_name, 'rb')
                obj = load(file)
                obj.Show_Modifiable()
                del file_name, file
                choice = input("Enter Utility Number To Change : ")
                if choice not in menu:
                    raise InvalidOption
            except InvalidOption:
                input("Invalid Option")
            else:
                break
        system("cls")    
        if choice == "1":
            Change_Name(obj)
        elif choice == "2":
            username = Change_Username(obj)
        elif choice == "3":
            Change_Phone_No(obj)
        elif choice == "4":
            Change_Password(obj)
        elif choice == "5":
            print()
            input("PRESS ANY KEY TO RETURN TO THE MENU ........")
            break
        if choice != "5":
            print()
            input("Data Has Been Modified Successfully")
    del obj
    return username

def Create_Account():
    while True:
        system("cls")
        print("Create Account")
        print("Fill In The Details Below : ")
        name = input("Name : ")
        obj = Details()
        while True:
            while True:
                try:
                    system("cls")
                    print("Create Account")
                    print("Fill In The Details Below : ")
                    print("Name : {}".format(name))
                    username = input("Username : ")
                    if obj.From_File_Username(username):
                        raise UsernameAlreadyTaken
                    password = input("Password : ")
                    phone_no = input("Phone Number : ")
                    digits = "1234567890"
                    for no in phone_no:
                        if no not in digits:
                            raise InvalidPhoneNumber
                    if obj.From_File_Phone_No(phone_no):
                        raise PhoneNumberAlreadyTaken
                except UsernameAlreadyTaken:
                    print("The Username Is Already In Use.")
                    input()
                except PhoneNumberAlreadyTaken:
                    print("The Phone Number Is Already In Use.")
                    input()
                except InvalidPhoneNumber:
                    print("The Phone Number Is Invalid")
                    input()
                else:
                    break
            obj.Assign(username, password, phone_no)
            obj.File_Write()
            del obj
            break
        obj1 = User()
        d = datetime.now()
        obj1.Assign(name, phone_no, username, password, 0, 0, d.strftime("%A %B %d, %I:%M %p, %Y"))
        obj1.File_Write()
        break
    Send_Message(6, obj1.Ret_Value(6), 0, obj1.Ret_Value(4), obj1.Ret_Value(2))
    del obj1
    print("Account Has Been Created Successfully")
    input()
        
def Authentication(username, password):
    check1 = 0 
    """Check For Username"""
    found1 = False
    check2 = 0 
    """Check For Password"""
    found2 = False
    check3 = 0 
    """Check For Phone Number"""
    found3 = False
    
    file = open("C:\\Projects\\Python\\Banking\\usernames.svbk", "rb")
    for line in file.readlines():
        check1 += 1
        if line.rstrip().decode() == username:
            found1 = True
            break
    file.close()
    del file
    
    if not found1:
        file = open("C:\\Projects\\Python\\Banking\\phone_no.svbk", "rb")
        for line in file.readlines():
            check2 += 1
            if line.rstrip().decode() == username:
                found2 = True
                break
        file.close()
        del file
    
    if not found1:
        check1 = 0
        if not found2:
            return 100 # No Such Username Or Phone Number
    
    file = open("C:\\Projects\\Python\\Banking\\passwords.svbk", "rb")
    for line in file.readlines():
        check3 += 1
        if line.rstrip().decode() == password:
            found3 = True
            break
    file.close()
    del file
    
    if found3:
        if check1 == check3:
            return 300 # Correct Password
        elif check2 == check3:
            return 400 # Correct Password
        else:
            return 200 # Incorrect Password
    else:
        return 200 # Incorrecnt Password

def Retrieve_Username(username):
    file = open("C:\\Projects\\Python\\Banking\\phone_no.svbk", 'rb')
    pos = 0
    for line in file.readlines():
        pos +=1
        if line.rstrip().decode() == Encrypt(username):
            break
    file.close()
    del file

    file = open("C:\\Projects\\Python\\Banking\\usernames.svbk", 'rb')
    pos1 = 0
    for line in file.readlines():
        pos1 += 1
        if pos1 == pos:
            return line.rstrip().decode()

def Duration_Of_Using(Start, End):
    m, s = divmod(int(round(End - Start, 0)), 60)
    h, m = divmod(m, 60)
    return "{}:{}:{}".format(h, m, s)
    
def Account_Holders_Details(username):
    system("cls")
    print("All Account Holders")
    print()
    
    file1 = open("C:\\Projects\\Python\\Banking\\usernames.svbk", 'rb')
    
    for line in file1.readlines():
        user_in_file = line.rstrip().decode()[:]
        if user_in_file != "USERNAMES":
            location = "C:\\Projects\\Python\\Banking\\" + user_in_file + ".bku"
            file2 = open(location, 'rb')
            obj = load(file2)
            file2.close()
            obj.Show_Details()
            del file2, obj, location
        del user_in_file
        
    print()
    print()
    input("Press Any Key To Return To The Main Menu ..............")

def View_Passbook(username):
    system("cls")
    print("Passbook")
    print()
    print("[Transaction Number - Transaction Date - Transaction Type - Money Source - Amount - Balance]")
    print()
    location = "C:\\Projects\\Python\\Banking\\Passbook" + username + ".txt"
    if not path.exists(location):
        print("No Transactions Have Been Made Yet")
    else:
        file = open(location)
        for line in file.readlines():
            print(line.rstrip())
        file.close()
        del file
    
    del location
    
    print()
    print()
    input("Press Any Key To Return To The Main Menu ..............")

def Deposit_Money(obj):
    current_balance = obj.Ret_Value(4)
    current_transactions = obj.Ret_Value(5)
    while True:
        try:
            system("cls")
            print("Your Account Balance : {} Rs".format(current_balance))
            amount = input("Enter Amount(Rs) To Deposit : ")
            new_amount = ""
            for d in amount:
                if d != ",":
                    new_amount += d
            amount = float(new_amount[:])
            if amount < 0:
                raise ValueError
        except ValueError:
            input("Invalid Input")
        else:
            break
    current_balance += amount
    current_transactions += 1
    print("{} Rs Has Been Added To Your Account Balance".format(amount))
    print()
    print("Your Current Account Balance : {} Rs".format(current_balance))
    obj.Modify(current_balance, 5)
    obj.Modify(current_transactions, 6)
    obj.File_Write()
    
    obj2 = Passbook()
    d = datetime.now()
    obj2.Assign(current_transactions, d.strftime("%A %B %d, %I:%M %p, %Y"), "Deposition", "Local ATM / BANK", amount, current_balance)
    obj2.File_Write(obj.Ret_Value(1))
    del obj2
    print()
    Send_Message(1, obj.Ret_Value(6)[:], amount, current_balance, obj.Ret_Value(2)[:])
    input("PRESS ANY KEY TO RETURN TO THE PAYMENTS MENU ............")

def Withdraw_Money(obj):
    current_balance = obj.Ret_Value(4)
    current_transactions = obj.Ret_Value(5)
    while True:
        try:
            system("cls")
            print("Your Account Balance : {} Rs".format(current_balance))
            amount = input("Enter Amount(Rs) To Deposit : ")
            new_amount = ""
            for d in amount:
                if d != ",":
                    new_amount += d
            amount = float(new_amount[:])
            if amount < 0:
                raise ValueError
            if amount > current_balance:
                raise InsufficientFunds
        except ValueError:
            input("Invalid Input")
        except InsufficientFunds:
            input("You Have Insufficient Amount To Withdraw")
        else:
            break
    current_balance -= amount
    current_transactions += 1
    print("{} Rs Has Been Subtracted From Your Account Balance".format(amount))
    print()
    print("Your Current Account Balance : {} Rs".format(current_balance))
    obj.Modify(current_balance, 5)
    obj.Modify(current_transactions, 6)
    obj.File_Write()
    
    obj2 = Passbook()
    d = datetime.now()
    obj2.Assign(current_transactions, d.strftime("%A %B %d, %I:%M %p, %Y"), "Withdrawn", "Local ATM / BANK", amount, current_balance)
    obj2.File_Write(obj.Ret_Value(1))
    del obj2
    print()
    Send_Message(2, obj.Ret_Value(6)[:], amount, current_balance, obj.Ret_Value(2)[:])
    input("PRESS ANY KEY TO RETURN TO THE PAYMENTS MENU ..............")

def Available_Users():
    avail_users = list()
    file1 = open("C:\\Projects\\Python\\Banking\\usernames.svbk", 'rb')
    for line in file1.readlines():
        user_in_file = line.rstrip().decode()[:]
        if user_in_file != "USERNAMES":
            location = "C:\\Projects\\Python\\Banking\\" + user_in_file + ".bku"
            file2 = open(location, 'rb')
            obj = load(file2)
            file2.close()
            avail_users.append(obj.Ret_Value(1))
            del file2, obj, location
        del user_in_file
        
    return avail_users[:]

def Transfer_Money(obj):
    avail_users = Available_Users()
    
    if obj.Ret_Value(1) in avail_users:
        avail_users.remove(obj.Ret_Value(1))
    
    sender_balance = obj.Ret_Value(4)
    sender_transactions = obj.Ret_Value(5)
    
    try:
        if not len(avail_users):
            raise NoUserAvailable
    except NoUserAvailable:
        input("Currently There Are No Users To Recieve Money")
        return 0
    else:
        pass
    finally:
        print()
    
    while True:
        try:
            system("cls")
            print("Transfer Money")
            print()
            for u in avail_users:
                print(u)
            print()
            reciever = input("Enter Username From The Above List : ")
            if reciever == obj.Ret_Value(1):
                raise SameUser
            if reciever not in avail_users:
                raise InvalidUsername
        except SameUser:
            input("You Can't Transfer Money To Yourself")
        except InvalidUsername:
            input("No Such User Is Available")
        else:
            break
        
    reciever_location = "C:\\Projects\\Python\\Banking\\" + Encrypt(reciever) + ".bku"
    reciever_file = open(reciever_location, 'rb')
    obj2 = load(reciever_file)
    reciever_file.close()
    reciever_balance = obj2.Ret_Value(4)
    reciever_transactions = obj2.Ret_Value(5)
    
    while True:
        try:
            system("cls")
            print("Enter Username From The Above List : {}".format(reciever))
            print()
            print("Your Current Account Balance : {} Rs".format(sender_balance))
            print()
            amount = input("Enter Amount To Transfer : ")
            new_amount = ""
            for d in amount:
                if d != ",":
                    new_amount += d
            amount = float(new_amount[:])
            if amount < 0:
                raise ValueError
            if amount > sender_balance:
                raise InsufficientFunds
        except InsufficientFunds:
            input("You Have Insufficient Money To Transfer")
        except ValueError:
            input("Invalid Input")
        else:
            break
        
    sender_balance -= amount
    sender_transactions += 1
    print("{} Rs Has Been Subtracted From Your Account Balance".format(amount))
    print()
    print("Your Current Account Balance : {} Rs".format(sender_balance))
    obj.Modify(sender_balance, 5)
    obj.Modify(sender_transactions, 6)
    obj.File_Write()
    obj3 = Passbook()
    d = datetime.now()
    obj3.Assign(sender_transactions, d.strftime("%A %B %d, %I:%M %p, %Y"), "Online Transfer - Sender", "Online", amount, sender_balance)
    obj3.File_Write(obj.Ret_Value(1))
    del obj3
    print()
    Send_Message(4, obj.Ret_Value(6)[:], amount, sender_balance, obj.Ret_Value(2)[:], obj2.Ret_Value(1))
    
    reciever_balance += amount
    reciever_transactions += 1
    obj2.Modify(reciever_balance, 5)
    obj2.Modify(reciever_transactions, 6)
    obj2.File_Write()
    obj4 = Passbook()
    obj4.Assign(reciever_transactions, d.strftime("%A %B %d, %I:%M %p, %Y"), "Online Transfer - Reciever", "Online", amount, reciever_balance)
    obj4.File_Write(obj2.Ret_Value(1))
    del obj4
    Send_Message(5, obj2.Ret_Value(6)[:], amount, reciever_balance, obj2.Ret_Value(2)[:], obj.Ret_Value(1))
    
    input("PRESS ANY KEY TO RETURN TO PAYMENTS MENU")
    return 1

def Payments(obj):
    while True:
        while True:
            try:
                system("cls")
                print("Payments")
                print("[1]. Deposit")
                print("[2]. Withdraw")
                print("[3]. Transfer")
                print("[4]. EXIT")
                choice = input("Enter Your Choice : ")
                if choice not in "1234":
                    raise InvalidOption
            except InvalidOption:
                input("Invalid Option")
            else:
                break
        if choice == "1":
            Deposit_Money(obj)
        elif choice == "2":
            Withdraw_Money(obj)
        elif choice == "3":
            k = Transfer_Money(obj)
        elif choice == "4":
            print()
            input("PRESS ANY KEY TO EXIT TO THE MAIN MENU ...............")
            break

def After_Log_In(username, value):
    Start = perf_counter()
    if value == 400:
        username = Retrieve_Username(username)[:]
    else:
        username = Encrypt(username)[:]
    while True:
        while True:
            try:
                system("cls")
                location = "C:\\Projects\\Python\\Banking\\" + username + ".bku"
                file = open(location, 'rb')
                obj = load(file)
                file.close()
                del file, location
                print("{} Menu".format("\t\t\t\t\t\t"))
                print("[1]. Settings")
                print("[2]. Account Holders")
                print("[3]. Payments")
                print("[4]. Passbook")
                print("[5]. LOG OUT")
                choice_at_menu = input("Enter Your Choice : ")
                
                if choice_at_menu not in "12345":
                    raise InvalidOption
            except:
                print("Invalid Option")
                input()
            else:
                break
        system("cls")
        print("{}".format("\t\t\t\t\t\t\t"), end = "")
        if choice_at_menu == "1":
            username = Settings(username[:])
        elif choice_at_menu == "2":
            Account_Holders_Details(username[:])
        elif choice_at_menu == "3":
            Payments(obj)
        elif choice_at_menu == "4":
            View_Passbook(username[:])
        elif choice_at_menu == "5":
            print("Logged Out Successfully")
            print()
            break
    del obj    
    End = perf_counter()
    print("Session Time [H:M:S] : {}".format(Duration_Of_Using(Start, End)))

def Login_To_Account():
    chance = 0
    
    while True:
        if chance > 2:
            break
        
        try:
            system("cls")
            print("Login")
            username = input("Username/Phone Number : ")
            password = getpass(mask = "•")
            value = Authentication(Encrypt(username), Encrypt(password))
            
            if value == 100:
                raise InvalidUsername
            
            elif value == 200:
                raise InvalidPassword
        
        except InvalidUsername:
            print("The Username Or Phone Number Is Incorrect")
            chance += 1
            input()
        
        except InvalidPassword:
            print("The Password Is Incorrect")
            chance += 1
            input()
        
        else:
            if value > 200:
                chance = 4
    
    if chance == 4:
        print("Login Successfull")
        input()
        After_Log_In(username[:], value)
    else:
        print("Try Again After A While")
    
    input()

def Main_Function():
    while True:
        while True:
            try:
                system("cls")
                print("Project Name : Banking Project")
                print("Standalone Executable Name : bank.exe")
                print("Project Author : Suraj Vijay")
                print("*" * 37)
                print()
                menu = "123"
                print("{} Welcome To Bank".format("\t\t\t\t\t\t"))
                print("[1]. Create Account")
                print("[2]. Login")
                print("[3]. EXIT")
                choice_at_menu = input("Enter Your Choice : ")
                
                if choice_at_menu not in menu:
                    raise InvalidOption
            except:
                print("Invalid Option")
                input()
            else:
                break
        
        if choice_at_menu == '1':
            Create_Account()
        
        elif choice_at_menu == '2':
            Login_To_Account()
        
        elif choice_at_menu == '3':
            system("cls")
            print("Thank You For Using Our Services")
            print()
            print()
            input("PRESS ANY KEY TO EXIT .......")
            system("cls")
            break

if __name__ == "__main__":
    system("cls")
    Initialise()
    Main_Function()
