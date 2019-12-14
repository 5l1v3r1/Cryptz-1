#!/usr/bin/env python3
"""
Provides a number of encoders, decoders, encryptors and decryptors.

Created By r2dr0dn.
Improvements by Haxys.
Updated 2019.12.04.
"""

import base64
import binascii
import binhex
import datetime
import os
import random
import string
from tempfile import NamedTemporaryFile

try:
    from colorama import Fore, Style, init
    from Crypto.Cipher import AES
    from cryptography.fernet import Fernet
except ImportError:
    print(
        "ERROR: Missing required libraries.\n"
        "Install dependencies with: pip install -r requirements.txt"
    )
    exit(1)


init()
print(
    f"""{Fore.MAGENTA}
https://github.com/r2dr0dn
{Fore.CYAN}
 ####   #####   #   #  #####   #####  ######
#    #  #    #   # #   #    #    #        #
#       #    #    #    #    #    #       #
#       #####     #    #####     #      #
#    #  #   #     #    #         #     #
 ####   #    #    #    #         #    ######  {Fore.RED}v3.0{Style.RESET_ALL}
{Fore.CYAN}
made by: {Fore.RED}r2dr0dn{Style.RESET_ALL}
"""
)

# Global Variables
MENU_OPTIONS = list()


def get_input(color, message):
    return input(color + message + Style.RESET_ALL).encode()


def get_plaintext():
    return get_input(Fore.GREEN, "Enter plaintext message: ")


def get_encoded():
    return get_input(Fore.YELLOW, "Enter encoded message: ")


def get_filename():
    return get_input(Fore.MAGENTA, "Specify filename: ")


def get_password():
    return get_input(Fore.RED, "Enter encryption password: ")


def saved_as(filename):
    print(f"{Fore.YELLOW}Output saved as: {Style.RESET_ALL}{filename}\n")


def show_output(color, type, output):
    print(f"{color}{type}:{Style.RESET_ALL}\n{output}\n")


def show_encoded(output):
    show_output(Fore.YELLOW, "Encoded output", output)


def show_plaintext(output):
    show_output(Fore.GREEN, "Plaintext", output)


def ran_generator():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = 4
    keypass = "".join(random.choice(chars) for x in range(size, 20))
    return keypass


def hex_enc():
    """Encode to Hexadecimal."""
    plaintext = get_plaintext()
    output = binascii.hexlify(plaintext).decode()
    show_encoded(output)
MENU_OPTIONS.append(hex_enc)


def hex_dec():
    """Decode from Hexadecimal."""
    encoded_message = get_encoded()
    output = binascii.unhexlify(encoded_message).decode()
    show_plaintext(output)
MENU_OPTIONS.append(hex_dec)


def uu_enc():
    """Encode with uuencode."""
    plaintext = get_plaintext()
    output = binascii.b2a_uu(plaintext).decode()
    show_encoded(output)
MENU_OPTIONS.append(uu_enc)


def uu_dec():
    """Decode with uudecode."""
    encoded_message = get_encoded()
    output = binascii.a2b_uu(encoded_message).decode()
    show_plaintext(output)
MENU_OPTIONS.append(uu_dec)


def base64_enc():
    """Encode with Base64."""
    plaintext = get_plaintext()
    output = base64.b64encode(plaintext).decode()
    show_encoded(output)
MENU_OPTIONS.append(base64_enc)


def base64_dec():
    """Decode with Base64."""
    encoded_message = get_encoded()
    output = base64.b64decode(encoded_message).decode()
    show_plaintext(output)
MENU_OPTIONS.append(base64_dec)


def binhex_enc():
    """Encode with BinHex4."""
    temp_filename = f"temp_{ran_generator()}"
    with open(temp_filename, "wb") as outfile:
        outfile.write(get_plaintext())
    dest_filename = get_filename().decode()
    binhex.binhex(temp_filename, dest_filename)
    os.unlink(temp_filename)
    saved_as(dest_filename)
MENU_OPTIONS.append(binhex_enc)


def binhex_dec():
    """Decode with BinHex4."""
    temp_filename = f"temp_{ran_generator()}"
    binhex.hexbin(get_filename().decode(), temp_filename)
    with open(temp_filename, "rb") as infile:
        show_plaintext(infile.read().decode())
    os.unlink(temp_filename)
MENU_OPTIONS.append(binhex_dec)


def fernet_enc():
    """Encrypt with Fernet. (Symmetric)"""
    data = get_plaintext()
    key = Fernet.generate_key()
    e = Fernet(key)
    encry = e.encrypt(data)
    encry = encry.decode()
    key = key.decode()
    print(Fore.RED + "Your Decryption password: [%s]" % key)
    print("\n" + Fore.GREEN + "Encryption Value [%s]" % encry + "\n")
#MENU_OPTIONS.append(fernet_enc)


def fernet_dec():
    """Decrypt with Fernet. (Symmetric)"""
    encr = get_encoded()
    password = get_password()
    D = Fernet(password)
    decr = D.decrypt(encr)
    decr = decr.decode()
    print("\n" + Fore.RED + "Decrypted Value: [%s]" % decr + "\n")
#MENU_OPTIONS.append(fernet_dec)


def aes_enc_manual():
    """Encrypt with AES. (Manual)"""
    keypass = ran_generator()
    keypass2 = keypass
    data = get_plaintext()
    keypass = keypass.encode()
    cipher = AES.new(keypass, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    print(Fore.GREEN + "\n" + "Encryption Password: {}".format(keypass2))
    print(
        Fore.BLUE
        + "\n"
        + f"Your Encryption: Ciphertext: {ciphertext}\n"
        + f"Tag: {tag}\nNonce: {cipher.nonce}\n"
        + f"Please Save Them All Somewhere Safe"
        + Style.RESET_ALL
        + "\n"
    )
# Uncomment the following line once you have a working decryptor.
# MENU_OPTIONS.append(aes_enc_manual)


# def aes_dec_manual():
#     """Decrypt with AES. (Manual)"""
#     try:
#         keypass = get_password()
#         tag = input('Enter Tag: ')
#         # tag = tag.encode()
#         tag = str.encode(tag)
#         ciphertext = input("Enter CipherText: ")
#         # ciphertext = ciphertext.encode()
#         ciphertext = str.encode(ciphertext)
#         nonce = input("Enter Nonce: ")
#         # nonce = nonce.encode()
#         nonce = str.encode(nonce)
#         cipher = AES.new(keypass, AES.MODE_EAX, nonce)
#         data = cipher.decrypt_and_verify(ciphertext, tag)
#         data = data.decode()
#         print("\n" + Fore.RED + data + Style.RESET_ALL + "\n")
#     except ValueError:
#         print("Unmatched Value!!!")
#         exit(1)
# MENU_OPTIONS.append(aes_dec_manual)


def rsa_enc_manual():
    """Encrypt with RSA. (Manual)"""
    data = get_plaintext()
    BLOCK_SIZE = 16
    PADDING = "{"
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    secret = ran_generator()
    passphrase = secret
    secret = str.encode(secret)
    cipher = AES.new(secret)
    encoded = EncodeAES(cipher, data)
    encoded = bytes.decode(encoded)
    print(Fore.CYAN + "\n" + "encryption key:" + passphrase + "\n")
    print(
        Fore.WHITE + Style.DIM + "Encrypted Data: ",
        encoded + "\n" + Style.RESET_ALL,
    )
# Uncomment the following line once you have a working decryptor.
# MENU_OPTIONS.append(rsa_enc_manual)


def aes_enc_auto():
    """Encrypt with AES. (Automatic)"""
    data = get_plaintext()
    data = data.encode()
    filename = get_input(
        Fore.YELLOW, "Enter output filename: "
    )
    keypass = ran_generator()
    keypass2 = keypass
    keypass = keypass.encode()
    cipher = AES.new(keypass, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    file_out = open(filename + ".enc", "wb")
    [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
    saved_pass = open(filename + ".txt", "w")
    saved_pass.write(keypass2 + "\n")
    saved_pass.close()
    print(
        Fore.WHITE
        + Style.DIM
        + "\nUse "
        + Style.NORMAL
        + Fore.RED
        + f"[{keypass2}] "
        + Fore.WHITE
        + Style.DIM
        + "To Decrypt Your Data"
        + Style.RESET_ALL
    )
    print(
        Fore.GREEN
        + "Data Has Been Saved In"
        + Fore.RED
        + "[%s.enc] \n" % (filename)
    )
#MENU_OPTIONS.append(aes_enc_auto)


def aes_dec_auto():
    """Decrypt with AES. (Automatic)"""
    filename = input(
        Fore.RED
        + "Enter Encrypted Data File (make sure it on the same path): "
    )
    file_in = open(filename, "rb")
    keypass = get_password()
    nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
    cipher = AES.new(keypass, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    data = data.encode()
    print(Fore.MAGENTA + "\n" + "Decrypted: " + data + Style.RESET_ALL + "\n")
#MENU_OPTIONS.append(aes_dec_auto)


# Main Function
def main():
    try:
        while True:
            print(
                Fore.CYAN
                + "Choose from the following options, or press Ctrl-C to quit."
                + Style.RESET_ALL
            )
            for index in range(len(MENU_OPTIONS)):
                print(
                    f"{index + 1}. {' ' if index < 9 else ''}"
                    f"{MENU_OPTIONS[index].__doc__}"
                )
            choice = get_input(Fore.CYAN, "CRYPTZ -> ")
            print()
            try:
                MENU_OPTIONS[int(choice) - 1]()
            except IndexError:
                print(Fore.RED + "Unknown option.")
    except KeyboardInterrupt:
        print(
            f"\n{Fore.RED}Program terminated. "
            f"{Fore.WHITE}{Style.BRIGHT}Have a nice day!"
            f"{Style.RESET_ALL}"
        )
        exit(1)


if __name__ == "__main__":
    main()
