
# Excercise 1: write a code that prints, for each month of the year,
# its number, its name and how many days it contains.

# This is one of the many potential implementations for this exercise.
# it make use of two dictionaries, one for storing the month names and
# the other for how many days they contain. The key is the month number.
# Another approach would have been to store in a list 12 dictionaries
# where each dictionary would have represented a month with name and days,
# i.e. [{'January': 31}, {'February': 28}, ...]

month_names = { 1: 'January',
                2: 'February',
                3: 'March',
                4: 'April',
                5: 'May',
                6: 'June',
                7: 'July',
                8: 'August',
                9: 'September',
                10: 'October',
                11: 'November',                    
                12: 'December' }

month_days = { 1: 31,
               2: 28,
               3: 31,
               4: 31,
               5: 30,
               6: 31,
               7: 30,
               8: 31,
               9: 30,
               10: 31,
               11: 30,                    
               12: 31 }

for i in range(12):
    print('{}: {}, {}'.format(i+1, month_names[i+1], month_days[i+1]))
