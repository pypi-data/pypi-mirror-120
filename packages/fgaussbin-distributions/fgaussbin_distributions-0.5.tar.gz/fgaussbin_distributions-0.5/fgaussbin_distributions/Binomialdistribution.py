# import necessary libraries
import math
import matplotlib.pyplot as plt
from functools import reduce
from .Generaldistribution import Distribution


# Binomial class that inherits from the Distribution class
class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
                
    """
    #       A binomial distribution is defined by two variables: 
    #           the probability of getting a positive outcome and
    #           the number of trials
    
    #       If you know these two values, you can calculate the mean and the standard deviation
    #       
    #       For example, if you flip a fair coin 25 times, p = 0.5 and n = 25
    #       You can then calculate the mean and standard deviation with the following formula:
    #           mean = p * n
    #           standard deviation = sqrt(n * p * (1 - p))
    
    #       


    # define the init function
    def __init__(self, prob = None, size = None):
        """store the probability of the distribution in an instance variable p
           store the size of the distribution in an instance variable n
        """
        mu = None
        sigma = None
        
        self.p = prob
        self.n = size
        
        # define mean and stdev attributes from Distribution class
        if (prob and size != None):
            Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
        else:
            Distribution.__init__(self, mu, sigma)
 


    # define a method calculate_mean() according to the specifications below
    def calculate_mean(self):
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
        """
        self.mean = self.p * float(self.n)
        return self.mean

    

    # define a calculate_stdev() method accordin to the specifications below.
    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
        """
        self.stdev = math.sqrt(self.p * float(self.n) * (1 - self.p))
        return self.stdev

    
            
    # define a replace_stats_with_data() method according to the specifications below.
    # The read_data_file() from the Generaldistribution class can read in a data file.
    # Because the Binomaildistribution class inherits from the Generaldistribution class,
    # you don't need to re-write this method.
    # However, the method doesn't update the mean or standard deviation of a distribution.
    # Hence you are going to write a method that calculates n, p, mean and standard
    # deviation from a data set and then updates the n, p, mean and stdev attributes.
    # Assume that the data is a list of zeros and ones like [0 1 0 1 1 0 1]
    def replace_stats_with_data(self):
        """Function to calculate n, p, mean and standard deviation from the data set.
           The function updates the p and n variables of the object.
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """
        self.n = len(self.data)
        self.p = sum(x == 1 for x in self.data) / len(self.data)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        
        return self.p, self.n
        #       Write code that: 
        #           updates the n attribute of the binomial distribution
        #           updates the p value of the binomial distribution by calculating the
        #               number of positive trials divided by the total trials
        #           updates the mean attribute
        #           updates the standard deviation attribute
        #
        #       Hint: You can use the calculate_mean() and calculate_stdev() methods
        #           defined previously.
        
      
        
    # define a method plot_bar() that outputs a bar chart of the data set according to the following specifications.
    def plot_bar(self):
        """Function to output a histogram of the instance variable data 
           using matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        plt.bar(self.data)
        plt.title('Bar plot')
        plt.xlabel('data')
        plt.ylabel('count')
        plt.show()
        
        
    
    # Calculate the probability density function of the binomial distribution
    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        # define inner function factorial() to calculate nfactorial, (n-k)factorial, and kfactorial
        def factorial(n):
            if n < 2:
                return 1
            else:
                return reduce(lambda x, y: x * y, range(2, int(n) + 1))
            
        # clculate the pdf
        q = 1.0 - self.p
        prob = (factorial(self.n) / (factorial(self.n - k) * factorial(k))) * (self.p**k) * (q**(self.n - k))

        return prob
 


    # define a method to plot the probability density function of the binomial distribution
    def plot_bar_pdf():
        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        x_values = list(range(0, len(self.data) + 1))
        y_values = list(map(pdf, x_list))
        
        plt.bar(x_values, y_values)
        plt.title('Probability density plot')
        plt.xlabel('number of success outcomes')
        plt.ylabel('density')
        plt.show()
        
        return x_values, y_values



    # define a method to output the sum of two binomial distributions. Assume both distributions have the same p value
    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """

        try:
            assert self.p == other.p, "can't sum distributions: p values are not equal"
        except AssertionError as error:
            raise
        
        result = Binomial()
        result.n = self.n + other.n
        result.p = self.p
        
        return result
        
        # Define addition for two binomial distributions. Assume that the
        # p values of the two distributions are the same. The formula for 
        # summing two binomial distributions with different p values is more complicated,
        # so you are only expected to implement the case for two distributions with equal p.
        
        # the try, except statement above will raise an exception if the p values are not equal
        
        # Hint: When adding two binomial distributions, the p value remains the same
        #   The new n value is the sum of the n values of the two distributions.
 



    # use the __repr__ magic method to output the characteristics of the binomial distribution object.
    def __repr__(self):
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial object
        
        """
        return "mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n)
        #       Define the representation method so that the output looks like
        #       mean 5, standard deviation 4.5, p .8, n 20

    

