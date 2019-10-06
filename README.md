# Ormuco Programming Test

## Q1
```python
def do_lines_overlap(line_one, line_two): # assuming the inputs are tuples
    # this ensures that the line is defined as (smaller x, larger x)
    line_one = list(line_one)
    line_one.sort()
    line_two = list(line_two)
    line_two.sort()
    # assuming that if the two lines share a start/end point it is overlapping
    if line_one[1] >= line_two[0]:
        return True
    return False
```
This code can be found within question_1.py, and running this file will run the function with various test cases.

## Q2
```python
def get_larger_version(version_one, version_two):

    # check for bad inputs
    if (version_one is None or version_one == "") and version_two is not None and version_two != "":
            return version_two
    if version_one is not None and (version_two is None or version_two == "") and version_one != "":
            return version_one
    if (version_one is None and version_two is None) or (version_one == "" and version_two == ""):
        return None
    # first split the strings on "." in order to compare the version at each level
    version_one_values = version_one.split('.')
    version_two_values = version_two.split('.')

    for i in range(len(version_one_values)):
        if i > len(version_two_values) - 1:
            # then version_one is has more levels, and since we have not returned
            # yet then version one must be the greater version number
            return version_one
        elif i == len(version_one_values) - 1 and i == len(version_two_values) - 1:
            # then there are the same number of levels in both, and we have reached the end. Want to check if they are equal
            if int(version_one_values[i]) == int(version_two_values[i]):
                # then they are equal, return both
                return version_one, version_two
        else:
            if int(version_one_values[i]) > int(version_two_values[i]):
                return version_one
            elif int(version_one_values[i]) < int(version_two_values[i]):
                return version_two
    # if after going through all of the values in version_one we did not return, then version_two has more levels and is
    # also the larger version, e.g. version_one = "1.2.3" and version_two = "1.2.3.4"
    return version_two
```
This code can be found in question_2.py, and as before running the file will run the function with various test cases.

## Q3
Below you will find a diagram of my solution for the Geo-Distributed LRU Cache
![](https://github.com/jopotochny/ormuco_programming_test/blob/master/images/LRUCache.png "LRUCache")

My solution is made up of a class that represents the actual [LRUCache](https://github.com/jopotochny/ormuco_programming_test/blob/master/OrmucoCache/LRUCache.py), a class that acts as the [handler](https://github.com/jopotochny/ormuco_programming_test/blob/master/OrmucoCache/LRUCacheHandler.py) for a Python socket server, and a [manager](https://github.com/jopotochny/ormuco_programming_test/blob/master/OrmucoCache/LRUCacheManager.py) class that upon initialization runs the LRUCache in memory, where it will listen for requests to either get a value or update the cache. 

An instance of the cache acts either as a master cache, which is assigned by the user any number of child caches, or a child cahce, which is assigned a master cache. Whenever a cache lookup results in a cache miss, the cache will add the missed value to itself. If the cache is a child cache, it conencts to its assigned master cache and sends it the missed item. The master cache then adds the missed item to itself and propagates the missed item to all of its children in order for them to update as well. In this way, all caches within a master cache's network should remain consistent. Further work could be done to connect master caches, allowing for various regions to remain consistent as well.

Cached items also expire, and the cache is purged of expired items only after a request is made for an item. For ease of access, the LRUCache is composed of a Python dictionary and a circular doubly linked list consisting of [CacheNodes](https://github.com/jopotochny/ormuco_programming_test/blob/master/OrmucoCache/CacheNode.py).

