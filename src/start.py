import main, settings

# Import the modules needed to run the script.
import sys, os

# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu

def main_menu():
    os.system('cls')

    print "Welcome,\n"
    print "Please choose the menu you want to start:"
    print "1. Start"
    print "0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice, {
        'main_menu': main_menu,
        '1': menu_enter_name,
        '0': exit,
    })

    return

# Execute menu
def exec_menu(choice, action):
    os.system('cls')
    ch = choice.lower()
    if ch == '':
        return
    else:
        try:
            action[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            action[ch]()
    return

# Menu Name
def menu_enter_name():
    default = settings.file_name
    default_str = default and ('['+ default +']') or ''

    name = raw_input("Enter File's name " + default_str + ": ")
    main.set_file_name(name or default)

    main.create_folder(settings.path + '/' + settings.file_name)

    menu_enter_index()

# Menu Index
def menu_enter_index():
    default = main.get_last_index_from_folder(settings.path + '/' + settings.file_name)
    default_str = ('['+ str(default) +']') or ''

    index = raw_input("Enter File's index " + default_str + " : ")
    main.set_file_index(index and int(index) or default)

    menu_record_preparing()

# Menu Record Decision
def menu_record_preparing():
    os.system('cls')

    print "Record Menu,\n"
    print "Please choose the menu you want to start:"
    print "1. Start record '" + settings.path + '/' + settings.file_name + '/' + str(settings.file_index) + ".txt'"
    print "2. Edit Name & Index"
    print "\n0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice, {
        '1': menu_start_record,
        '2': menu_enter_name,
        '0': exit,
    })

    return

# Menu Start Record
def menu_start_record():
    # TODO: Start Recording Menu
    return

# Back to main menu
def back():
    menu_actions['main_menu']()

# Exit program
def exit():
    main.exit()
    sys.exit()


# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    settings.init()
    # Launch main menu
    main_menu()
