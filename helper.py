
def report_duplicates(l: list):
    count = {}
    
    for element in l:
        if element not in count:
            count[element] = 1
        else:
            count[element] += 1
    
    for key, val in count.items():
        if val > 1:
            print('Duplicate item {} | count({}) = {}'.format(key, key, val))