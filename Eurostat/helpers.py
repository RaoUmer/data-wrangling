'''
Just some useful examples to work with the data.
'''

# To get just the finer values
comext['Jan2008'][comext['Jan2008']['PRODUCT_NC'].apply(len) > 2]