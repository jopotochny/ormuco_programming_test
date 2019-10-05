
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
        else:
            if int(version_one_values[i]) > int(version_two_values[i]):
                return version_one
            elif int(version_one_values[i]) < int(version_two_values[i]):
                return version_two
    # if after going through all of the values in version_one we did not return, then version_two has more levels and is
    # also the larger version, e.g. version_one = "1.2.3" and version_two = "1.2.3.4"
    return version_two

# test cases
test_cases = [
    ["1.2", "2.1.5"],
    ["5.8.2", "1"],
    ["4.6.7.8.9.12", "4.6.7.8.9"],
    ["1.2.3.4.5", "1.2.3.4.5.6"],
    ["", "2.1"],
    ["1.2", ""],
    ["", ""],
    [None, "1.2"],
    ["1.2", None],
    [None, None]
]
for test_case in test_cases:
    print(get_larger_version(test_case[0], test_case[1]))