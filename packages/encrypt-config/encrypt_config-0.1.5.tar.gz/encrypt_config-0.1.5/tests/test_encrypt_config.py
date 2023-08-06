#!/usr/bin/env python

"""Tests for `encrypt_config` package."""
import json
import os
import tempfile

import pytest

from encrypt_config.encrypt_config import FernetEncryptedConfig, JSONFernetFileConfig


@pytest.fixture
def fernet_key():
    # enc_config = FernetEncryptedConfig()
    # print(enc_config.key.decode())
    # return enc_config.key
    key = 'ZD1g-k09xoZ2h8v2QqgIAnyW-UZUBkSDKE93Ks1fBdI='
    return key


@pytest.fixture
def simple_dict():
    data = {'username': 'batman_4', 'password': 'MyP8998KK-;/', 'favorite_port': 3455}
    return data


def test_fernet_encryption(simple_dict):
    enc_config = FernetEncryptedConfig()
    enc_data = enc_config.encrypt_config(simple_dict)
    dec_data = enc_config.decrypt_config(enc_data)
    assert len(simple_dict) == len(enc_data)
    assert len(simple_dict) == len(dec_data)
    for key in simple_dict.keys():
        assert dec_data[key] == simple_dict[key]
        if isinstance(simple_dict[key], str):
            assert enc_data[key] != simple_dict[key]


def test_fernet_decrypt(fernet_key, simple_dict):
    enc_config = FernetEncryptedConfig(fernet_key)
    enc_data = enc_config.encrypt_config(simple_dict)
    dec_data = enc_config.decrypt_config(enc_data)
    assert len(simple_dict) == len(enc_data)
    assert len(simple_dict) == len(dec_data)
    for key in simple_dict.keys():
        assert dec_data[key] == simple_dict[key]
        if isinstance(simple_dict[key], str):
            assert enc_data[key] != simple_dict[key]


def test_write_files(fernet_key, simple_dict):
    manager = JSONFernetFileConfig(fernet_key)
    # filename = '../output/simple_dict.json'
    new_file, filename = tempfile.mkstemp()
    print(f'Filename: {filename}')
    #if os.path.exists(filename):
    #    os.remove(filename)

    encrypted, key = manager.write(filename, simple_dict)
    assert fernet_key == key
    assert os.path.exists(filename)

    with open(filename, 'r') as json_file:
        encrypted_from_file = json.load(json_file)

    assert encrypted_from_file.keys() == simple_dict.keys()

    decrypted, dec_key = manager.read(filename)
    assert decrypted == simple_dict
