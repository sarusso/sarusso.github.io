
# Excercise 2: Write a function that sums all the numbers of a list.

def sum_list(the_list):
    if not the_list:
        return None
    else:
        
        if not type(the_list) == list:
            return None
        
        total = 0
        for element in the_list:
            if type(element) not in [int, float]:
                return None
            else:
                total = total + element
        return total






















