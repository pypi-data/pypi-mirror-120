# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CONVERT OBS DICT TO LIST
# └─────────────────────────────────────────────────────────────────────────────────────


def convert_obs_dict_to_list(_obs):
    """ Converts an object dict to list based on respective counts """

    # Return the sum of object lists by count
    return sum([[k] * v for i, (k, v) in enumerate(_obs.items())], [])


# ┌─────────────────────────────────────────────────────────────────────────────────────
# │ CONVERT STRING TO PASCAL CASE
# └─────────────────────────────────────────────────────────────────────────────────────


def convert_string_to_pascal_case(string):
    """ Converts a strong to Pascal case """

    # Split string
    string = [s.strip() for s in string.split(" ")]

    # Capitalize each word
    string = [s[0].upper() + s[1:] for s in string if s]

    # Join string
    string = "".join(string)

    # Return string
    return string
