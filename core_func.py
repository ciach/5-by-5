def find_paths(node, my_dict, path, my_array, steps_list):
    path.append(node)
    word = [my_array[item] for item in path]
    if word.count("#") == 1:
        steps_list.append(path.copy())
    if len(path) < 12:  # words longer than 12 letters are not allowed for CPU
        for next_node in my_dict[node]:
            if next_node not in path:
                find_paths(next_node, my_dict, path, my_array, steps_list)
    path.pop()


def my_bad_function(my_array, my_dict) -> list:
    steps_list = []
    for node in my_dict.keys():
        find_paths(node, my_dict, [], my_array, steps_list)
    return steps_list
