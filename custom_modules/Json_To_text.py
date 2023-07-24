import json
from dateutil.parser import parse
import tempfile
import os


# Define a function to get the message type from a message dictionary
def get_message_type(message):
    if 'type' in message:
        return message['type']
    else:
        return 'message'


# Define a function to get the text from a message dictionary
def get_text(message):
    if 'text' in message:
        return message['text']
    else:
        return ''


# Define a function to convert a JSON file to text
def convert_json_to_text(json_file):
    # Save uploaded JSON file as a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(json_file.read())
        temp_file_path = temp_file.name

    # Load the JSON data from the temporary file
    with open(temp_file_path, encoding='utf-8') as fp:
        json_data = json.load(fp)

    # Convert each message in the JSON data to a formatted text message
    converted_text = []
    for message in json_data['messages']:
        # Parse the timestamp from the message dictionary
        timestamp = parse(message['date'])
        formatted_timestamp = timestamp.strftime("%d/%m/%y, %I:%M %p")

        # Get the sender and message type from the message dictionary
        sender = message.get('from', '')
        message_type = get_message_type(message)

        # Get the text from the message dictionary based on the message type
        if message_type == 'sticker':
            if 'sticker_emoji' in message:
                text = message['sticker_emoji']
        elif message_type == 'media':
            if 'caption' in message:
                text = message['caption']
            else:
                text = ''
        else:
            text = get_text(message)

        # Format the message as a string and append it to the converted text list
        converted_message = f"{formatted_timestamp} - {sender}: {text}"
        if text != '':
            converted_text.append(converted_message)

    # Join the converted text messages into a single string
    output = '\n'.join(converted_text)

    # Remove the temporary file
    temp_file.close()
    os.remove(temp_file_path)

    # Return the converted text as a string
    return output