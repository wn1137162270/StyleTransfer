##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Created by: Hang Zhang
## ECE Department, Rutgers University
## Email: zhang.hang@rutgers.edu
## Copyright (c) 2017
##
## This source code is licensed under the MIT-style license found in the
## LICENSE file in the root directory of this source tree 
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
import sys
import time
import numpy as np
from tqdm import tqdm, trange

import torch
from torch.optim import Adam
from torch.autograd import Variable
from torch.utils.data import DataLoader

from torchvision import datasets
from torchvision import transforms

import mains
from option import Options

def main():
    # figure out the experiments type
    args = Options().parse()
    if args.subcommand is None:
        raise ValueError("ERROR: specify the experiment type")
    if args.cuda and not torch.cuda.is_available():
        raise ValueError("ERROR: cuda is not available, try running on CPU")


    if args.subcommand == "train":
        # Training the model 
        train(args)

    elif args.subcommand == 'eval':
        # Test the pre-trained model
        mains.evaluate(args)

    elif args.subcommand == 'optim':
        # Gatys et al. using optimization-based approach
        optimize(args)

    else:
        raise ValueError('Unknow experiment type')


if __name__ == "__main__":
   main()
