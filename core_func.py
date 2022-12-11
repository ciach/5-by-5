""" That's a very poorly writen function, but it does its job.
    I think it should be recursive function. I don't know how to do it.
    Low code quality, but it works.

    TODO: should add check if the possible path contains only one empty
    space (#), if not we should not add it to the list
    in that case we should be quicker a bit.
    Despite the poor quality code
"""


def my_bad_function(my_array, my_dict) -> list:
    """_summary_

    Args:
        my_array (list): list of lists containing the game board
        my_dict (dict): dictionary with possible moves

    Returns:
        list: list of all possible moves

    Example One:
    Input:
        >>> my_array = [['#' '#' '#' '#' '#']
                        ['#' '#' '#' '#' '#']
                        ['F' 'I' 'M' 'E' 'L']
                        ['#' '#' '#' '#' '#']
                        ['#' '#' '#' '#' '#']]

        >>> my_dict = {
                        (1, 0): [(2, 0)],
                        (1, 1): [(2, 1)],
                        (1, 2): [(2, 2)],
                        (1, 3): [(2, 3)],
                        (1, 4): [(2, 4)],
                        (2, 0): [(1, 0), (3, 0), (2, 1)],
                        (2, 1): [(1, 1), (3, 1), (2, 0), (2, 2)],
                        (2, 2): [(1, 2), (3, 2), (2, 1), (2, 3)],
                        (2, 3): [(1, 3), (3, 3), (2, 2), (2, 4)],
                        (2, 4): [(1, 4), (3, 4), (2, 3)],
                        (3, 0): [(2, 0)],
                        (3, 1): [(2, 1)],
                        (3, 2): [(2, 2)],
                        (3, 3): [(2, 3)],
                        (3, 4): [(2, 4)]
                    }
    Output:
        >>> my_bad_function(my_array, my_dict)
        [
            [(1, 0), (2, 0)],
            [(1, 0), (2, 0), (2, 1)],
            [(1, 0), (2, 0), (2, 1), (2, 2)],
            [(1, 0), (2, 0), (2, 1), (2, 2), (2, 3)],
            [(1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
            [(1, 1), (2, 1)],
            [(1, 1), (2, 1), (2, 0)],
            [(1, 1), (2, 1), (2, 2)],
            [(1, 1), (2, 1), (2, 2), (2, 3)],
            [(1, 1), (2, 1), (2, 2), (2, 3), (2, 4)],
            [(1, 2), (2, 2)],
            [(1, 2), (2, 2), (2, 1), (2, 0)],
            [(1, 2), (2, 2), (2, 1)],
            [(1, 2), (2, 2), (2, 3)],
            [(1, 2), (2, 2), (2, 3), (2, 4)],
            [(1, 3), (2, 3)],
            [(1, 3), (2, 3), (2, 2), (2, 1), (2, 0)],
            [(1, 3), (2, 3), (2, 2), (2, 1)],
            [(1, 3), (2, 3), (2, 2)],
            [(1, 3), (2, 3), (2, 4)],
            [(1, 4), (2, 4)],
            [(1, 4), (2, 4), (2, 3), (2, 2), (2, 1), (2, 0)],
            [(1, 4), (2, 4), (2, 3), (2, 2), (2, 1)],
            [(1, 4), (2, 4), (2, 3), (2, 2)],
            [(1, 4), (2, 4), (2, 3)],
            [(2, 0), (1, 0)],
            [(2, 0), (3, 0)],
            [(2, 0), (2, 1), (1, 1)],
            [(2, 0), (2, 1), (3, 1)],
            [(2, 0), (2, 1), (2, 2), (1, 2)],
            [(2, 0), (2, 1), (2, 2), (3, 2)],
            [(2, 0), (2, 1), (2, 2), (2, 3), (1, 3)],
            [(2, 0), (2, 1), (2, 2), (2, 3), (3, 3)],
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (1, 4)],
            [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 4)],
            [(2, 1), (1, 1)],
            [(2, 1), (3, 1)],
            [(2, 1), (2, 0), (1, 0)],
            [(2, 1), (2, 0), (3, 0)],
            [(2, 1), (2, 2), (1, 2)],
            [(2, 1), (2, 2), (3, 2)],
            [(2, 1), (2, 2), (2, 3), (1, 3)],
            [(2, 1), (2, 2), (2, 3), (3, 3)],
            [(2, 1), (2, 2), (2, 3), (2, 4), (1, 4)],
            [(2, 1), (2, 2), (2, 3), (2, 4), (3, 4)],
            [(2, 2), (1, 2)],
            [(2, 2), (3, 2)],
            [(2, 2), (2, 1), (1, 1)],
            [(2, 2), (2, 1), (3, 1)],
            [(2, 2), (2, 1), (2, 0), (1, 0)],
            [(2, 2), (2, 1), (2, 0), (3, 0)],
            [(2, 2), (2, 3), (1, 3)],
            [(2, 2), (2, 3), (3, 3)],
            [(2, 2), (2, 3), (2, 4), (1, 4)],
            [(2, 2), (2, 3), (2, 4), (3, 4)],
            [(2, 3), (1, 3)],
            [(2, 3), (3, 3)],
            [(2, 3), (2, 2), (1, 2)],
            [(2, 3), (2, 2), (3, 2)],
            [(2, 3), (2, 2), (2, 1), (1, 1)],
            [(2, 3), (2, 2), (2, 1), (3, 1)],
            [(2, 3), (2, 2), (2, 1), (2, 0), (1, 0)],
            [(2, 3), (2, 2), (2, 1), (2, 0), (3, 0)],
            [(2, 3), (2, 4), (1, 4)],
            [(2, 3), (2, 4), (3, 4)],
            [(2, 4), (1, 4)],
            [(2, 4), (3, 4)],
            [(2, 4), (2, 3), (1, 3)],
            [(2, 4), (2, 3), (3, 3)],
            [(2, 4), (2, 3), (2, 2), (1, 2)],
            [(2, 4), (2, 3), (2, 2), (3, 2)],
            [(2, 4), (2, 3), (2, 2), (2, 1), (1, 1)],
            [(2, 4), (2, 3), (2, 2), (2, 1), (3, 1)],
            [(2, 4), (2, 3), (2, 2), (2, 1), (2, 0), (1, 0)],
            [(2, 4), (2, 3), (2, 2), (2, 1), (2, 0), (3, 0)],
            [(3, 0), (2, 0)],
            [(3, 0), (2, 0), (2, 1)],
            [(3, 0), (2, 0), (2, 1), (2, 2)],
            [(3, 0), (2, 0), (2, 1), (2, 2), (2, 3)],
            [(3, 0), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
            [(3, 1), (2, 1)],
            [(3, 1), (2, 1), (2, 0)],
            [(3, 1), (2, 1), (2, 2)],
            [(3, 1), (2, 1), (2, 2), (2, 3)],
            [(3, 1), (2, 1), (2, 2), (2, 3), (2, 4)],
            [(3, 2), (2, 2)],
            [(3, 2), (2, 2), (2, 1), (2, 0)],
            [(3, 2), (2, 2), (2, 1)],
            [(3, 2), (2, 2), (2, 3)],
            [(3, 2), (2, 2), (2, 3), (2, 4)],
            [(3, 3), (2, 3)],
            [(3, 3), (2, 3), (2, 2), (2, 1), (2, 0)],
            [(3, 3), (2, 3), (2, 2), (2, 1)],
            [(3, 3), (2, 3), (2, 2)],
            [(3, 3), (2, 3), (2, 4)],
            [(3, 4), (2, 4)],
            [(3, 4), (2, 4), (2, 3), (2, 2), (2, 1), (2, 0)],
            [(3, 4), (2, 4), (2, 3), (2, 2), (2, 1)],
            [(3, 4), (2, 4), (2, 3), (2, 2)],
            [(3, 4), (2, 4), (2, 3)]
        ]
    """
    steps_list = []
    for aa_ in my_dict.keys():
        for bb_ in my_dict[aa_]:
            if bb_ not in [aa_]:
                for cc_ in my_dict[bb_]:
                    if cc_ not in [aa_, bb_]:
                        for dd_ in my_dict[cc_]:
                            if dd_ not in [aa_, bb_, cc_]:
                                for ee_ in my_dict[dd_]:
                                    if ee_ not in [aa_, bb_, cc_, dd_]:
                                        for ff_ in my_dict[ee_]:
                                            if ff_ not in [aa_, bb_, cc_, dd_, ee_]:
                                                for gg_ in my_dict[ff_]:
                                                    if gg_ not in [
                                                        aa_,
                                                        bb_,
                                                        cc_,
                                                        dd_,
                                                        ee_,
                                                        ff_,
                                                    ]:
                                                        for hh_ in my_dict[gg_]:
                                                            if hh_ not in [
                                                                aa_,
                                                                bb_,
                                                                cc_,
                                                                dd_,
                                                                ee_,
                                                                ff_,
                                                                gg_,
                                                            ]:
                                                                for ii_ in my_dict[hh_]:
                                                                    if ii_ not in [
                                                                        aa_,
                                                                        bb_,
                                                                        cc_,
                                                                        dd_,
                                                                        ee_,
                                                                        ff_,
                                                                        gg_,
                                                                        hh_,
                                                                    ]:
                                                                        for (
                                                                            jj_
                                                                        ) in my_dict[
                                                                            ii_
                                                                        ]:
                                                                            if (
                                                                                jj_
                                                                                not in [
                                                                                    aa_,
                                                                                    bb_,
                                                                                    cc_,
                                                                                    dd_,
                                                                                    ee_,
                                                                                    ff_,
                                                                                    gg_,
                                                                                    hh_,
                                                                                    ii_,
                                                                                ]
                                                                            ):
                                                                                path_ = [
                                                                                    aa_,
                                                                                    bb_,
                                                                                    cc_,
                                                                                    dd_,
                                                                                    ee_,
                                                                                    ff_,
                                                                                    gg_,
                                                                                    hh_,
                                                                                    ii_,
                                                                                    jj_,
                                                                                ]
                                                                                word_ = [
                                                                                    my_array[
                                                                                        item
                                                                                    ]
                                                                                    for item in path_
                                                                                ]
                                                                                if (
                                                                                    word_.count(
                                                                                        "#"
                                                                                    )
                                                                                    == 1
                                                                                ):
                                                                                    steps_list.append(
                                                                                        path_
                                                                                    )
                                                                            else:
                                                                                path_ = [
                                                                                    aa_,
                                                                                    bb_,
                                                                                    cc_,
                                                                                    dd_,
                                                                                    ee_,
                                                                                    ff_,
                                                                                    gg_,
                                                                                    hh_,
                                                                                    ii_,
                                                                                ]
                                                                                word_ = [
                                                                                    my_array[
                                                                                        item
                                                                                    ]
                                                                                    for item in path_
                                                                                ]
                                                                                if (
                                                                                    word_.count(
                                                                                        "#"
                                                                                    )
                                                                                    == 1
                                                                                ):
                                                                                    steps_list.append(
                                                                                        path_
                                                                                    )
                                                                    else:
                                                                        path_ = [
                                                                            aa_,
                                                                            bb_,
                                                                            cc_,
                                                                            dd_,
                                                                            ee_,
                                                                            ff_,
                                                                            gg_,
                                                                            hh_,
                                                                        ]
                                                                        word_ = [
                                                                            my_array[
                                                                                item
                                                                            ]
                                                                            for item in path_
                                                                        ]
                                                                        if (
                                                                            word_.count(
                                                                                "#"
                                                                            )
                                                                            == 1
                                                                        ):
                                                                            steps_list.append(
                                                                                path_
                                                                            )
                                                            else:
                                                                path_ = [
                                                                    aa_,
                                                                    bb_,
                                                                    cc_,
                                                                    dd_,
                                                                    ee_,
                                                                    ff_,
                                                                    gg_,
                                                                ]
                                                                word_ = [
                                                                    my_array[item]
                                                                    for item in path_
                                                                ]
                                                                if (
                                                                    word_.count("#")
                                                                    == 1
                                                                ):
                                                                    steps_list.append(
                                                                        path_
                                                                    )
                                                    else:
                                                        path_ = [
                                                            aa_,
                                                            bb_,
                                                            cc_,
                                                            dd_,
                                                            ee_,
                                                            ff_,
                                                        ]
                                                        word_ = [
                                                            my_array[item]
                                                            for item in path_
                                                        ]
                                                        if word_.count("#") == 1:
                                                            steps_list.append(path_)
                                            else:
                                                path_ = [
                                                    aa_,
                                                    bb_,
                                                    cc_,
                                                    dd_,
                                                    ee_,
                                                ]
                                                word_ = [
                                                    my_array[item] for item in path_
                                                ]
                                                if word_.count("#") == 1:
                                                    steps_list.append(path_)
                                    else:
                                        path_ = [
                                            aa_,
                                            bb_,
                                            cc_,
                                            dd_,
                                        ]
                                        word_ = [my_array[item] for item in path_]
                                        if word_.count("#") == 1:
                                            steps_list.append(path_)
                            else:
                                path_ = [
                                    aa_,
                                    bb_,
                                    cc_,
                                ]
                                word_ = [my_array[item] for item in path_]
                                if word_.count("#") == 1:
                                    steps_list.append(path_)
                    else:
                        path_ = [
                            aa_,
                            bb_,
                        ]
                        word_ = [my_array[item] for item in path_]
                        if word_.count("#") == 1:
                            steps_list.append(path_)

    return steps_list
