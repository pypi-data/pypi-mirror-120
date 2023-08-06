import time

# Class Menu that handles each and everything it is destined to


class Menu:
    def __init__(self):
        self.system_check = False
        self.add_record = False
        self.view_record = False
        self.exit = False
        self.help = False

    # setting the variable based upon the command given
    def command_factory(self, num):
        print(num)
        if num == "1":
            self.system_check = True
        elif num == "2":
            self.add_record = True
        elif num == "3":
            self.view_record = True
        elif num == "4":
            print("exiting ")
            print("." * 10)
            time.sleep(2)
            self.exit = True
        elif num == "5":
            self.help = True
        else:
            return 0
        return 1

    # command is handled as per the request
    def handle_command(self):
        if self.system_check:
            checkDb()
            self.system_check = False
        elif self.add_record:
            add_record()
            self.add_record = False
        elif self.view_record:
            view_record()
            self.view_record = False
        elif self.exit:
            pass
        elif self.help:
            help()
            self.help = False
        else:
            print("Not a valid command")


# checks if database exist or not if not creates a new file
def checkDb():
    print("checking database if exits")
    print("Loading")
    time.sleep(2)
    try:
        open("database.txt", "r")
        print("\n \n file exits")
    except Exception:
        open("database.txt", "x")
        print("\n \n file created")


# adding the record in database file
def add_record():
    print("Adding the record >> ")
    print("Loading")
    username = input("Enter the username\n")
    password = input("Enter the password\n")
    url = input("Enter the url\n")
    file = open("database.txt", "a")
    file.writelines("username: " + username + ", password:" + password + ", url:" + url)
    file.close()
    print("Record Added for ", username)


# printing the records inside the database file
def view_record():
    print("Viewing the Record")
    print("Loading")
    file = open("database.txt", "r")
    Lines = file.readlines()
    if len(Lines) == 0:
        print("\n\n*****************No records found********\n\n\n")
    else:
        count = 0
        print("\n\n*****************Records found********\n\n\n")
        for line in Lines:
            count += 1
            print("Record{}: {}".format(count, line.strip()))
    file.close()
    print("exiting. .. \n\n\n\n")
    time.sleep(3)


# calling the help method
def help():
    print("When the program runs enter the command and do accordingly")
