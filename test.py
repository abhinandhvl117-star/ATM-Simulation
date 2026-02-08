class  Train:
    def __init__(self):
        self.trains=[]
            
    def add(self,train):
        self.trains.append(train)
                            
    def view(self,user_from,user_to):
        for train in self.trains:
            if user_from in train[2] and user_to in train[3]:
                    train_no,train_name,From,to,seats,prize = train
                    print("TRAIN NUMBER :",train_no,
                        "|TRAIN NAME :",train_name,
                        "|FROM :",From,
                        "TO :",to,
                        "SEATS :",seats,
                        "PRIZE :",prize)
        
class Admin:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        
    
    def login(self):
        a=input("enter username :".title())
        b=input("enter password".title())
        
        if a==self.username and b==self.password:
            print("admin login successfull".title())
            return True
        else:
            print("invalid username or password")
            return False
    
    def add_train(self):
        temp = []
        train_no=input("enter train number :".title())
        temp.append(train_no)
        
        train_name=input("enter train name : ".title())
        temp.append(train_name)
        
        From=input("From :")
        temp.append(From)
        
        To=input("To :")
        temp.append(To)
        
        seats=int(input("enter total seats :").title())
        temp.append(seats)
        
        prize=int(input("enter ticket prize :").title())
        temp.append(prize)
        print('train added successfully'.title())
        return temp
        
        
class User(Train):
    def __init__(self):
        super().__init__()
        self.personal_info = {}

    def add_detail(self,name,number):
        self.personal_info = {name:train for train in self.trains if train[0] == number}
        print(self.personal_info)
        
        
            
    
admin = Admin("hg",4566)
user = User()

for i in range(3):
    x = admin.add_train()
    user.add(x)
    
# x = admin.add_train()
# user.add(x)
    
f = input("From: ")
t = input("To: ")
user.view(f,t)

name = input("Enter: ")
train_no = input("Enter train no: ")
user.add_detail(name,train_no)

print("yo")