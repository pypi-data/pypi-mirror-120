# vton-imaterialist
A python package for Binary Segmentation DataSet ( vton_plus and imaterialist [topwear])

# Download dataset 

`Note - This step can be performed after installing package as well.`
```
#Download dataset from following drive and unzip it.
https://drive.google.com/drive/folders/1cGp0-s5p8n4oNnZr5AM_AaYCVzlJbkCo?usp=sharing
```

# Install package 

## Installation with pypi
```
pip3 install <Inprocess >
```
## Installation from source

```
git clone https://github.com/aarti-b/vton-imaterialist
python3 setup.py install
```

## Set path to use package outside directory

```
export PYTHONPATH="$PYTHONPATH:/path_to_github-clone-package/package/package/"

```

# Usage Guide

There are two datasets this package focuses on 
* vton
* imaterialist

## vton dataset
default option for dataset is **vton**. Follow the following commands to load data. assign path value to the folder where data is downloaded and unzipped.

### Load whole data
```
from vtonimat import SegData
images, labels = SegData(path='path_to_datafiles').load_training()
```
### Load batchwise dataset 
Load by batches. Following command returns list of batches. Batch size is input parameter in method `load_training_in_batches`. 

### Load whole data

```
from vton import SegData
images, labels = SegData().load_training_in_batches(1000)
```
## imaterialist'19 topwear dataset

```
from vtonimat import SegData
images, labels = SegData(path='path_to_datafiles', dataset='imat19').load_training()
```

### Load batchwise dataset 
Load by batches. Following command returns list of batches. Batch size is input parameter in method `load_training_in_batches`. 

```
from vton import SegData
images, labels = SegData().load_training_in_batches(1000)
```

There is a python file `convert.py` to convert dataset to ubyte format the dataset you downloaded from google drive link. This file converts 3D images and 2D labels images to ubyte format.

## Usage to convert data

```
python3 convert.py train 0    #0 is ratio, which means whole data is converted to train. you can add proportions.
python3 convert.py test 0
```