import subprocess
import os


def getPipVersion():
    """
    Function to get pip version on machine.

    :return: pip version
    """

    stdoutdata = subprocess.getoutput("python --version")
    output_list = stdoutdata.split()

    if not output_list:
        return False
    if not output_list[1]:
        return False
    
    splitList = output_list[1].split('.')
    
    if int(splitList[0]) == 3:
        return 'pip3'
    else:
        return 'pip'

def getListOfAvailableModules():
    """
    Function to get list of available modules in a project.

    :return: list
    """

    # install pipreqs library to generate requirenment.txt which will have all the module names
    subprocess.run(getPipVersion() + " install pipreqs")
    
    # generate requirenment.txt file
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    subprocess.run("pipreqs --force " + ROOT_DIR)

    if not os.path.isfile(ROOT_DIR + '/requirements.txt'):
        return "Not able to create requirenment file."

    return ROOT_DIR + '/requirements.txt'

def installAllRequirements():
    """
    Function to install all requirements for project

    :return: True/False
    """

    requirementFilePath = getListOfAvailableModules()
    subprocess.run(getPipVersion() + " install -r " + requirementFilePath)
    print("Successfully installed all required packages.")
    return True
