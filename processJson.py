import json
import os
import re
from datetime import datetime
import Remittance_Operation
import Payroll_Operation

# Existing keywords
existing_keywords = ['remittance', 'create', 'send', 'payroll']
date_list = []
employee_details = []


# def extract_date(email_body):
#     date_match = re.search(r'on\s+(\d+)(?:st|nd|rd|th)\s+(\w+)\s+(\d+)', email_body)
#     day = int(date_match.group(1))
#     global date
#     date = day
#     month_name = date_match.group(2)
#     year = int(date_match.group(3))
#
#     # Map month name to numeric representation
#     month_dict = {
#         'January': '01',
#         'February': '02',
#         'March': '03',
#         'April': '04',
#         'May': '05',
#         'June': '06',
#         'July': '07',
#         'August': '08',
#         'September': '09',
#         'October': '10',
#         'November': '11',
#         'December': '12'
#     }
#     month = month_dict.get(month_name, '')  # Get the numeric representation of the month
#
#     date_list.append(year)
#     date_list.append(month)
#     date_list.append(day)
#
#     # print(date_list)
#
#
# # return date_list

# Function to extract month's numbers
def extract_month_numbers(text):
    matches = re.findall(r'\b\d+\b', text)
    return [int(match) for match in matches]


# Function to execute the operation based on command
def execute_operation(command):
    if command == 'create_remittance':
        # Call the method to create a remittance
        Remittance_Operation.run(['python', 'create_remittance.py'])
    elif command == 'send_remittance':
        # Call the method to send the remittance
        Remittance_Operation.run(['python', 'send_remittance.py'])
    # Add more conditions for other commands as needed


def delete_json_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    except OSError as e:
        print(f"Error deleting file: {file_path} - {e}")


# get employee list
def extract_employee_details(email_body):
    lines = email_body.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line:
            match = re.search(r'^(.*?) (\d+(?:\.\d+)?|\$[\d.]+/hr)(?: hours)?$', line)
            if match:
                employee_name = match.group(1)
                hours_or_salary = match.group(2)
                employee_details.append((employee_name, hours_or_salary))


def convert_month(month):
    month_dict = {
        'Jan': '1',
        'Feb': '2',
        'Mar': '3',
        'Apr': '4',
        'May': '5',
        'Jun': '6',
        'Jul': '7',
        'Aug': '8',
        'Sep': '9',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }
    return month_dict.get(month)


# Directory path containing JSON files
json_files_directory = '/root/AccountiumEmailBot'

# Iterate over each JSON file

for filename in os.listdir(json_files_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(json_files_directory, filename)

        # Read the JSON file
        with open(file_path, 'r') as json_file:
            email_data = json.load(json_file)

            # Extract relevant information
            subject = email_data['Subject']
            body = email_data['Body']
            nouns = email_data['Nouns']
            verbs = email_data['Verbs']

            # Extract month numbers from nouns and numbers
            document_request_date = email_data['Document Request Date']
            month = document_request_date['Month'][0]  # get month
            year = document_request_date['Year'][0]  # get year
            date = document_request_date['Date']  # get date
            # Etract user information
            credential = email_data['ClientCredentials']
            userAccount = credential['userAccount']
            print(userAccount)
            userPassword = credential['userPassword']
            print(userPassword)
            # call function to log in
            driver = Remittance_Operation.login_to_accountium(userAccount, userPassword)

            # Check if the keywords match with existing keywords : Remittance
            if 'remittance' in nouns and any(keyword in verbs for keyword in existing_keywords):
                for verb in verbs:
                    if 'create' and 'send' in verbs:
                        Remittance_Operation.create_remittance(driver, month, year)
                        Remittance_Operation.send_email(driver)
                        Remittance_Operation.quit_driver(driver)
                        break
                    elif verb == 'send':
                        NumMonth = convert_month(month)
                        # print(NumMonth, year)
                        Remittance_Operation.send_existingRemittance(driver, NumMonth, year)
                        Remittance_Operation.quit_driver(driver)
                        break
                    elif verb == 'create' and 'remittance' in nouns:
                        Remittance_Operation.create_remittance(driver, month, year)
                        Remittance_Operation.quit_driver(driver)
                        break

            # Check if the keywords match with existing keywords :payroll
            if 'payroll' in nouns and any(keyword in verbs for keyword in existing_keywords):
                extract_employee_details(body)
                for verb in verbs:
                    if 'create' or 'send' in verbs:
                        Payroll_Operation.create_payroll(driver, year, month, date, employee_details)
                        Payroll_Operation.quit_driver(driver)
                        break

            # Check if the keywords match with existing keywords :T4

            # Check if the keywords match with existing keywords :Invoice

            # Check if the keywords match with existing keywords : Income statement

            # Check if the keywords match with existing keywords : balance sheet

            # delete the processed file
            # os.remove(file_path)
