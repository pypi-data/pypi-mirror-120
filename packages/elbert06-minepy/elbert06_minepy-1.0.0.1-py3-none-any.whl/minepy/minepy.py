global check_list
check_list = []
global python_space
python_space = 0
global test_value
test_value = 0
global pl1
global st1
global addition_list
addition_list = []
global m 
m = 0
global n
n = 0
global check_list_var
check_list_var = 0
global javacode
javacode = ''
def getglobal():
    global check_list
    return check_list
def init():
    global pl1
    pl1 = Player()
    global st1
    st1 = String()
    check_list = getglobal()
    check_list.append('init')
def println(message):
    check_list.append('sys_activity')
class Integer:
    def __init__(self):
        check_list = getglobal()
        check_list.append("define")
class Player:
    def __init__(self):
        global addition_list
        if not addition_list.__contains__('org.bukkit.entity.Player'):
            addition_list.append('org.bukkit.entity.Player')
        check_list = getglobal()
        check_list.append("define")
    def setHealth(self,value):
        check_list = getglobal()
        check_list.append("activity")
    def getName(self):
        check_list = getglobal()
        check_list.append("setvar")
        return st1
    def sendMessage(self,message):
        check_list = getglobal()
        check_list.append("activity")
class ArrayList:
    def __init__(self,typeof):
        global addition_list
        addition_list.append('java.util.ArrayList')
        check_list = getglobal()
        check_list.append("define")
class String:
    def __init__(self):
        check_list = getglobal()
        check_list.append("define")
class Event:
    def __init__(self,eventname):
        check_list = getglobal()
        check_list.append("define_python")
    def getPlayer(self):
        check_list = getglobal()
        check_list.append("setvar")
        return pl1
class Random:
    def __init__(self):
        global addition_list
        addition_list.append('java.util.Random')
        check_list = getglobal()
        check_list.append("define")
    def nextInt(self,value):
        check_list = getglobal()
        check_list.append("setvar")
        return 15
def time(when):
    global n
    n += 1
    if n == 1:
        check_list = getglobal()
        check_list.append("while_time")
        return True
    else:
        n = 0
        return False
def event(when):
    global m
    m += 1
    if m == 1:
        check_list = getglobal()
        check_list.append("while_event")
        return True
    else:
        m = 0
        return False
def tell():
    global check_list
    print(check_list)
    check_list.append("tell")
def getspace(string):
    global java_space
    string += "   "*java_space
    return string
def make():
    Strin = ''
    global addition_list
    global python_space
    global java_space
    java_space = 0
    global check_list
    global check_list_var
    global javacode
    check_list.append("make")
    while check_list[0] != 'init':
        del check_list[0]
    print(check_list)
    javacode = ''
    file = open("main.py","r")
    lines = file.readlines()
    for i in lines:
        i = str(i)
        getvalue = possible(i)
        if getvalue == True:
            m = check_list[check_list_var]
            if m == 'init':
                javacode = getspace(javacode)
                javacode += 'public class Main extends JavaPlugin implements Listener{\n'
                java_space += 1
                addition_list.append('org.bukkit.plugin.java.JavaPlugin')
                addition_list.append('org.bukkit.event.Listener')
            elif m == 'define_python':
                pass
            elif m == 'define':
                i = forfinish(i)
                i = i.replace(" ","")
                javacode = getspace(javacode)
                i_list = i.split("=")
                variable_name = i_list[0]
                middle_part = i_list[1].split("(")
                if middle_part[0] == "ArrayList":
                    species = middle_part[1].replace(")\n","")
                    javacode += 'ArrayList<'+species+'> '+variable_name+';\n'
                elif middle_part[0] == "Random":
                    javacode += 'Random '+variable_name+' = new Random();\n'
                else:
                    javacode += middle_part[0]+' '+variable_name+';\n'
            elif m == 'activity':
                i = forfinish(i)
                i = i.replace(" ","")
                javacode = getspace(javacode)
                i_list = i.split(".")
                variable_name = i_list[0]
                middle_part = i_list[1].split("(")
                species = middle_part[1].replace(")\n","")
                javacode += variable_name+'.'+middle_part[0]+'('+species+');\n'
            elif m == 'sys_activity':
                i = forfinish(i)
                i = i.replace(" ","")
                javacode = getspace(javacode)
                i_list = i.split("(")
                left_part = i_list[0]
                message = i_list[1].replace(")\n","")
                if left_part == 'println':
                    javacode += 'System.out.println('+message+');\n'
            elif m == 'setvar':
                i = forfinish(i)
                i = i.replace(" ","")
                javacode = getspace(javacode)
                i = i.replace("=", " = ")
                i = i.replace("\n","")
                javacode += i+';\n'  
            elif m == 'while_time':
                i = forfinish(i)
                i = i.replace(" ","")
                javacode = getspace(javacode)
                h = i.replace('whiletime("', '')
                h = h.replace('"):','')
                h = h.replace('\n','')
                if h == "Enable":
                    javacode += 'public void onEnable(){\n'
                    python_space += 1
                    java_space += 1
                if h == "Disable":
                    javacode += 'public void onDisable(){\n'
                    python_space += 1
                    java_space += 1
            elif m == 'while_event':
                global test_value
                test_value += 1
                name = 'test'+str(test_value)
                i = forfinish(i)
                i = i.replace(" ","")
                javacode = getspace(javacode)
                javacode += '@EventHandler\n'
                javacode = getspace(javacode)
                h = i.replace('whileevent("', '')
                h = h.replace('"):','')
                h = h.replace('\n','')
                if not addition_list.__contains__('org.bukkit.event.EventHandler;'):
                    addition_list.append('org.bukkit.event.EventHandler')
                if h.__contains__("Player") and not addition_list.__contains__('org.bukkit.event.player.'+h):
                    addition_list.append('org.bukkit.event.player.'+h)
                elif h.__contains__("Block") and not addition_list.__contains__('org.bukkit.event.block.'+h):
                    addition_list.append('org.bukkit.event.block.'+h)
                elif h.__contains__("Entity") and not addition_list.__contains__('org.bukkit.event.entity.'+h):
                    addition_list.append('org.bukkit.event.entity.'+h)
                javacode += 'public void '+name+'('+h+' e'+') {\n'
                python_space += 1
                java_space += 1
            check_list_var += 1
    java_space -= 1
    javacode = getspace(javacode)
    javacode += '}\n'
    java_space -= 1
    javacode = getspace(javacode)
    javacode += '}\n'
    for h in addition_list:
        Strin += 'import '+h +';\n'
    file = open("data/src/main/java/Main/Main.java","w")
    last_String = 'package Main;\n\n'+Strin+javacode
    file.write(last_String)
def possible(i):
    i = str(i)
    if not i.__contains__("import"):
        no_blank_i = i.replace(" ","")
        if not no_blank_i[0] == "#":
            if not i == "tell":
                if not i == "make":
                    return True
    return False
def forfinish(i):
    global python_space
    global javacode
    global java_space
    if i.__contains__("    "*python_space):
        return i
    else:
        python_space -= 1
        java_space -= 1
        javacode = getspace(javacode)
        javacode += "}\n"
        return i