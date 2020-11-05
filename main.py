# coding: utf-8
"""
    GAN Project
"""
import argparse
from image_loader import ImageLoader
from cyclegan import CycleGan

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

datasets = ["ukiyoe2photo", "vangogh2photo", "cezanne2photo", "monet2photo"]

def main():
    _execute_command(args.execute)

def _execute_command(command):
    if command == 'train':
        _train()
    elif command == 'test':
        _test()

def _train():
    print('Starting training')
    for dataset in datasets:
        gan = CycleGan(dataset)
        gan.train(epochs=90, batch_size=1, sample_interval=1, saving_interval=30)
    print("Training complete")

def _test():
    print('Starting testing')
    for dataset in datasets:
        gan = CycleGan(dataset)
        gan.test()
    print("All fakes generated")
if __name__ == '__main__':
    main()


