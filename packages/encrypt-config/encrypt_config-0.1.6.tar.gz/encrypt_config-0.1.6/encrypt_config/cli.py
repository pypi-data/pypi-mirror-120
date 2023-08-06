"""Console script for encrypt_config."""
import argparse
import json
import os
import sys

from encrypt_config.encrypt_config import JSONFernetFileConfig


def fernet_encrypt(source_file, output_file, key_file=None):
    with open(source_file, 'r') as json_file:
        clear_text_dict = json.load(json_file)

    json_fernet_config = JSONFernetFileConfig()
    encrypted_dict, key = json_fernet_config.write(output_file, clear_text_dict)
    return encrypted_dict, key

def serialize_key(output_file, key):
    with open(output_file, 'w') as txt:
        txt.write(key)


def main():
    """Console script for encrypt_config."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source-file", help="Source file")
    parser.add_argument("-o", "--output-file", help="Output file")
    parser.add_argument("-k", "--key-file", help="Key file")
    parser.add_argument("-e", "--encrypt", help="Encrypt action", action='store_true')
    parser.add_argument("-d", "--decrypt", help="Decrypt action", action='store_true')
    args = parser.parse_args()

    print("Arguments: " + str(args))
    # sys.exit(main())  # pragma: no cover
    if args.encrypt:
        output_file = args.output_file
        key_file = args.key_file
        if args.output_file is None:
            path, file = os.path.split(args.source_file)
            output_file = os.path.join(path, f'encrypted_{file}')
            print(f'>>>Output file {output_file}')
        if key_file is None:
            path, file = os.path.split(args.source_file)
            key_file = os.path.join(path, 'key.txt')

        enc_dict, key = fernet_encrypt(args.source_file, output_file)
        serialize_key(key_file, key)
        sys.stdout.write(f'Encrypted file to {output_file}')


    return 0



if __name__ == "__main__":

    """Console script for encrypt_config."""

    sys.exit(main())