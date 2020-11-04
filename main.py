# coding: utf-8
"""
    GAN Project
"""
import argparse

print("""\
     ██████╗██╗   ██╗ ██████╗██╗     ███████╗ ██████╗  █████╗ ███╗   ██╗
    ██╔════╝╚██╗ ██╔╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗████╗  ██║
    ██║      ╚████╔╝ ██║     ██║     █████╗  ██║  ███╗███████║██╔██╗ ██║
    ██║       ╚██╔╝  ██║     ██║     ██╔══╝  ██║   ██║██╔══██║██║╚██╗██║
    ╚██████╗   ██║   ╚██████╗███████╗███████╗╚██████╔╝██║  ██║██║ ╚████║
    ╚═════╝   ╚═╝    ╚═════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
        """)

parser = argparse.ArgumentParser(description='CycleGAN')
parser.add_argument('-e', dest='execute', help='Select execution')

args = parser.parse_args()

def main():
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

if __name__ == '__main__':
    main()


