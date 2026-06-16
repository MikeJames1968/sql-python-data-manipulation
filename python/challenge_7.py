# initialise empy menu list

menu = []

# print menu function

def print_menu(menu):
    for index, menuopt in enumerate(menu):
        print(f"{index+1} - {menuopt}")


# loop until quit selected

quit_not_selected = True
while quit_not_selected:

    # display menu options

    print("===============SIMPLE CLI MENU===============")
    print("Type 1 to add an item")
    print("Type 2 to remove an item")
    print("Type 3 to list all menu items")
    print("Type 4 to quit")

    # loop until a valid choice enetered

    invalid_option = True
    while invalid_option:
        option = input("Choose an option: ")
        if option not in ("1", "2", "3", "4"):
            print(f"{option} is not a valid option. Enter 1-4")
        else:
            invalid_option = False

    # process option

    match option:
        case "1":
            new_item = input("Enter a new menu item: ")
            menu.append(new_item)
            print(f"{new_item} added to menu at position {len(menu)}")
            print("New menu:")
            print_menu(menu)

        case "2":
            while True:
                raw = input("Enter the position of the option to remove: ")
                try:
                    del_item = int(raw)
                    break
                except ValueError:
                    print(f"'{raw}' is not a valid number. Enter a positive integer.")
            if del_item < 1 or del_item > len(menu):
                print(f"Menu option {del_item} does not exist")
            else:
                removed = menu.pop(del_item-1)
                print(f"Menu option '{removed}' removed")
                print("New menu:")
                print_menu(menu)
        case "3":
            print("Current Menu:")
            print_menu(menu)
        case "4":
            quit_not_selected = False
