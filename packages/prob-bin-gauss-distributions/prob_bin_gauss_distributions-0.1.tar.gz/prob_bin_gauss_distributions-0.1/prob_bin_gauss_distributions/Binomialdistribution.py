import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution
import math
import numpy as np
import pandas as pd
import random

class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials
    
    
    TODO: Fill out all TODOs in the functions below
            
    """
        
    def __init__(self, prob=1, size=1):
        
        self.p = prob
        self.n = size
        self.data = []
   
    def calculate_mean(self):
            
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        mean = self.p * self.n
        self.mean = mean
        return self.mean
    
    def calculate_stdev(self):
        
        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        stdev = math.sqrt(self.n * self.p * (1 - self.p))
        self.stdev = stdev
        return self.stdev 
        
        
    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """        
        
   
        self.read_data_file('numbers_binomial.txt')
        self.p = self.data.count(1)/len(self.data)
        self.n = len(self.data)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p, self.n
        
        
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        
        data = pd.Series(self.data)
        counts = data.value_counts()
        plt.bar(x=counts.index, height=counts.values)
        plt.xticks(counts.index)
        plt.xlabel('Zero or One')
        plt.ylabel('Frequency')
        plt.title('Zero vs. One Frequency')
        plt.show()
    
        
    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        
        return math.factorial(self.n)/(math.factorial(k)*math.factorial(self.n - k))*(self.p**k)*(1-self.p)**(self.n-k)
           

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        x_list = []
        y_list = []
        for k in range(0, n.self+1):
                x_list.append(k)
                y_list.append(self.pdf(k))
        plt.bar(x=x_list, height=y_list)
        plt.xticks(x_list)
        plt.xlabel('Amount of matches')
        plt.ylabel('Probability for amount of matches')
        plt.title('Amount of matches and their probabilities')
        plt.show()
        return x_list, y_list
        
                
    def __add__(self, other):
        
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
            binomial_result = Binomial()
            binomial_result.n = self.n + other.n
            binomial_result.p = other.p
            binomial_result.calculate_mean()
            binomial_result.calculate_stdev()
            
            
        except AssertionError as error:
            raise

                
        return binomial_result
        
        
    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
        
        return f'mean {self.mean}, standard deviation {self.stdev}, p {self.p}, n {self.n}'