#!/usr/bin/env python
"""Tool to generate xlsx file and send it on mail."""

import glob
import os
import pandas as pd
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.encoders import encode_base64
from email.message import Message
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import time
import xlsxwriter


def generate_report(data):
    """
    Function to generate xlsx file from dataset.

    :param data: information to create xlsx file
    :type data: list
    :return: filename
    :rtype: string
    """

    if not data:
        return False

    filename_format = 'Firmware_Compatibility_Report'
    valid = validate_data(data)
    if valid is True:

        report_dir = os.getcwd() + '/firmware_reports'
        if not os.path.exists(report_dir):
            os.mkdir(report_dir)

        new_data = format_data(data)
        filename = filename_format + '_' + time.strftime("%Y%m%d-%H%M%S") + '.xlsx'
        filepath = report_dir + '/' + filename
        writer = pd.ExcelWriter(filepath, engine='xlsxwriter')

        # write summary sheet to same excel
        summary_tabular_data = pd.DataFrame(new_data.get('summary'))
        summary_tabular_data.to_excel(writer, sheet_name='Summary', index=False)
        for platform_name in new_data.get('platforms'):
            tabular_form_data = pd.DataFrame(new_data.get('data').get(platform_name))
            tabular_form_data.to_excel(writer, sheet_name=platform_name)
        writer.save()

    # check if file generated successfully
    if os.path.isfile(filepath):
        return True
    else:
        return False


def validate_data(data):
    """
    Function to validate data.

    :param data: information to create csv file
    :type data: list
    :return: True/False
    :rtype: boolean
    """

    if not data:
        return False

    # check data format is a list
    if not isinstance(data, list):
        return False

    validlist = [True for i in data if isinstance(i, dict)]

    for value in validlist:
        # check all the values in a list should be true if not then return False
        if value is not True:
            return False

    return True


def format_data(data):
    """
    Function to format data on the basis of platform name and to calculate the summary of a data.

    :param data: information to create csv file
    :type data: list
    :return: formatted data
    :rtype: dict
    """

    list_of_platforms = []
    new_data = {}
    summary_data = []
    for items in data:
        if items.get('Platform') not in list_of_platforms:
            list_of_platforms.append(items.get('Platform'))
            new_data[items.get('Platform')] = [items]
        else:
            new_data[items.get('Platform')].append(items)

    for key, value in new_data.items():
        summary_data.append({'Platform': key, 'Total': len(value)})

    return dict(
        platforms=list_of_platforms,
        data=new_data,
        summary=summary_data
    )


def sendMail(emailto):
    """
    Send email function.

    :param email_to: list of email
    :type emailto: list
    """

    emailfrom = 'pyERC@simplivity.com'
    filepath = os.getcwd() + '/firmware_reports/*'
    list_of_files = glob.glob(filepath)

    # if files not found then return False
    if not list_of_files:
        return False

    fileToSend = max(list_of_files, key=os.path.getctime)

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ",".join(emailto)
    msg["Subject"] = "Firmware Report - " + time.strftime("%Y%m%d-%H%M%S")
    msg.preamble = "Firmware Report"

    df = pd.read_excel(fileToSend, sheet_name = 'Summary')

    body = '''<div>Hi,<br><br>
        <div>Firmware Table:<div><br>
        ''' + df.to_html() + '''<br><br><br><br>
        <div>Regards,<br> pyERC</div>
    <div>'''
    msg.attach(MIMEText(body, 'html')) 

    ctype, encoding = mimetypes.guess_type(fileToSend)

    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    fp = open(fileToSend, 'rb')
    attachment = MIMEBase(maintype[0], ctype[1])
    attachment.set_payload(fp.read())
    fp.close()
    encode_base64(attachment)

    attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(fileToSend))
    msg.attach(attachment)

    server = smtplib.SMTP('10.250.0.131')
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()
    return True
