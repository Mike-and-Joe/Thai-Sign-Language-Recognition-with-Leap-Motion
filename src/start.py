import main, settings, utils

# Import the modules needed to run the script.
import sys, os, time

# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu

def main_menu():
    clear_screen()

    print "Welcome,\n"
    print "Please choose the menu you want to start:"
    print "1. Start"
    print "\n0. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice, {
        '1': menu_enter_name,
        '0': exit,
    })

    return

# Execute menu
def exec_menu(choice, action):
    ch = choice.lower()
    if ch == '':
        main_menu()
    else:
        try:
            action[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            main_menu()
    return

# Menu Name
def menu_enter_name():
    clear_screen()

    default = settings.file_name
    default_str = default and ('['+ default +']') or ''

    name = raw_input("Enter File's name " + default_str + ": >>")
    main.set_file_name(name or default)

    utils.create_folder(settings.path + '/' + settings.file_name)

    menu_enter_index()

# Menu Index
def menu_enter_index():
    default = int(utils.get_last_index_from_folder(settings.path + '/' + settings.file_name)) + 1
    default_str = ('['+ str(default) +']') or ''

    index = raw_input("Enter File's index " + default_str + " : >> ")
    main.set_file_index(index and int(index) or default)

    menu_record_preparing()

# Menu Record Decision
def menu_record_preparing():
    clear_screen()

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
    clear_screen()

    print "Recording.....,\n"
    print "Files : '" + settings.path + '/' + settings.file_name + '/' + str(settings.file_index) + "'"
    choice = raw_input(" Start ? ")

    main.start_record()
    start_record = time.time()

    choice = raw_input(" Stop ! ")

    print '\nTotal time : ' + str(time.time() - start_record)
    main.stop_record()

    print "\nNext index,\n"
    menu_enter_index()

    return

# Exit program
def exit():
    main.exit()
    sys.exit()

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    # pass

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Initialized Settings
    settings.init()
    # Initialized Cameras
    main.init()
    # Launch main menu
    main_menu()
