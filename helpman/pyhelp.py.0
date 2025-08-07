#this script is show help minimalis for python module
#tested on windows
#licface (licface@yahoo.com)

import os
import sys

__version__ = "0.1"
__filename__ = os.path.basename(sys.argv[0])
__author__ = "licface"
__url__ = "licface@yahoo.com"
__target__ = "all"
__build__ = "2.7"

__usage__ = "\t use : " + __filename__ + " [module/module.function/module.class or other \n\n\t Example : " + __filename__ + " os.path"

def check_python_home(data_array_dir):
    """ check if python dir is exist in data array of PATH or PYTHONHOME or PYTHON_HOME environment "data_array_dir" is data from PATH,PYTHONHOME,PYTHON_HOME or other directory may have python.exe, this must a tuple or arary data """
    for i in data_array_dir:
        if "python" in i:
            if path.isdir(i):
                pythonhome = path.abspath(i)
                return pythonhome
            else:
                pass
        elif "Python" in i:
            if path.isdir(i):
                pythonhome = path.abspath(i)
                return pythonhome
            else:
                pass
        else:
            return False
        
def check_python_path(data_array_path):
    """ check if python dir is exist in data array of PATH or PYTHONHOME or PYTHON_HOME environment "data_array_dir" is data from PATH,PYTHONHOME,PYTHON_HOME or NOT other directory may have python.exe, this must a tuple or arary data"""
    data_a = str(data_array_path).split(";")
    for i in data_a:
        if path.isdir(i):
            if "python" in i:
                data_b = os.popen("dir /s /b \"" + str(i) + "\\").readlines()
                for x in data_b:
                    if "python.exe" in x:
                        PYTHONPATH = x
                    elif "Python.exe" in x:
                        PYTHONPATH = x
            elif "Python" in i:
                data_c = os.popen("dir /s /b \"" + str(i) + "\\").readlines()
                for z in data_c:
                    if "python.exe" in z:
                        PYTHONPATH = z
                    elif "Python.exe" in z:
                        PYTHONPATH = z
        else:
            if "python.exe" in i:
                PYTHONPATH = i
            elif "Python.exe" in i:
                PYTHONPATH = i
            else:
                return None
    return PYTHONPATH
        
def extract_python(data_pythonhome):
    """ check if exist "python.exe" on PYTHONHOME, PYTHON_HOME or a Directory, "data_pythonhome" must a directory with ";" 

        return name of directory where "python.exe" if exist    , return None if file not found
    """
    xa = None
    data_a = str(data_pythonhome).split(";")
    #print "data_a = ", data_a
    for i in data_a:
        data_b = os.popen("dir /s /b \"" + str(i) + "\"").readlines()
        #print "data_b = ", data_b
        for x in data_b:
            if "python.exe" in x:
                xa = x
            elif "Python.exe" in x:
                xa = x
            elif "python3.exe" in x:
                xa = x
            elif "Python3.exe" in x:
                xa = x
            else:
                pass
    return xa
    
        
def print_helper(data,intp = "python -c"):
    """ print help() & dir() module
    
        return help() & dir() if True
        return None if Error or False or data/module no Found
    """
    print("\n\n")
    if "." in data:
        data_s = str(data).split(".")
        data_c = "import " + str(data_s[0]) + "; " + "help(" + str(data) + ");print \'All Attribute = \', dir(" + str(data) + ")"
        #data_c = "import " + str(data_s[0]) + ";print dir(" + str(data) + ")"
        try:
            data_p = os.system(intp + " \"" + str(data_c) + "\"")
            #print data_p
            return data_p
        except:
            import traceback
            print("Error: ", traceback.format_exc())
    else:
        try:
            excp = ['dict']
            for i in excp:
                if data == i:
                #if data == "dict":
                    data_c = "help(" + str(data) + ");print \'All Attribute = \', dir(" + str(data) + ")"
                    data_p = os.system(intp + " \"" + str(data_c) + "\"")
                    #print data_p
                    return data_p
                else:
                    data_c = "import " + str(data) + "; " + "help(" + str(data) + ");print \'All Attribute = \', dir(" + str(data) + ")"
                    #data_c = "import " + str(data_s[0]) + ";print dir(" + str(data) + ")"
                    data_p = os.system(intp + " \"" + str(data_c) + "\"")
                    #print data_p
                    return data_p
        except:
            import traceback
            print("Error: ", traceback.format_exc())
    
def print_helper_process_2():
    """ check if PYTHONHOME, PYTHON_HOME or a directory where "python.exe" not found, this will process check a common/famous directory where "python.exe" if exist  """
    if check_python_path == None:
        print("pythonhome = None")
        if os.getenv("PYTHONHOME") == None or os.getenv("PYTHONHOME") == "":
            if os.getenv("PYTHON_HOME") == None or os.getenv("PYTHON_HOME") == "":    
                e = os.popen("dir /b \"c:\\\"").readlines()
                f = os.popen("dir /b \"c:\\Program Files\"").readlines()
                d = check_python_home(e)
                if d != False:
                    PYTHONHOME = d
                    py_interp = extract_python(PYTHONHOME)
                    if py_interp != None:
                        print_helper(sys.argv[1],py_interp)
                else:
                    h = check_python_home(f)
                    if f != False:
                        PYTHONHOME = h
                        py_interp = extract_python(PYTHONHOME)
                        if py_interp != None:
                            print_helper(sys.argv[1],py_interp)
                    else:
                        print("\n\n")
                        print("\t Python Interpreter Not Detection/Installer On Your System/PATH !\n")
                        print("\t Please Set\Install Your Python Version !\n")
            else:
                PYTHONHOME = os.getenv("PYTHON_HOME")
                py_interp = extract_python(PYTHONHOME)
                if py_interp != None:
                    print_helper(sys.argv[1],py_interp)
        else:
            PYTHONHOME = os.getenv("PYTHONHOME")
            py_interp = extract_python(PYTHONHOME)
            if py_interp != None:
                print_helper(sys.argv[1],py_interp)
    else:
        #print "print_helper(sys.argv[1])"
        print_helper(sys.argv[1])

def print_helper_process(data):
    data2 = __import__(data)
    if "." in data:
        data_a = str(data).split(".")
        try:
            if sys.winver > float('2.6'):
                import importlib
                try:
                    importlib.import_module(data_a[0])
                    print(help(data))
                    print("\n\n")
                    print("All Attribute: ", dir(data2))
                except:
                    print("\n")
                    print(__usage__)
            else:
                try:
                    __import__(data_a[0])
                    print(help(data))
                    print("\n\n")
                    print("All Attribute: ", dir(data2))
                except:
                    print("\n")
                    print(__usage__)
        except:
            print("\n")
            print(__usage__)
    else:
        print(help(data))
        print("\n\n")
        print("All Attribute: ", dir(data2))
            
if __name__ == "__main__":
    if len(sys.argv) > 1:
        print_helper_process(sys.argv[1])
        #print extract_python(os.getenv("PATH")) #test
        #print check_python_path(os.getenv("PATH")) #test

    else:
        print("\n")
        print(__usage__)
