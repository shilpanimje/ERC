#!/usr/bin/env python
__author__ = "Avinash Nair"
__copyright__ = "Copyright 2018, Equipment Record Capture"
__credits__ = ["Yogesh Bora", "Ajinkya Walvalkar"]
__license__ = "HPE"
__version__ = "2.0.0"
__maintainer__ = "Avinash Nair"
__email__ = "avinash.nair@hpe.com"
__status__ = "WIP"

import paramiko, re

def connectDodge(ip):
    '''
        This function will connect to the Dodge system using SSH paramiko & executes command(s) to fetch component firmware information.
    :param ip:
    :return:
    '''

    # Command to fetch firmware inventory from iDRAC
    cmd = 'racadm swinventory'

    # Connecting to iDRAC using SSH paramiko
    print('INFO: Opening SSH Client')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('INFO: Connecting to host: ', ip)
    ssh.connect(ip, port = 22, username = 'root', password = 'calvin')

    print('INFO: Executing command on the Dodge host & fetching the data to process. Please be patient...')
    (stdin,stdout,sterr) = ssh.exec_command(cmd)
    print(type(stdout))
    # Once the command output is fetched, it needs to be parsed/filtered
    return(parseDodgeContents(stdout,ip))
    print(type(stdout))
    #output = stdout.readlines()
    #print(''.join(output))

    # Closing SSH connection
    print('INFO: Closing SSH Client connection')
    ssh.close()

def parseDodgeContents(foo,racip):
    '''
        This function will parse the contents fetched by the command.
        It will bisect the data and store the contents in a dictionary format, which inturn will be stored in a list.
        Thereby accessing this list will get the firmware contents of the host.
    :param foo:
    :return:
    '''

    dashedLine = '-------------------------------------------------------------------'
    softwareInvLine = '-------------------------SOFTWARE INVENTORY------------------------'
    compTypLine = 'ComponentType = FIRMWARE'
    procFinLine = 'Process finished with exit code 0'
    blankLine = ''

    tempDict = {}   # temporary Dictionary to store the contents when reading line by line
    finalDict = {}  # final Dictionary that will be used to add in the list
    stripList = []  # List containing values that are stripped 2nd time. This is used after splitting the contents and spaces left before and after '='
    finalList = []  # final List containing all the dictionary information about the firmware components
    splitList = []  # Temporary list used to split the line based on the '=' keyword

    print('INFO: Parsing through the lines from the STDOUT')

    for line in foo:
        # Stripping the spaces, end of line characters at both ends (left & right)
        line = line.strip()


        # Searching for lines that contains the keyword '='
        if re.search('=',line):
            # Once the line is found, split the line into 2 parts (i.e. left and right) based on the keyword '='
            splitList = str.split(line,'=')
            # Strip the list elements and remove spaces and end of line characters and storing it back in the same list
            stripList = [i.strip() for i in splitList]


            # Storing values against the keys in the temporary dictionary
            if stripList[0] == 'ComponentType':
                tempDict['ComponentType'] = stripList[1]
            elif stripList[0] == 'Current Version':
                tempDict['Current Version'] = stripList[1]
            elif stripList[0] == 'ElementName':
                tempDict['ElementName'] = stripList[1]
            elif stripList[0] == 'FQDD':
                tempDict['FQDD'] = stripList[1]
            elif stripList[0] == 'Available Version':
                tempDict['Available Version'] = stripList[1]
            elif stripList[0] == 'Rollback Version':
                tempDict['Rollback Version'] = stripList[1]
            elif stripList[0] == 'InstallationDate':
                tempDict['InstallationDate'] = stripList[1]
            else:
                continue

        # If you hit a dashed line in the list, then it means that all the contents related to on component is traversed through and loaded into the temporary dictionary.
        # Now it is time to offload the contents of the temporary dictionary to the final one, so that the data is not overridden.
        # Also the final dictionary is then loaded into the final List
        if line == dashedLine:
            finalDict = tempDict.copy()
            tempDict.clear()
            finalList.append(finalDict)
    print(finalList)
    exit()
    # print the entire component firmware information for dodge for the host
    #print('INFO: Component firmwares: ', finalList)

    dodgeFWDict = {}

    dodgeFWDict['RAC IP'] = racip
    dodgeFWDict['Platform'] = 'Dodge'

    for i in finalList:
        #print(i)

        if (re.search('Integrated Remote Access Controller', i['ElementName'])):
            for k,v in i.items():
                if k == 'Current Version':
                    dodgeFWDict[i['ElementName']] = i['Current Version']
                    #print(dodgeFWDict)

        if (re.search('Backplane Expander', i['ElementName'])):
            for k,v in i.items():
                if k == 'Current Version':
                    dodgeFWDict[i['ElementName']] = i['Current Version']
                    #print(dodgeFWDict)

        if (re.search('OS COLLECTOR', i['ElementName'])):
            for k,v in i.items():
                if k == 'Current Version':
                    dodgeFWDict[i['ElementName']] = i['Current Version']
                    #print(dodgeFWDict)

        if (re.search('PERC H730', i['ElementName'])):
            for k,v in i.items():
                if k == 'Current Version':
                    dodgeFWDict[i['ElementName']] = i['Current Version']
                    #print(dodgeFWDict)

        if (re.search('BIOS', i['ElementName'])):
            for k,v in i.items():
                if k == 'Current Version':
                    dodgeFWDict[i['ElementName']] = i['Current Version']
                    #print(dodgeFWDict)

        if (re.search('Lifecycle Controller', i['ElementName'])):
            for k,v in i.items():
                if k == 'Current Version':
                    dodgeFWDict[i['ElementName']] = i['Current Version']
                    #print(dodgeFWDict)

        if (re.search('PERC H330', i['ElementName'])):
            for k,v in i.items():
                if k == 'Current Version':
                    dodgeFWDict[i['ElementName']] = i['Current Version']
                    #print(dodgeFWDict)

        if (re.search('uEFI', i['ElementName'])):
            for k,v in i.items():
                if k == 'Current Version':
                    dodgeFWDict['uEFI Diagnostics'] = i['Current Version']
                    #print(dodgeFWDict)

    dodgeFWDictfinal = dodgeFWDict.copy()
    dodgeFWDict.clear()
    #print('INFO: Dodge FW: ', dodgeFWDictfinal)

    return(dodgeFWDictfinal)