import json
import random
import string 
from pathlib import Path


class Bank:
    database='data.json'
    data=[]

    try:
        if Path(database).exists():
            with open(database)as fs:
                data=json.loads(fs.read())
        else:
            print("no such file exist")
    except Exception as err:
        print(f"an exception occured as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database,'w')as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerate(cls):
        alpha=random.choices(string.ascii_uppercase,k=3)
        num=random.choices(string.digits,k=3)
        spchar=random.choices("!@#$%^&*",k=1)
        id=alpha+num+spchar
        random.shuffle(id)
        return "".join(id)
     

        
    def createaccount(self):
        info={
            "name":input("tell your name:"),
            "age":int(input("tell your age:")),
            "email":input("tell your email:"),
            "pin":int(input("tell your 4 number pin:")),
            "accountNo." :Bank.__accountgenerate(),
            "balance": 0
        }
        if info['age']<18 or len(str(info['pin']))!=4:
            print("sorry you are not eligible to create an account")
        else:
            print("your account has been created successfully") 
            for i in info:
                print(f"{i}: {info[i]}") 
            print("please note down your accountnumber")

            Bank.data.append(info)

            Bank.__update()

        def depositmoney(self):
            accnumber=input("please tell your account number:")
            pin=int(input("please tell your pin:"))

            userdata=[i for i in Bank.data if i['accountNo.']==accnumber and i['pin']==pin]

            if userdata==False:
                print("sorry your account number or pin is incorrect")

            else:
                amount=int(input("please tell the amount you want to deposit:"))
                if amount > 10000 or amount <0 :
                    print("sorry the amount is too much you can deposit below 10000 or above 0")
                
                else: 
                   
                    userdata[0]['balance']+=amount
                    Bank.__update()
                    print("your amount has been deposited successfully")


        def withdrawmoney(self):
            accnumber=input("please tell your account number:")
            pin=int(input("please tell your pin:"))
        
            userdata=[i for i in Bank.data if i['accountNo.']==accnumber and i['pin']==pin]
        
            if userdata==False:
                    print("sorry your account number or pin is incorrect")
        
            else:
                    amount=int(input("please tell the amount you want to withdraw:"))
                    if userdata[0]['balance'] <  amount:
                         print("sorry you dont have sufficient balance to withdraw the amount")
                        
                    else: 
                       
                        userdata[0]['balance'] -= amount
                        Bank.__update()
                        print("your amount has been withdraw successfully")
                                                                                                              
        def showdetails(self):     

            accnumber=input("please tell your account nmber:")
            pin=int(input("please tell your pin:"))

            userdata=[i for i in Bank.data if i['accountNo.']==accnumber and i['pin']==pin]
            print(" your information are\n\n\n")
            for i in userdata:
                print(f"{i}: {userdata[0][i]}")



        def updatedetais(self):
            accnumber = input("please tell your account number:")
            pin = int(input("please tell your pin:"))

            userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

            if userdata == False:
                print("no such user found")

            else:
                print("you cannot change your age , accoun number and balance  but you can change your name, email and pin")

                print("Fill the details to change the data or leave it empty if you dont want to chaange it")

                newdata={
                    "name":input("please tell your name or press enter to skip" ),
                    "email":input("please tell your email or press enter to skip"),
                     "pin":input("please tell your pin or press enter to skip")
                     }

                if newdata["name"] == "":
                    newdata["name"] = userdata[0]["name"]
                if newdata["email"] == "":
                    newdata["email"] = userdata[0]["email"]
                if newdata["pin"] == "":
                    newdata["pin"] = userdata[0]["pin"]

                newdata["age"] = userdata[0]["age"]

                newdata["accountNo."] = userdata[0]["accountNo."]
                newdata["balance"] = userdata[0]["balance"]

                if type(newdata["pin"]) == str:
                    newdata["pin"] = int(newdata["pin"])


                for i in newdata:
                    if newdata[i] == userdata[0][i]:   
                        continue
                    else:
                        userdata[0][i] = newdata[i]

                Bank.__update()
                print("your data has been updated successfully")

        
        def deleteaccount(self):
            accnumber = input ("please tell your account number:")
            pin = int(input("please tell your pin:"))

            userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

            if userdata == False:
                print("no such data exists")
            else:
                check = input("are you sure you want to delete your account? press y for yes and n for no:")
                if check == "n" or check == "N":
                    print("your account has not been deleted")
                else:
                    index = Bank.data.index(userdata[0])
                    Bank.data.pop(index)
                    print("account has been deleted successfully")
                    Bank.__update()



user = Bank()
print("press 1 for creating an account")   
print("press 2 for depositing the money in the bank")
print("press 3 for withdrawing the money from the bank")
print("press 4 for details of the account")
print("press 5 for updating the data")
print("press 6 for deleting the account")

check = int(input("tell me your response:"))

if check == 1:
    user.createaccount()

if check == 2:
    user.depositmoney()

if check == 3:
    user.withdrawmoney()


if check == 4:
    user.showdetails()

if check == 5:
    user.updateaccount()

if check == 6:
    user.deleteaccount()

