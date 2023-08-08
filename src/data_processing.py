from cryptography.fernet import Fernet
import base64

# Hardcoded key (just for assignment purposes)
key = base64.urlsafe_b64encode(b'abcdefghijklmnopqrstuvwxzy012345')
cipher_suite = Fernet(key)


def encrypt_data(data):
    """
    Encrypts the provided data using Fernet symmetric encryption.

    :param data: Original string data to be encrypted.
    :return: Encrypted string.
    """
    byte_data = data.encode()  # Convert string to bytes
    encrypted_data = cipher_suite.encrypt(byte_data)
    return encrypted_data.decode()  # Convert encrypted bytes back to string


def decrypt_data(data):
    """
    Decrypts the provided encrypted data using Fernet symmetric encryption.

    :param data: Encrypted string data.
    :return: Original decrypted string.
    """
    byte_data = data.encode()  # Convert encrypted string to bytes
    decrypted_data = cipher_suite.decrypt(byte_data)
    return decrypted_data.decode()  # Convert decrypted bytes back to string


def mask_data(data):
    """
    Encrypts the 'ip' and 'device_id' fields in the data.

    :param data: Dictionary containing user data.
    :return: Data with encrypted 'ip' and 'device_id' fields.
    """
    data['ip'] = encrypt_data(data['ip'])
    data['device_id'] = encrypt_data(data['device_id'])
    return data


def flatten_json(data):
    """
    Flattens and transforms the provided data to match the database schema.

    :param data: Dictionary containing user data.
    :return: Transformed data.
    """
    return {
        'user_id': data['user_id'],
        'device_type': data['device_type'],
        'masked_ip': data['ip'],
        'masked_device_id': data['device_id'],
        'locale': data['locale'],
        'app_version': int(''.join([i for i in data['app_version'] if i.isdigit()])),
        # Convert version string to integer
    }
