# coding: utf-8
"""
    GAN Project
"""
import argparse
import subprocess
from input_helper import InputHelper
import os

print("""\n\
     ██████╗██╗   ██╗ ██████╗██╗     ███████╗ ██████╗  █████╗ ███╗   ██╗
    ██╔════╝╚██╗ ██╔╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗████╗  ██║
    ██║      ╚████╔╝ ██║     ██║     █████╗  ██║  ███╗███████║██╔██╗ ██║
    ██║       ╚██╔╝  ██║     ██║     ██╔══╝  ██║   ██║██╔══██║██║╚██╗██║
    ╚██████╗   ██║   ╚██████╗███████╗███████╗╚██████╔╝██║  ██║██║ ╚████║
    ╚═════╝   ╚═╝    ╚═════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
        """)

def main():
    args = __initialize_args()

    if args.init:
        __initialize_data()
    elif not os.path.isdir('datasets'):
        print('[WARNING]: You will need to download datasets to datasets folder!')
        print('You can initialize datasets using --init command or by running the download_data.sh script.\n')

        selection = input('Would you like to download datasets [Y/n]: ')
        if selection.lower() == 'y':
            __initialize_data()

    __execute_command(args.execute, args.dataset)

def __execute_command(command=None, dataset=None):
    if command == None:
        command = __get_command_selection()

    if dataset == None:
        dataset = __get_dataset_selection() 
    else:
        if not os.path.isdir('datasets/%s' % dataset):
            print('[Error]: Dataset "%s" was not fould!' % (dataset))
            print('You can initialize datasets using --init command or by running the download_data.sh script.\n')

            selection = input('Would you like to reinitialize datasets [Y/n]: ')
            if selection.lower() == 'y':
                __initialize_data()
            else:
                print('[Error]: No valid dataset found.')
                return

    if command == 'train':
        __train(dataset)

    elif command == 'test':
        __test(dataset)

def __train(dataset):
    print('Train with %s' % (dataset.capitalize()))

def __test(dataset):
    print('Test with %s' % (dataset.capitalize()))

def __initialize_data():
    print('Downloading the training datasets...')
    subprocess.call(['./download_data.sh'])

def __initialize_args():
    parser = argparse.ArgumentParser(description='CycleGAN')
    parser.add_argument('-e', dest='execute', help='Select execution')
    parser.add_argument('--data', dest='dataset', help='Select execution')
    __add_boolean_arg(parser, 'init', help='Download the training data')

    args = parser.parse_args()
    return args

def __add_boolean_arg(parser, name, help='', default=False, hasInverted=False):
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--' + name, dest=name, action='store_true')

    if hasInverted:
        group.add_argument('--no-' + name, dest=name, action='store_true')

    parser.set_defaults(**{name:default})

def __get_command_selection():
    input_helper = InputHelper(help='\nSelect command to be used:', options=['train', 'test'], default=0)
    command = input_helper.get_output()
    return command

def __get_dataset_selection():
    input_helper = InputHelper(help='\nSelect training dataset to be used:', options=['monet2photo', 'cezanne2photo', 'ukiyoe2photo', 'vangogh2photo' ], default=0)
    dataset = input_helper.get_output()
    return dataset


if __name__ == '__main__':
    main()
