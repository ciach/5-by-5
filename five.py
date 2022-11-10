# open a file and read all the lines from item


def read_lines_from_file(filename):
    """_summary_

    Args:
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(filename, "r", encoding="UTF-8") as file:
        return file.readlines()
