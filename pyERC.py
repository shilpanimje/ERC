#!/usr/bin/env python
__author__ = "Avinash Nair"
__copyright__ = "Copyright 2018, Equipment Record Capture"
__credits__ = ["Yogesh Bora", "Ajinkya Walvalkar"]
__license__ = "HPE"
__version__ = "2.0.0"
__maintainer__ = "Avinash Nair"
__email__ = "avinash.nair@hpe.com"
__status__ = "WIP"

import paramiko, re, sys, os, csv
import ercDodge as dg
import ercLincoln as ln
#import ercCamry as cam
#import ercHonda as hon
#import pandas as pd
import generator as gen

def main():
    #(ip, sysType) = ('10.11.23.234','Dodge')
    #(ip, sysType) = ('10.11.21.157','Dodge')
    #(ip, sysType) = ('10.11.6.223','Lincoln')

    fwList = []

    myIPList = readIP()

    for item in myIPList:
        if str(item['platform']).lower() == 'dodge':
            print('INFO: Let us connect to %s which has the IP of %s' %(str(item['platform']),item['ip']))
            fwList.append(dg.connectDodge(item['ip']))
            #print(fwList)
            #writeCSV(fwList)
        elif str(item['platform']).lower() == 'lincoln':
            fwList.append(ln.connectLincoln(item['ip']))
        elif str(item['platform']).lower() == 'camrym3':
            cam.connectCamryM3(item['ip'])
        elif str(item['platform']).lower() == 'camrym4':
            cam.connectCamryM4(item['ip'])
        elif str(item['platform']).lower() == 'hondagen9':
            hon.connectHondaGen9(item['ip'])
        elif str(item['platform']).lower() == 'hondagen10':
            hon.connectHondaGen10(item['ip'])
        else:
            print('ERROR: Exiting...\n')

    print(fwList)
    # exit()
    displayFCR(fwList)

    '''
    #Generate a CSV file for the report
    temp = gen.generate_report(fwList)
    emailList = ['avinash.nair@simplivity.com']

    if temp:
        print('INFO: Sending email to ', emailList)
        gen.sendMail(emailList)
    else:
        print('ERROR: File not generated. Email not sent.')
    '''

def readIP():
    filename = 'ips.txt'
    if not os.path.isfile(filename):
        # Checks if the file exists or not in the current directory
        print('ERROR: Exiting, ips.txt does not exist in the same folder.')
        print(r'Kindly create a file "ips.txt" in the following format:')
        print('<RAC IP>,<Dodge/Lincoln/CamryM3/CamryM4/HondaGen9/HondaGen10>')
        sys.exit()
    elif os.path.getsize(filename) <= 0:
        # Checks if the file has contents based on the size of the file
        print('ERROR: ips.txt file is blank. Please fill it with RAC IP.')
        print('Format to be followed:')
        print('<RAC IP>,<Dodge/Lincoln/CamryM3/CamryM4/HondaGen9/HondaGen10>')
        sys.exit()

    tempDict = {}
    ipDict = {}
    ipList = []
    tempList = []

    contents = open(filename, 'r')

    for ip in contents:
        tempList = (ip.split(','))
        tempList = [i.strip() for i in tempList]
        #print(tempList[1])
        tempDict['ip'] = tempList[0]
        tempDict['platform'] = tempList[1]
        ipDict = tempDict.copy()
        ipList.append(ipDict)
    print('INFO: System Info read from input file: ', ipList)

    return(ipList)

def displayFCR(fwList):
    '''
    Firmware compatability report displaying the current versions for the systems
    '''
    print('\n')
    print('-' * 50)
    print('Firmware Compatibility Report'.center(50, ' '))
    print('-' * 50)
    for systems in fwList:
        print('-' * 50)
        for keys, values in systems.items():
            temp = ('%s : %s' % (keys,values))
            print(temp.center(50, ' '))
        print('-' * 50)

if __name__ == "__main__":
    main()
