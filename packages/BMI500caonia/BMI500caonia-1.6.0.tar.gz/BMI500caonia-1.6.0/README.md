# The Kmeans unsupervised clustering package

# Contents
This package is an example Kmeans' package for BMI500's project in Emory University. The package will automatically download the iris data collected from UCI. The dataset contains three classes of flowers, and the clustering algorithm is to seperate each group of the flowers. It does not necessary tell you what kind of flower is, but will tell you which flowers are in a same group.

# FAQ

## How to install?

In your command line, type "pip install BMI500caonia"

## How to use

python

from BMI500caonia import BMI500clustering

BMI500clustering.Kmeans_run()

## Running time and hardware requirement

The running time is 14 seconds in Titan'x 12 GB gpu and Intel Iris 16 GB cpu. 

## Future work

The function should be modified to be more flexible in the future, so the user can customize parameters. 