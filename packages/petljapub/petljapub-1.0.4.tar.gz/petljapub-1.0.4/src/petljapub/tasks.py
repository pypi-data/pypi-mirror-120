import os, sys, glob, shutil
import re
import json
from datetime import date
from string import Template
import tempfile

from invoke import task

from petljapub import logger

from petljapub.translit import lat_to_cyr, cyr_to_lat
from petljapub.util import read_file, write_to_file
from petljapub.md_util import PandocMarkdown
from petljapub.serialization import ZipWriter

from petljapub.task import Task
from petljapub.task_repository import TaskRepository
from petljapub.publication_repository import PublicationRepository
from petljapub.yaml_specification import YAMLSpecification, YAMLSpecificationVisitor
from petljapub.yaml_specification_visitor_stats import YAMLSpecificationVisitorStats
from petljapub.yaml_specification_visitor_runtime import RuntimeTaskVisitor
from petljapub.task_visitor_html import TaskVisitorHTML
from petljapub.publication_visitor_check import PublicationVisitorCheck
from petljapub.publication_visitor_html import PublicationVisitorHTML, PublicationVisitorHTMLPetljaPackage
from petljapub.publication_visitor_tex import PublicationVisitorTeX
from petljapub.compilation import tgen_dir
from petljapub.plot_times import plot_times
import petljapub.check_compilers

sys.stdout.reconfigure(encoding='utf-8')

# directory where all auxiliary data files are stored
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


# identifier of the task in the current directory
def task_id():
    return Task.extract_id_from_dir(os.path.basename(os.getcwd()))

# check if the script is invoked from a task directory
def is_task_dir(dir, is_new_dir=False):
    st = task_id() + "-st.md"
    return re.match(r"\d{2}\ .+", dir) and (is_new_dir or os.path.isfile(st))

# ensure that script is called within a task directory
def ensure_task_dir(is_new_dir=False):
    dir = os.path.basename(os.getcwd())
    if not is_task_dir(dir, is_new_dir):
        logger.error("Task directory must start by two leading zeroes and must contain -st.md file")
        return False
    return True

# compile source file
def compile(ctx, sol, lang):
    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    task.compile(sol, lang)

# check if the file exists and if it does not try to find it in the given default directory
def obtain_file(file, default_dir):
    if file and not os.path.isfile(file):
        default_file = os.path.join(default_dir, file)
        if not os.path.isfile(default_file):
            logger.warn("ignoring non-existent file", file)
            file = None
        else:
            logger.warn("using preinstalled file:", default_file)
            file = default_file
    return file
    
################################################################################
## Processing of the current task
    
@task
def new(ctx):
    """
    Start working on a new task (template files are generated)
    """
    if not ensure_task_dir(True):
        return
    if len(os.listdir(os.getcwd())) != 0:
        logger.error("directory must be empty")
        return
    template_dir = os.path.join(data_dir, '_task_template')
    task_name_cyr = lat_to_cyr(task_id().replace("_", " ").capitalize())
    subst = {
        "TASK_NAME": task_id(),
        "TASK_NAME_CYR": lat_to_cyr(task_id().replace("_", " ").capitalize()),
        "DATE": date.today().strftime("%Y-%m-%d")
    }
    for file in os.listdir(template_dir):
        file_contents = read_file(os.path.join(template_dir, file))
        write_to_file(os.path.basename(file).replace("task", task_id()),
                      Template(file_contents).safe_substitute(subst))

@task
def cpp(ctx):
    """
    Compile the main C++ solution file
    """
    compile(ctx, "ex0", "cpp")

@task
def ex1_cpp(ctx):
    """
    Compile the first alternative C++ solution file
    """
    compile(ctx, "ex1", "cpp")

@task
def ex2_cpp(ctx):
    compile(ctx, "ex2", "cpp")

@task
def ex3_cpp(ctx):
    compile(ctx, "ex3", "cpp")

@task
def ex4_cpp(ctx):
    compile(ctx, "ex4", "cpp")
    
@task
def ex5_cpp(ctx):
    compile(ctx, "ex5", "cpp")

@task
def ex6_cpp(ctx):
    compile(ctx, "ex6", "cpp")
    
@task
def ex7_cpp(ctx):
    compile(ctx, "ex7", "cpp")

@task
def ex8_cpp(ctx):
    compile(ctx, "ex8", "cpp")

@task
def ex9_cpp(ctx):
    compile(ctx, "ex9", "cpp")

@task
def ex10_cpp(ctx):
    compile(ctx, "ex10", "cpp")

@task
def ex11_cpp(ctx):
    compile(ctx, "ex11", "cpp")

@task
def ex12_cpp(ctx):
    compile(ctx, "ex12", "cpp")

@task
def ex13_cpp(ctx):
    compile(ctx, "ex13", "cpp")

@task
def ex14_cpp(ctx):
    compile(ctx, "ex14", "cpp")

@task
def ex15_cpp(ctx):
    compile(ctx, "ex15", "cpp")

@task
def c(ctx):
    """
    Compile the main C solution file
    """
    compile(ctx, "ex0", "c")
    
@task
def ex1_c(ctx):
    """
    Compile the first alternative C# solution file
    """
    compile(ctx, "ex1", "c")

@task
def ex2_c(ctx):
    compile(ctx, "ex2", "c")

@task
def ex3_c(ctx):
    compile(ctx, "ex3", "c")

@task
def ex4_c(ctx):
    compile(ctx, "ex4", "c")
    
@task
def ex5_c(ctx):
    compile(ctx, "ex5", "c")

@task
def ex6_c(ctx):
    compile(ctx, "ex6", "c")
    
@task
def ex7_c(ctx):
    compile(ctx, "ex7", "c")

@task
def ex8_c(ctx):
    compile(ctx, "ex8", "c")

@task
def ex9_c(ctx):
    compile(ctx, "ex9", "c")

@task
def ex10_c(ctx):
    compile(ctx, "ex10", "c")
    
@task
def ex11_c(ctx):
    compile(ctx, "ex11", "c")
    
@task
def ex12_c(ctx):
    compile(ctx, "ex12", "c")
    
@task
def ex13_c(ctx):
    compile(ctx, "ex13", "c")

@task
def ex14_c(ctx):
    compile(ctx, "ex14", "c")

@task
def ex15_c(ctx):
    compile(ctx, "ex15", "c")


@task
def cs(ctx):
    """
    Compile the main C# solution file
    """
    compile(ctx, "ex0", "cs")

    
@task
def ex1_cs(ctx):
    """
    Compile the first alternative C# solution file
    """
    compile(ctx, "ex1", "cs")

@task
def ex2_cs(ctx):
    compile(ctx, "ex2", "cs")

@task
def ex3_cs(ctx):
    compile(ctx, "ex3", "cs")

@task
def ex4_cs(ctx):
    compile(ctx, "ex4", "cs")
    
@task
def ex5_cs(ctx):
    compile(ctx, "ex5", "cs")

@task
def ex6_cs(ctx):
    compile(ctx, "ex6", "cs")
    
@task
def ex7_cs(ctx):
    compile(ctx, "ex7", "cs")

@task
def ex8_cs(ctx):
    compile(ctx, "ex8", "cs")

@task
def ex9_cs(ctx):
    compile(ctx, "ex9", "cs")

@task
def ex10_cs(ctx):
    compile(ctx, "ex10", "cs")
    
@task
def ex11_cs(ctx):
    compile(ctx, "ex11", "cs")
    
@task
def ex12_cs(ctx):
    compile(ctx, "ex12", "cs")
    
@task
def ex13_cs(ctx):
    compile(ctx, "ex13", "cs")

@task
def ex14_cs(ctx):
    compile(ctx, "ex14", "cs")

@task
def ex15_cs(ctx):
    compile(ctx, "ex15", "cs")

@task(pre=[cpp])
def tgen(ctx):
    """
    Generate testcases
    """
    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    task.generate_example_testcases()
    task.generate_testcases()

@task
def tgen_hpp(ctx):
    """
    Copy tgen include files to current directory
    """
    for filename in glob.glob(os.path.join(tgen_dir(), "tgen*.hpp")):
        shutil.copy(filename, os.getcwd())
    
@task
def checker(ctx):
    """
    Compile custom checker
    """
    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    task.compile_checker()

@task(help={
    'sol': "Name of the solution (ex0, ex1, ...)",
    'lang': "Programming language of the solution",
    'recompile': "Recompile all solutions (and the custom checker if it exists) before checking"
})
def check(ctx, sol, lang='cpp', recompile=False, verbosity=1, timeout=2):
    """
    Check the given solution for the current task
    """
    logger._verbosity = 4
    if not ensure_task_dir():
        return
    
    task = Task(os.getcwd())
    if not sol.startswith("ex"):
        sol, lang = "ex0", sol
    task.check(sol, lang, force_recompile=recompile, verbosity=verbosity, timeout=timeout)

    
@task(help={'recompile': "Recompile all solutions (and the custom checker if it exists) before checking",
            'verbosity': "Level of messages printed to the user",
            'timeout': "timeout for every testcase (in seconds)"})
def check_all(ctx, recompile=False, verbosity=1, timeout=2):
    """
    Check all solutions for the current task
    """
    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    task.check_all(force_recompile=recompile, verbosity=verbosity, timeout=timeout)


@task
def extract_examples(ctx):
    """
    Extract and check examples from the problem statement
    """
    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    examples = task.examples(strip_md_verbatim = True)
    for i, example in enumerate(examples):
        input = os.path.join(task.dir(), "{:02d}.in".format(i+1))
        write_to_file(input, example["input"])
        expected_output = tempfile.NamedTemporaryFile(delete=False,mode="w")
        expected_output.write(example["output"])
        expected_output.close()
        result, ellapsed_time = task.check_testcase("ex0", "cpp", input, expected_output.name)
        logger.info(result, "-", os.path.basename(input))
        os.remove(expected_output.name)
    
    logger.info("Extracted {} example{}".format(len(examples), "" if len(examples) == 1 else "s"))
    
@task
def ee(ctx):
    return extract_examples(ctx)

@task(help={
    'force-run': "If not true, times can be read from time.json file (if it is available)",
    'timeout': "Timeout (in seconds) for each solution run",
    'repeat': "For better accurracy, solutions runs are repeated and median value is used",
    'plot': "Graphically show runtimes (using bar plot)",
    'lang': "Plot only runtime for the given language",
    'sol': "Plot only runtime for the given solution"
})
def time(ctx, force_run=False, timeout=2, repeat=3, plot=False, sol=None, lang=None):
    """
    Measure runtime for the current task
    """
    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    params = {
        "force_run": force_run,
        "timeout": timeout,
        "repeat": repeat
    }
    times = task.measure_all_runtimes(params)
    if plot:
        plot_times(times, lang=lang, sol=sol)
    print(json.dumps(times, indent=4))

@task(iterable=["langs"])
def preview(ctx, langs=None, css=None, header=None):
    """
    Generate html preview for the current task
    """
    
    if not ensure_task_dir():
        return

    # default languages
    if not langs:
        langs = ["cpp", "cs"]

    # if files do not exist, try to find preinstalled files in the data directory
    css = obtain_file(css, os.path.join(data_dir, "html"))
    header = obtain_file(header, os.path.join(data_dir, "md"))

    task = Task(os.getcwd(), normalize_md=PandocMarkdown.fix)
    task_visitor = TaskVisitorHTML(css, header)
    task_visitor.visit_task(task, langs)


@task      
def testcases(ctx):
    """
    Generate zip with all testcases for the currrent task
    """

    if not ensure_task_dir():
        return
    task = Task(os.getcwd())
    writer = ZipWriter(os.path.join(task.build_dir(), "testcases.zip"))
    writer.open()
    task.generate_testcases()
    i = 1
    for testcase_in in task.testcases():
        logger.info(testcase_in)
        writer.copy_file(testcase_in, "{:02d}.in".format(i))
        testcase_out = testcase_in[0:-2] + "out"
        logger.info(testcase_out)
        writer.copy_file(testcase_out, "{:02d}.out".format(i))
        i += 1
    writer.close()

################################################################################
## Processing of yaml specifications

@task(help={'yaml': "YAML specification of the publication",
            'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
            'recompile': "Recompile all solutions (and the custom checker if it exists) before checking",
            'timeout': "Timeout in seconds for running each testcase"})
def check_yaml(ctx, yaml, tasks_dir=None, pub_dir=None, recompile=False, timeout=2, verbosity=1):
    """
    Check correctness of all solutions for all tasks specified in a yaml file
    """
    logger._verbosity = verbosity

    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
    if not pub_dir:
        pub_dir = os.path.dirname(yaml)

    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")

    if pub_dir and not os.path.isdir(pub_dir):
        logger.error(pub_dir, "is not a directory")
        
    task_repo = TaskRepository(tasks_dir)
    pub_repo = PublicationRepository(pub_dir)
    yaml_specification = YAMLSpecification(yaml)
    yaml_specification.traverse(PublicationVisitorCheck(yaml_specification, task_repo, recompile, timeout))

@task(help={
    'yaml': "YAML specification of the publication",
    'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
    'force-run': "If not true, times can be read from time.json file (if it is available)",
    'timeout': "Timeout (in seconds) for each solution run",
    'repeat': "For better accurracy, solutions runs are repeated and median value is used",
})
def time_yaml(ctx, yaml, tasks_dir=None, pub_dir=None, force_run=False, timeout=2, repeat=3):
    """
    Measure runtime for all tasks specified in the yaml file
    """
    params = {
        "force_run": force_run,
        "timeout": timeout,
        "repeat": repeat
    }

    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
        
    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
        
    task_repo = TaskRepository(tasks_dir)
    yaml_specification = YAMLSpecification(yaml)
    yaml_specification.traverse(RuntimeTaskVisitor(task_repo, params))

# report statistics about the publication
@task(help={'yaml': "YAML specification of the publication",
            'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)"})
def stats_yaml(ctx, yaml, tasks_dir=None):
    """
    Report statistics about tasks in yaml file and repository

    """
    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)

    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")

    yaml = YAMLSpecification(yaml)
    task_repo = TaskRepository(tasks_dir)
    yaml.traverse(YAMLSpecificationVisitorStats(yaml, task_repo))
    
# build the publication in html format
@task(help={'yaml': "YAML specification of the publication",
            'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
            'pub-dir': "Directory where publication files are stored (if different from the one where the YAML file resides)",
            'dst': "Location where generated files are stored (directory or a ZIP file)",
            'standalone': "Controls if standalone HTML files are generated, or just HTML fragments to be included in other HTML files",
            'join-langs': "Controls whether a single or seperate HTML files are generated for different programming languages",
            'css': "CSS stylesheet to be applied to standalone HTML files",
            'header': "A header to be prepended to each Markdown file before conversion to HTML is applied",
            'lat': "If this flag is set, all content ist transliterated to latin alphabet"})
def html(ctx, yaml, dst, tasks_dir=None, pub_dir=None, standalone=True, join_langs=True, css=None, header=None, lat=False):
    """
    Build task or publication in HTML format
    """

    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
    if not pub_dir:
        pub_dir = os.path.dirname(yaml)

    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
        return

    if pub_dir and not os.path.isdir(pub_dir):
        logger.error(pub_dir, "is not a directory")
        return

    css = obtain_file(css, os.path.join(data_dir, "html"))
    header = obtain_file(header, os.path.join(data_dir, "md"))
        
    task_repo = TaskRepository(tasks_dir, normalize_md=PandocMarkdown.fix)
    pub_repo = PublicationRepository(pub_dir, normalize_md=PandocMarkdown.fix)

    yaml = YAMLSpecification(yaml)
    translit = (lambda x: x) if not lat else cyr_to_lat
    visitor = PublicationVisitorHTML(yaml, task_repo, pub_repo, dst, langs=yaml.langs(),
                                     html=True, standalone=standalone, css=css, header=header, join_langs=join_langs, translit=translit)
    yaml.traverse(visitor)

# build the publication in html format for petlja publishing
@task(help={'yaml': "YAML specification of the publication",
            'dst': "Location where generated files are stored (directory or a zip file)",
            'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
            'pub-dir': "Directory where publication files are stored (if different from the one where the YAML file resides)",
            'join-langs': "Controls whether a single or seperate HTML files are generated for different programming languages",
            'header': "A header to be prepended to each Markdown file before conversion to HTML is applied",
            'lat': "If this flag is set, all content ist transliterated to latin alphabet",
            'generate-tests': "Forces generating all test cases from scratch"})
def petlja_package(ctx, yaml, dst, tasks_dir=None, pub_dir=None, join_langs=True, header=None, lat=False, generate_tests=False):
    """
    Build package for publishing the publication on petlja.org
    """

    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
    if not pub_dir:
        pub_dir = os.path.dirname(yaml)

    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
        return

    if pub_dir and not os.path.isdir(pub_dir):
        logger.error(pub_dir, "is not a directory")
        return

    header = obtain_file(header, os.path.join(data_dir, "md"))
    
    task_repo = TaskRepository(tasks_dir, normalize_md=PandocMarkdown.fix)
    pub_repo = PublicationRepository(pub_dir, normalize_md=PandocMarkdown.fix)
    
    yaml = YAMLSpecification(yaml)
    translit = (lambda x: x) if not lat else cyr_to_lat
    visitor = PublicationVisitorHTMLPetljaPackage(yaml, task_repo, pub_repo, dst, langs=yaml.langs(),
                                                  html=True, header=header, join_langs=join_langs, translit=translit)
    visitor._generate_tests = generate_tests
    yaml.traverse(visitor)

# build the publication in latex format ready for producing pdf
@task(help={'yaml': "YAML specification of the publication",            
            'dst': "Path of the resulting file (all image files are saved in the same directory)",
            'tasks-dir': "Directory where tasks are stored (if different from the one where the YAML file resides)",
            'pub-dir': "Directory where publication files are stored (if different from the one where the YAML file resides)",
            'tex': "If tex is false, Markdown is not converted to TeX",
            'header': "A header to be prepended to the Markdown file before conversion to TeX is applied",
            'tex-template': "A tex template to be used",
})
def tex(ctx, yaml, dst, tasks_dir=None, pub_dir=None, tex=True, header=None, standalone=True, tex_template=None, lat=False):
    """
    Build publication in LaTeX format
    """
    if not tasks_dir:
        tasks_dir = os.path.dirname(yaml)
    if not pub_dir:
        pub_dir = os.path.dirname(yaml)

    if not os.path.exists(yaml):
        logger.error(yaml, "does not exist")
        return

    if tasks_dir and not os.path.isdir(tasks_dir):
        logger.error(tasks_dir, "is not a directory")
        return

    if pub_dir and not os.path.isdir(pub_dir):
        logger.error(pub_dir, "is not a directory")
        return

    if os.path.exists(dst) and not os.path.isfile(dst):
        logger.error(args.dst, "exists but is not a regular file")
        return

    header = obtain_file(header, os.path.join(data_dir, "md"))
    tex_template = obtain_file(tex_template, os.path.join(data_dir, "tex"))
    translit = (lambda x: x) if not lat else cyr_to_lat
    
    task_repo = TaskRepository(tasks_dir, normalize_md=PandocMarkdown.fix)
    pub_repo = PublicationRepository(pub_dir, normalize_md=PandocMarkdown.fix)
    
    yaml = YAMLSpecification(yaml)
    visitor = PublicationVisitorTeX(yaml, task_repo, pub_repo, dst, langs=yaml.langs(), tex=tex, header=header, standalone=standalone, tex_template=tex_template, translit=translit)
    yaml.traverse(visitor)

@task
def configure_compilers(ctx):
    """
    Detect compilers for programming langauges (C++, C#, C, Python) and pandoc for generating LaTeX and HTML from Markdown
    """
    petljapub.check_compilers.check_compilers()
