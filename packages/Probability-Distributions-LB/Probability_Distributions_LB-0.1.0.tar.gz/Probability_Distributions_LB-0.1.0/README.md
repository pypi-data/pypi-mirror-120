
This project calculates and visualizes Gaussian and Binomial Distribution.
To use After installation  import Gaussian and or Binomial from Probability_Distribution_LB.

Details of Attributes and Methods for the Binomial and Gaussian classes are below.

Class Gaussian
This is a Gaussian distribution class for calculating and visualizing a Gaussian distribution. This class inherits from Distribution class.

	Attributes:
			mean (float) representing the mean value of the distribution
			stdev (float) representing the standard deviation of the distribution
			data_list (list of floats) a list of floats extracted from the data file
			

	Methods:

		calculate_mean():
		
			To calculate the mean of the data set.
			
			Args: 
				None
			
			Returns: 
				float: mean of the data setcalculate_mean(self):
		
			
		calculate_stdev(self, sample=True):

			To calculate the standard deviation of the data set.
			
			Args: 
				sample (bool): whether the data represents a sample or population
			
			Returns: 
				float: standard deviation of the data set

		pdf(self, x):
			Probability density function calculator for the gaussian distribution.
			
			Args:
				x (float): point for calculating the probability density function
				
			
			Returns:
				float: probability density function output

		plot_histogram_pdf(self, n_spaces = 50):

			To plot the normalized histogram of the data and a plot of the 
			probability density function along the same range
			
			Args:
				n_spaces (int): number of data points 
			
			Returns:
				list: x values for the pdf plot
				list: y values for the pdf plot

		__add__(other):
		
			To add together two Gaussian distributions
			
			Args:
				other (Gaussian): Gaussian instance
				
			Returns:
				Gaussian: Gaussian distribution

		__repr__():
	
			To output the characteristics of the Gaussian instance
			
			Args:
				None
			
			Returns:
				string: characteristics of the Gaussian


Class Binomial
This is a Binomial distribution class for calculating and visualizing a Binomial distribution. it Inherits from the Distribution Class
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) number of trials            

    Methods: 

    	calculate_mean()
    
	        To calculate the mean from p and n
	        
	        Args: 
	            None
	        
	        Returns: 
	            float: mean of the data set

	    calculate_stdev()

	        To calculate the standard deviation from p and n.
	        
	        Args: 
	            None
	        
	        Returns: 
	            float: standard deviation of the data set

	    replace_stats_with_data():
    
	        To calculate p and n from the data set
	        
	        Args: 
	            None
	        
	        Returns: 
	            float: the p value
	            float: the n value

	    plot_bar():
	        To to output a histogram of the instance variable data using 
	        matplotlib pyplot library.
	        
	        Args:
	            None
	            
	        Returns:
	            None
	        """

	    pdf(k):
	        Probability density function calculator for the binomial distribution.
	        
	        Args:
	            x (float): point for calculating the probability density function
	            
	        
	        Returns:
	            float: probability density function output


        plot_bar_pdf():

	        To plot the pdf of the binomial distribution
	        
	        Args:
	            None
	        
	        Returns:
	            list: x values for the pdf plot
	            list: y values for the pdf plot
            

        __add__(other):
        
	        To add together two Binomial distributions with equal p
	        
	        Args:
	            other (Binomial): Binomial instance
	            
	        Returns:
	            Binomial: Binomial distribution


        __repr__():
    
	        To output the characteristics of the Binomial instance
	        
	        Args:
	            None
	        
	        Returns:
	            string: characteristics of the Binomial


Class Distributions
Generic distribution class for calculating and visualizing a probability distribution.
	
	Attributes:
		mean (float) representing the mean value of the distribution
		stdev (float) representing the standard deviation of the distribution
		data_list (list of floats) a list of floats extracted from the data file
		read_data_file(file_name):
	
	Method:
		read_data_file(file_name)
			To read in data from a txt file. The txt file should have
			one number (float) per line. The numbers are stored in the data attribute.
					
			Args:
				file_name (string): name of a file to read from
			
			Returns:
				None