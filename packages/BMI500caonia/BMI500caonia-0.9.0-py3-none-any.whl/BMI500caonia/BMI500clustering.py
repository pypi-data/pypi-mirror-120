# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 17:42:33 2021

@author: Shaoyan Pan

Version 1.0.0

This is the algorithm for K-means clustering algorithm. With the dataset collected from UCI's iris data' which has
three classes.



"""

#Add the packages
import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
 

#Download dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

# Assign colum names to the dataset. 'code' is just convert the categorical values to numberical
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class']
dataset = pd.read_csv(url, names=names)
dataset.Class = pd.Categorical(dataset.Class)
dataset['code'] = dataset.Class.cat.codes


#X are input featrues, and Y are labels
X = dataset.iloc[:,0:4].to_numpy()
Y = dataset.iloc[:,4].to_numpy()


#Kmean's function: x is input, k is k means, epoch is iterations, random_state means
# how many time we randomly initialize the K mean. Each initilization produce a cluster, and 
# we only select the one with minimum distance with their centroids
def kmeans(x,k, epoch,random_state):
    total_points = []
    total_distance = np.zeros([random_state])
    for jnd in range(random_state):
        #Initialize the K means Centroids 
        ind = np.random.choice(len(x), k, replace=False)
        centroids = x[ind, :] 
         
        #Calculate the distance between the centroid and all other data points
        distance = cdist(x, centroids ,'euclidean') 
         
        #Centroid with the minimum Distance
        points = np.zeros([1,len(x)])
        for i in range(len(x)):
            points[0,i] = distance[i,:].argmin()
         
        #Repeating the above steps for n epochs
        for _ in range(epoch): 
            centroids = []
            for idx in range(k):
                #Updating Centroids
                temp_cent = x[np.squeeze(points==idx),:].mean(axis=0) 
                centroids.append(temp_cent)
     
            centroids = np.vstack(centroids) #Updated Centroids 
             
            distances = cdist(x, centroids ,'euclidean')
            points = np.array([np.argmin(i) for i in distances])
        
        #record the sum of distances from each initilization
        total_distance[jnd] = np.sum((x[np.squeeze(points==0),:]-centroids[0])**2)
        +np.sum((x[np.squeeze(points==1),:]-centroids[1])**2)
        +np.sum((x[np.squeeze(points==2),:]-centroids[2])**2)
        #record the cluster from each initilization
        total_points.append(points)
    
    #only return the one with minimun sum of distance
    return total_points[total_distance.argmin()] 

def main():
    label = kmeans(X,3,1000,20)
    print(dataset['code'].tolist())
    print(label)
    print('Accuracy = '+ str(np.sum(dataset['code'].tolist()==label)/len(label)*100)+'%')