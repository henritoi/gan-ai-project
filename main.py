# coding: utf-8
"""
    GAN Project
"""
import argparse
import subprocess
from input_helper import InputHelper
import os
from cyclegan import CycleGan

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

    if args.list:
        __print_local_datasets()
        return

    if args.init:
        __initialize_data()
        __print_local_datasets()
        return

    elif not os.path.isdir('datasets'):
        print('[WARNING]: You will need to download datasets to datasets folder!')
        print('You can initialize datasets using --init command or by running the download_data.sh script.\n')

        selection = input('Would you like to download datasets [Y/n]: ')
        if selection.lower() == 'y':
            __initialize_data()

    __execute_command(args.method, args.dataset, epochs=args.epochs)

def __execute_command(command=None, dataset=None, epochs=250):
    if command == None:
        command = __get_command_selection()

    if dataset == None:
        if command == 'train' or 'test':
            dataset = __get_dataset_selection() 
    else:
        if not os.path.isdir('datasets/%s' % dataset):
            print('[Error]: Dataset "%s" was not found!' % (dataset))
            print('You can initialize datasets using --init command or by running the download_data.sh script.\n')

            selection = input('Would you like to reinitialize datasets [Y/n]: ')
            if selection.lower() == 'y':
                __initialize_data()
            else:
                dataset = __get_dataset_selection()

    if command == 'train':
        __train(dataset, epochs=epochs)

    elif command == 'test':
        __test(dataset)

def __train(dataset, epochs=250):
    print('Train with %s' % (dataset.capitalize()))
    gan = CycleGan(dataset)
    gan.train(epochs=90, batch_size=1, sample_interval=30, saving_interval=40)
    print("Training complete")
def __test(dataset, epoch="finished"):
    print('Test with the latest model trained')
    gan = CycleGan(dataset)
    gan.test(epoch=epoch)
    print("Testing complete")
def __initialize_data():
    print('Downloading the training datasets...')
    subprocess.call(['./download_data.sh'])

def __initialize_args():
    parser = argparse.ArgumentParser(description='CycleGAN')
    __add_boolean_arg(parser, 'list', help='List downloaded datasets')
    parser.add_argument('-m', dest='method', help='Select metdod to be used')
    parser.add_argument('-e', dest='epochs', type=int, help='Number of epochs (default 250)', default=250)
    parser.add_argument('--data', dest='dataset', help='Select dataset to be used')
    __add_boolean_arg(parser, 'init', help='Download the training data and pictures of Kuopio')

    args = parser.parse_args()
    return args

def __add_boolean_arg(parser, name, help='', default=False, hasInverted=False):
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--' + name, dest=name, action='store_true', help=help)

    if hasInverted:
        group.add_argument('--no-' + name, dest=name, action='store_true')

    parser.set_defaults(**{name:default})

def __get_command_selection():
    input_helper = InputHelper(help='\nSelect command to be used:', options=['train', 'test'], default=0)
    command = input_helper.get_output()
    return command

def __get_dataset_selection():
    downloaded_datasets = __get_downloaded_datasets()
    input_helper = InputHelper(help='\nSelect training dataset to be used:', options=downloaded_datasets, default=0)
    dataset = input_helper.get_output()
    return dataset

def __print_local_datasets():
    datasets = __get_downloaded_datasets()
    if len(datasets) > 0:
        print('List of local datasets:')
        for index, item in enumerate(datasets):
            print('[%d]: %s' % (index, item.capitalize()))
        print('')
    else:
        print('No datasets found')

def __get_downloaded_datasets():
    ret = []
    if os.path.isdir('datasets/train'):
        datasets = os.listdir('datasets/train')
        for item in os.listdir('datasets/train'):
            if os.path.isdir('datasets/train/%s' % (item)):
                ret.append(item)
    return ret

if __name__ == '__main__':
    main()
