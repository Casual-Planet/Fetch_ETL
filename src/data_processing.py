import base64
import json
from cryptography.fernet import Fernet


cipher_suite = Fernet(base64.urlsafe_b64encode(b'abcdefghijklmnopqrstuvwxzy012345'))


def encrypt_data(data):
    """
    Encrypts the provided data using Fernet symmetric encryption.

    :param data: Original string data to be encrypted.
    :return: Encrypted string.
    """
    byte_data = data.encode()  # Convert the provided string into bytes
    encrypted_data = cipher_suite.encrypt(byte_data)  # Encrypt the byte data
    return encrypted_data.decode()  # Convert the encrypted byte data back to string and return


def decrypt_data(data):
    """
    Decrypts the provided encrypted data using Fernet symmetric encryption.

    :param data: Encrypted string data.
    :return: Original decrypted string.
    """
    byte_data = data.encode()  # Convert the encrypted string into bytes
    decrypted_data = cipher_suite.decrypt(byte_data)  # Decrypt the byte data
    return decrypted_data.decode()  # Convert the decrypted byte data back to string and return


def mask_data(data):
    """
    Encrypts the 'ip' and 'device_id' fields in the data.

    :param data: Dictionary containing user data.
    :return: Data with encrypted 'ip' and 'device_id' fields.
    """

    # Check if the provided data is a string and try to parse it into a JSON format
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print("Error decoding JSON. The provided string is not a valid JSON format.")
            return {}  # If an error occurs during JSON decoding, return an empty dictionary

    # Ensure that the data is a dictionary before proceeding
    if not isinstance(data, dict):
        print("Unexpected data format:", type(data))
        return {}  # If data isn't a dictionary, return an empty dictionary

    ip_data = data.get('ip', 'DEFAULT_IP')  # Fetch the IP from the data or set a default IP if not found
    device_id_data = data.get('device_id',
                              'DEFAULT_DEVICE_ID')  # Fetch the device ID from the data or set a default one if not found

    data['ip'] = encrypt_data(ip_data)  # Encrypt the IP
    data['device_id'] = encrypt_data(device_id_data)  # Encrypt the device ID

    return data  # Return the updated dictionary with encrypted fields


def flatten_json(data):

    # Check if the provided data is a string and try to parse it into a JSON format
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print("Error decoding JSON. The provided string is not a valid JSON format.")
            return {}  # If an error occurs during JSON decoding, return an empty dictionary

    # Ensure that the data is a dictionary before proceeding
    if not isinstance(data, dict):
        print("Unexpected data format:", type(data))
        return {}  # If data isn't a dictionary, return an empty dictionary

    ip_data = data.get('ip', 'DEFAULT_IP')  # Fetch the IP from the data or set a default IP if not found
    device_id_data = data.get('device_id', 'DEFAULT_DEVICE_ID')  # Fetch the device ID from the data or set a default one if not found

    # Encrypt the IP and device ID fields
    masked_ip = encrypt_data(ip_data)
    masked_device_id = encrypt_data(device_id_data)

    app_version = None
    if 'app_version' in data:
        app_version = int(''.join([i for i in data['app_version'] if i.isdigit()]))

    return {
        'user_id': data['user_id'],
        'device_type': data.get('device_type', 'DEFAULT_DEVICE_TYPE'),
        'masked_ip': masked_ip,
        'masked_device_id': masked_device_id,
        'locale': data.get('locale', 'DEFAULT_LOCALE'),
        'app_version': app_version
    }