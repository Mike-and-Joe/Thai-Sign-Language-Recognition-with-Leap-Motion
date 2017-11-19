# Import the modules needed to run the script.
import sys, os, time, threading, cv2, json

# Import helper modules
import main, settings, utils
from predict import features

# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu

def main_menu():
    clear_screen()

    print "Welcome,\n"
    print "Please choose the menu you want to start:"
    print "1. Start"
    print "\nq. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice, {
        '1': menu_enter_name,
        'q': exit,
    })

    return

# Execute menu
def exec_menu(choice, action):
    ch = choice.lower()
    if ch == 'm':
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
    main.set_settings('file_name', name or default)

    utils.create_folder(settings.path + '/' + settings.file_name)

    menu_enter_index()

# Menu Index
def menu_enter_index():
    default = int(utils.get_last_index_from_folder(settings.path + '/' + settings.file_name)) + 1
    default_str = ('['+ str(default) +']') or ''

    index = default

    index_raw = raw_input("Enter File's index " + default_str + " : >> ")

    if (index_raw == 'q') :
        exit()
        return
    elif (index_raw != '') :
        index = int(index_raw)

    main.set_settings('file_index', index)

    menu_record_preparing()

# Menu Record Decision
def menu_record_preparing():
    clear_screen()

    print "Record Menu,\n"
    print "Please choose the menu you want to start:"
    print "(Enter) Start record '" + settings.path + '/' + settings.file_name + '/' + str(settings.file_index) + "'"
    print "(2) Edit Name & Index"
    print "\nq. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice, {
        '': menu_start_record,
        '2': menu_enter_name,
        'q': exit,
    })

    return

def menu_show_ready_list () :
    clear_screen()
    print 'Device ready list (Waiting for all true) : '
    for key, value in settings.is_ready.iteritems() :
        print key, value

def is_device_on () :
    while (True) :
        if main.is_all_ready() :
            break
        time.sleep(0.100)
        menu_show_ready_list()

# Menu Start Record
def menu_start_record():
    is_device_on()

    t = threading.Thread(name='menu_show_starting', target=menu_show_starting)
    t.start()

    choice = raw_input()
    main.start_record()
    start_record_time = time.time()

    t = threading.Thread(name='menu_show_recording', target=menu_show_recording, args=([start_record_time]))
    t.start()

    choice = raw_input()
    main.stop_record()

    conclusion_screen(start_record_time)

def menu_show_starting () :
    while not settings.is_recording :
        clear_screen()
        template_menu_show_what_doing('Wait for start', 'Stop')
        time.sleep(0.500)

def menu_show_recording (start_record_time) :
    while settings.is_recording :
        clear_screen()
        template_menu_show_what_doing('Recording', 'Stop', ['Time : ' + str(round(time.time() - start_record_time, 2)) + 's'])
        time.sleep(0.500)

def template_menu_show_what_doing (status_string, next_string, options_string = []) :
        frame = settings.frame

        features_out = features.print_while_recording(frame)

        print '##########################################'
        print "Files : '" + settings.path + '/' + settings.file_name + '/' + str(settings.file_index) + "'"
        print '##########################################'
        print 'Status : ', status_string
        print '##########################################'
        for item in options_string:
            print item
            print '##########################################'
        print '\nLeft hand  : ', '[X]' if 'left' in frame['hands'] else '[_]'
        print 'Right hand : ', '[X]' if 'right' in frame['hands'] else '[_]'
        print '\nPrint Features_out: \n', features_out
        print '\n\n to ', next_string, ' press Enter ! '

# Conclusion screen
def conclusion_screen (start_record_time) :
    clear_screen()

    print '\nTotal time : ' + str(time.time() - start_record_time)
    print 'Want to save ?'
    print '\nWriting Files...'
    main.wait_for_finish()
    print '\nDone'

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
