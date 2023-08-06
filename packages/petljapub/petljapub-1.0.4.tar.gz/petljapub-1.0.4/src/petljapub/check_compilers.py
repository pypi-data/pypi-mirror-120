import subprocess
import re
from petljapub import logger
from petljapub import config


def get_version(command):
    try: 
        result = subprocess.run([command, '--version'], stdout=subprocess.PIPE)
        version_line = result.stdout.decode('utf-8').split('\n')[0]
        m = re.search(r'[0-9]+([.][0-9]+)*', version_line)
        return m.group(0)
    except:
        return None

def version_ok(version, required_version):
    return list(map(int, version.split("."))) >= \
           list(map(int, required_version.split(".")))

def check_compiler(name, command, required_version):
    version = get_version(command)
    if not version:
        logger.warn("No", name, "installed or not in path")
        return False
    if not version_ok(version, required_version):
        logger.warn("Found", name, version, "but version >=", required_version, "is required")
        return False
    else:
        logger.info("Found", name, version)
        return True

def check_compilers():
    pandoc = check_compiler("pandoc", "pandoc", "2.0")

    cpp_compiler = None
    if check_compiler("g++", "g++", "4.9") and not cpp_compiler:
        cpp_compiler = "G++"
    if check_compiler("MSVC++", "cl", "14.1") and not cpp_compiler:
        cpp_compiler = "MSVC++"

    c_compiler = None
    if check_compiler("gcc", "gcc", "0.0"):
        c_compiler = "GCC"

    cs_compiler = None
    if check_compiler("mono", "mono", "6.8") and not cs_compiler:
        cs_compiler = "MONO"
    if check_compiler("MSVC#", "csc", "3.1") and not cs_compiler:
        cs_compiler = "MSVC#"
    if check_compiler(".NET", "dotnet", "3.1") and not cs_compiler:
        cs_compiler = ".NET"

    logger.info("-----------------  Final report  ----------------------")
    
    if not cpp_compiler:
        logger.error("No C++ compiler found. Please install one (g++ or MSVC++) and ensure it is in the path.")
    if not c_compiler:
        logger.warn("No C compiler found. Please install gcc and ensure it is in the path, or it will not be possible to work with C files.")
    if not cs_compiler:
        logger.warn("No C# compiler found. Please install one (.NET FRAMEWORK, .NET CORE or MonoDevelop) and ensure it is in the path, or it will not be possible to work with C# files.")
    if not pandoc:
        logger.warn("No pandoc >=", pandoc_required_version, "found. Please install it (https://pandoc.org/) or it will not be possible to generate HTML and LaTeX publications.")


    config.write_config({"pandoc": pandoc, "cpp_compiler": cpp_compiler, "cs_compiler": cs_compiler, "c_compiler": c_compiler})
        
        
if __name__ == '__main__':
    check_compilers()
