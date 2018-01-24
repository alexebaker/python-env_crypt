import argparse

import main


def parse_args():
    parser = argparse.ArgumentParser(
        description='Tool for encrypting and decrypting environment variables.')

    parser.add_argument(
        '--env-path', '-e',
        type=str,
        default='.env',
        help='Path to the env file to use for encryption/decryption.')

    parser.add_argument(
        '--password', '-p',
        type=str,
        help='Password to use for encryption/decryption.')

    parser.add_argument(
        '--keyfile', '-f',
        type=str,
        help='Path to the key file to use for encryption/decryption.')

    subparser = parser.add_subparsers()

    enc_parser = subparser.add_parser(
        'encrypt',
        help='Encrypt an env file in place.')

    enc_parser.set_defualts(func=main.encrypt_env)

    dec_parser = subparser.add_parser(
        'decrypt',
        help='Decrypt an env file in place.')

    dec_parser.set_defualts(func=main.decrypt_env)

    update_parser = subparser.add_parser(
        'update',
        help='Update an encrypted env file in place.')

    update_parser.add_argument(
        '--key', '-k',
        type=str,
        help='Environment key value to update.')

    update_parser.add_argument(
        '--value', '-v',
        type=str,
        help='Value to set the key to.')

    update_env.set_defualts(func=main.update_env)

    list_parser = subparser.add_parser(
        'list',
        help='List the current encrypted env values.')

    list_parser.set_defualts(func=main.list_env)

    load_parser = subparser.add_parser(
        'load',
        help='Load an encrypted env file into the current environment.')

    load_parser.set_defualts(func=main.load_env)
    return parser.parse_args()
