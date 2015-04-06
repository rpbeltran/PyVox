import os

def delete_file(path):

    REMOVAL_ERROR = "Error removing " + path

    try:

        os.remove(path)

    except OSError:

        try:

            os.rmdir(path)

        except OSError:

            return "Directory is not empty"

        except:

            return REMOVAL_ERROR

    except:

        return REMOVAL_ERROR

    return False

def open_file(path):

    os.startfile(path)

    return False

def change_dir(path):

    try:

        os.chdir(path)

    except:

        return "Nonexistant path \"" + path + "\""

    return False

def get_dir(x):

    return os.getcwd()

def ls_files(x):

    pass

def shell(command):

    os.system(command)

    return False

def calibrate(time):

    return time

def get_param(command_string, command):

    return command_string[command_string.index(command) + len(command):]

commands = {"RUN" : open_file,
            "DELETE" : delete_file,
            "CHANGE DIRECTORY" : change_dir,
            "CURRENT DIRECTORY" : get_dir,
            "LIST FILES" : ls_files,
            "SHELL" : shell,
            "CALIBRATE" : calibrate}

def case_insensitive_equal(stringA, stringB):

    return stringA.upper() == stringB.upper()

def run_command(command_string):

    result = "Unknown command"

    for command in commands.keys():

        if command_string.upper().startswith(command):

            print "hey"

            result = commands[command](get_param(command_string.upper(), command).upper().strip())

    return result

sendkeysModeInitialized = False
shell = None

def case_insensitive_replace(string, old, new):

    replaced_string = ""

    skip_counter = 0

    for i in xrange(len(string)):

        if case_insensitive_equal(string[i:i+len(old)], old):

            replaced_string += new

            skip_counter += len(old)

        if skip_counter > 0:

            skip_counter -= 1

        else:

            replaced_string += string[i]

    return replaced_string

def sendkeys(keys):

    if keys:

        global sendkeysModeInitialized, shell

        if not sendkeysModeInitialized:

            try:

                import win32com.client

                shell = win32com.client.Dispatch("WScript.Shell")

                sendkeysModeInitialized = True

            except:

                return "Oops"

        if sendkeysModeInitialized:

            keyFilter = {"ENTER KEY" : "~",
                         "SHIFT KEY" : "+",
                         "PAGE UP" : "{PGUP}",
                         "PAGE DOWN" : "{PGDN}",
                         "TAB KEY" : "{TAB}",
                         "BACKSPACE KEY" : "{BACKSPACE}",
                         "ALT KEY" : "{ALT}",
                         "F4" : "{F4}",
                         "+" : "{+}",
                         "!" : "{!}",
                         "~" : "{~}",
                         "^" : "{^}"}

            print keys

            for target in keyFilter.keys():

                keys = case_insensitive_replace(keys, target, keyFilter[target])

            print keys

            in_brackets = False

            key_code = ""

            for index, key in enumerate(keys):
                
                if key == "{":

                    in_brackets = True

                if in_brackets:

                    key_code += key

                    if key == "}":

                        in_brackets = False

                else:

                    key_code = key

                if not in_brackets:

                    shell.SendKeys(key_code)

                    key_code = ""
