import socket
import os
import platform


def validateIP(ip_address):
    """
    Function to validate ip address.

    :param ip_address: ip address
    :type ip_address: string
    :return: True/False
    :rtype: boolean
    """

    if not ip_address:
        return False

    parts = ip_address.split(".")
    if len(parts) != 4:
        return False

    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        return False


def validatePlatform(platformName):
    """
    Function to validate platform names.

    :param platformName: platform name
    :type platformName: string
    :return: True/False
    :rtype: boolean
    """

    if not platformName:
        return False

    list_of_platform = ['Dodge', 'CamryM3', 'CamryM4', 'HondaGen9', 'HondaGen10', 'HondaApollo', 'Lincoln']
    # check platformName exist in a available platform list
    if platformName not in list_of_platform:
        return False

    return True


def checkPingIPStatus(serverIp):
    """
    Function to check the IP provided is pingable using ping command.

    :param serverIp: server ip address
    :return: True/False
    """

    if not serverIp:
        return False

    # check ping command for specific ip address
    rep = os.system('ping ' + ('-n 1 ' if platform.system().lower()=='windows' else '-c 1 ') + serverIp)
    if rep == 0:
        return True
    else:
        return False


def getSMTP():
    """
    Function to get SMTP server ip based on the location script is run.

    :return: SMTP server ip
    """

    SMTP_SERVER_IPS = [{'HOU': '10.250.0.131', 'WEBO':'100.00.0.0'}]

    if checkPingIPStatus(SMTP_SERVER_IPS[0]['HOU']):
        return SMTP_SERVER_IPS[0]['HOU']
    elif checkPingIPStatus(SMTP_SERVER_IPS[0]['WEBO']):
        return SMTP_SERVER_IPS[0]['WEBO']
    else:
        return 0
