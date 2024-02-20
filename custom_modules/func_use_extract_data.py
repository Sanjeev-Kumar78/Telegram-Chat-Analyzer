import pandas as pd
import re

import custom_modules.func_analysis as analysis


def startsWithDateTime(s):
    pattern = '^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4})(,)? ([0-9])|([0-9]):([0-9][0-9]) '
    result = re.match(pattern, s)
    if result:
        return True
    return False


def startsWithAuthor(s):
    """
        This function is used to verify the string(s) contains 'Author' or not with the help of regular expressions.

        Parameters:
            s: String

        Returns:
            True if it contains author name otherwise False
    """

    # pattern = '^([\w()\[\]-]+):|([\w]+[\s]+([\w()\[\]-]+))'
    # result = re.match(pattern, s)
    # if result:
    #     return True
    # return False
    """Authors Name along with emojis are also considered"""
    if s.find(":") != -1:
        return True
    else:
        return False

def getDataPoint(line):
    """
        Use to extract the date, time, author and message from line.

        Parameters: 
            line (from txt file)

        Returns:
            date, time, author, message        
    """
    splitLine = line.split(
        ' - ')  # splitLine = ['18/06/17, 22:47', 'Loki: Why do you have 2 numbers, Banner?']

    dateTime = splitLine[0]  # dateTime = '18/06/17, 22:47'

    if ',' not in dateTime:
        dateTime = dateTime.replace(' ', ', ', 1)

    date, time = dateTime.split(', ')  # date = '18/06/17'; time = '22:47'


    if "am" in time:
        # time = '11:00 am' becomes time = '11:00'
        time = time.replace("am", "")
        
    elif "pm" in time:
        # time = '11:00 pm' becomes time = '11:00 '
        time = time.replace("pm", "")
        time = time.split(':')  # time = ['11', '00 ']
        time[0] = str(int(time[0]) + 12)  # time = ['23', '00 ']
        time = ':'.join(time)  # time = '23:00 '
    else:
        if len(time) == 4:
            time = '0' + time
        
    # message = 'Loki: Why do you have 2 numbers, Banner?'
    message = ' '.join(splitLine[1:])

    if startsWithAuthor(message):  # True
        # splitMessage = ['Loki', 'Why do you have 2 numbers, Banner?']
        splitMessage = message.split(': ')
        author = splitMessage[0]  # author = 'Loki'
        # message = 'Why do you have 2 numbers, Banner?'
        message = ' '.join(splitMessage[1:])
    else:
        author = None
    return date, time, author, message


def read_data(file_contents, date_format):
    """
        This function is use to return the extracted data from txt file.

        Parameters:
            file_contents -> line by line contents from txt chat file

        Returns:
            data -> list of list having elements as date, time, author and message by the user.
    """

    data = []  # List to keep track of data so it can be used by a Pandas dataframe

    messageData = []  # to capture intermediate output for multi-line messages
    # Intermediate variables to keep track of the current message being processed
    date, time, author = None, None, None

    for line in file_contents:
        line = line.strip()  # Guarding against erroneous leading and trailing whitespaces
        # If a line starts with a Date Time pattern, then this indicates the beginning of a new message
        if startsWithDateTime(line):
            # Check if the message buffer contains characters from previous iterations
            if len(messageData) > 0:
                # Save the tokens from the previous message in data
                data.append([date, time, author, ' '.join(messageData)])
            messageData.clear()  # Clear the messageData so that it can be used for the next message
            # Identify and extract tokens from the line
            date, time, author, message = getDataPoint(line)
            messageData.append(message)  # Append message
        else:
            # If a line doesn't start with a Date Time pattern, then it is part of a multi-line message. So, just append to messageData
            messageData.append(line)

    df = pd.DataFrame(data, columns=['Date', 'Time', 'Author', 'Message'])
    df["Date"] = pd.to_datetime(
        df["Date"], infer_datetime_format=True)
    df['emoji'] = df["Message"].apply(analysis.extract_emojis)

    return df
