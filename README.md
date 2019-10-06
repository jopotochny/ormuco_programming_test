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
