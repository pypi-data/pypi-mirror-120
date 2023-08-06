from pass_addy.menu import Menu


def main():
    print("password manager game")
    menu = Menu()
    while not menu.exit:
        print("Welcome to the password Mangaer\n\n\n")
        print("1 for system check")
        print("2 for add Record")
        print("3 for view Records")
        print("4 for exit")
        print("5 for help")
        print("")
        val = menu.command_factory(input("Enter your command \n"))
        if val == 0:
            print("enter valid index")
        else:
            # handles the command
            menu.handle_command()


if __name__ == "__main__":
    """
    The main method that intialises the Menu class while is used to run program until user applies
    for exit co*mmand
    """
    main
