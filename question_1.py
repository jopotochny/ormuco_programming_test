
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

# testing of cases
line_pairs = [
    ((1, 3), (4, 6)),
    ((6, 2), (10, 1)),
    ((5, 6), (7, 6)),
    ((2, 9), (7, 8)),
    ((1, 2), (3, 4)),
    ((4, 2), (5, 8)),
    ((9, 6), (5, 8))
]
for lines in line_pairs:
    print(do_lines_overlap(lines[0], lines[1]))