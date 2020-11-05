# coding: utf-8
"""
    GAN Project
"""
import argparse
import subprocess

print("""\
     ██████╗██╗   ██╗ ██████╗██╗     ███████╗ ██████╗  █████╗ ███╗   ██╗
    ██╔════╝╚██╗ ██╔╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗████╗  ██║
    ██║      ╚████╔╝ ██║     ██║     █████╗  ██║  ███╗███████║██╔██╗ ██║
    ██║       ╚██╔╝  ██║     ██║     ██╔══╝  ██║   ██║██╔══██║██║╚██╗██║
    ╚██████╗   ██║   ╚██████╗███████╗███████╗╚██████╔╝██║  ██║██║ ╚████║
    ╚═════╝   ╚═╝    ╚═════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
        """)

def main():
    args = _initialize_args()

    if args.init:
        _initialize_data()

    _execute_command(args.execute)

def _execute_command(command):
    if command == 'train':
        _train()
    elif command == 'test':
        _test()

def _train():
    print('Train')

def _test():
    print('Test')

def _initialize_data():
    print('Downloading the training datasets...')
    subprocess.call(['./download_data.sh'])

def _initialize_args():
    parser = argparse.ArgumentParser(description='CycleGAN')
    parser.add_argument('-e', dest='execute', help='Select execution')

    add_boolean_arg(parser, 'init', help='Download the training data')

    args = parser.parse_args()
    return args

def add_boolean_arg(parser, name, help='', default=False, hasInverted=False):
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--' + name, dest=name, action='store_true')

    if hasInverted:
        group.add_argument('--no-' + name, dest=name, action='store_true')

    parser.set_defaults(**{name:default})

if __name__ == '__main__':
    main()


