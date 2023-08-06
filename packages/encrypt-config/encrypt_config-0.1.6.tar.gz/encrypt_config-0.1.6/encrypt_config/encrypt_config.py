"""Main module."""
from abc import ABC, abstractmethod
import json

from cryptography.fernet import Fernet


class EncryptedConfig(ABC):
    @abstractmethod
    def encrypt_config(self, config_data, keys_to_encrypt=None):
        pass

    @abstractmethod
    def decrypt_config(self, config_data, keys_to_encrypt=None):
        pass


class FileConfig(ABC):

    @abstractmethod
    def read(self, filename, encrypted_keys=None, **kwargs):
        pass

    @abstractmethod
    def write(self, filename, data, keys_to_encrypt=None):
        pass


class JSONFernetFileConfig(FileConfig):  # noqa

    def __init__(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], str):
            key = args[0].encode()
            self.fernet_config = FernetEncryptedConfig(key)
        elif len(args) > 0 and isinstance(args[0], bytes):
            key = args[0]
            self.fernet_config = FernetEncryptedConfig(key)
        else:
            self.fernet_config = FernetEncryptedConfig()

    def read(self, filename, encrypted_keys=None, **kwargs):
        if kwargs.get('fernet_key'):
            self.fernet_config = FernetEncryptedConfig(kwargs['fernet_key'])

        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        unencrypted_data = self.fernet_config.decrypt_config(data, encrypted_keys=encrypted_keys)
        return unencrypted_data, self.fernet_config.key.decode()

    def write(self, filename, data, keys_to_encrypt=None):
        encrypted_data = self.fernet_config.encrypt_config(data, keys_to_encrypt=keys_to_encrypt)
        with open(filename, 'w') as json_file:
            json.dump(encrypted_data, json_file)
        return encrypted_data, self.fernet_config.key.decode()


class FernetEncryptedConfig(EncryptedConfig): # noqa

    def __init__(self, *args, **kwargs):
        if len(args) > 0 and isinstance(args[0], str):
            self.key = args[0].encode()
        elif len(args) > 0 and isinstance(args[0], bytes):
            self.key = args[0]
        else:
            self.key = Fernet.generate_key()
        # Instance the Fernet class with the key
        self.fernet = Fernet(self.key)  # noqa

    def encrypt_config(self, config_data, keys_to_encrypt=None):
        encrypted_data = config_data.copy()
        if keys_to_encrypt is None:
            keys_to_encrypt = config_data.keys()
        for key in config_data.keys():
            if key in keys_to_encrypt and isinstance(config_data[key], str):
                encrypted_data[key] = self.fernet.encrypt(config_data[key].encode()).decode()
        return encrypted_data

    def decrypt_config(self, config_data, encrypted_keys=None):
        decrypted_data = config_data.copy()
        if encrypted_keys is None:
            encrypted_keys = config_data.keys()
        for key in config_data.keys():
            if key in encrypted_keys and isinstance(config_data[key], str):
                decrypted_data[key] = self.fernet.decrypt(config_data[key].encode()).decode()
        return decrypted_data
