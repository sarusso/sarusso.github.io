

# Write a function that sums all the values of a CSV file.


# This is an helper function which sums every elemnt of a list
# The same does the buil-in sum() function, but here we write
# it explicitly so that we can return None if the elist is empty

def sum_list(the_list):
    
    if not the_list:
        # If the list is empty it passes a "not" check
        return None
    
    else:
        # Initialize the total sum
        total = 0
        
        # Loop over each element and sum it to the total
        for element in the_list:
            total += element
            
        # Return the total
        return total


# This is the main exercise implementation. As for everything, there are many
# ways, this is using the with() together tith the open() and a support variable
# to keep track if the header line was already processed or not.

def sum_csv(the_file):
        
    if not the_file:
        # If the file name is empty it passes a "not" check
        return None
    
    else:
        
        # Initialize a list where to store all the values
        values = []
        
        # Add a support var to track if we already processed the header
        header_processed = False
        
        # Open and read the file line by line
        with open(the_file, 'r') as my_file:
                
            for line in my_file:

                if not header_processed:
                    
                    # If I have not yet processed the header, I mark it as such
                    header_processed = True
                
                else:
                    # Otherwise, process the line
            
                    # Split the line elements on the comma
                    elements = line.split(',')

                    # Set the date (which will not be used) and the value
                    date  = elements[0]
                    value = elements[1]
                    
                    # Clean the valaue
                    clean_value = value.strip()
                    
                    # Check if I can conver it, and if so append it to the values list
                    if clean_value.isnumeric():
                        values.append(float(clean_value))

        return sum_list(values)



