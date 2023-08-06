import sys

import pytest

import termplotlib as tpl


@pytest.mark.skipif(
    sys.stdout.encoding.upper() not in ["UTF-8", "UTF8"],
    reason=f"Need UTF-8 terminal (not {sys.stdout.encoding})",
)
def test_barh():
    fig = tpl.figure()
    fig.barh([3, 10, 5, 2], ["Cats", "Dogs", "Cows", "Geese"])
    # fig.show()
    string = fig.get_string()

    assert (
        string
        == """\
Cats   [ 3]  ████████████
Dogs   [10]  ████████████████████████████████████████
Cows   [ 5]  ████████████████████
Geese  [ 2]  ████████\
"""
    )


def test_barh_ascii():
    fig = tpl.figure()
    fig.barh([3, 10, 5, 2], ["Cats", "Dogs", "Cows", "Geese"], force_ascii=True)
    # fig.show()
    string = fig.get_string()

    assert (
        string
        == """\
Cats   [ 3]  ************
Dogs   [10]  ****************************************
Cows   [ 5]  ********************
Geese  [ 2]  ********\
"""
    )


@pytest.mark.skipif(
    sys.stdout.encoding.upper() not in ["UTF-8", "UTF8"],
    reason=f"Need UTF-8 terminal (not {sys.stdout.encoding})",
)
def test_barh_floats():
    fig = tpl.figure()
    fig.barh([0.3, 0.4, 0.6, 0.2], ["Cats", "Dogs", "Cows", "Geese"])
    # fig.show()
    string = fig.get_string()

    assert (
        string
        == """\
Cats   [0.3]  ████████████████████
Dogs   [0.4]  ██████████████████████████▋
Cows   [0.6]  ████████████████████████████████████████
Geese  [0.2]  █████████████▍\
"""
    )


def test_barh_floats_different_precision():
    fig = tpl.figure()
    fig.barh([3, 2.5341234], ["Cats", "Dogs"])
    # fig.show()
    string = fig.get_string()

    ref = """\
Cats  [3.0000000]  ████████████████████████████████████████
Dogs  [2.5341234]  █████████████████████████████████▊"""

    assert string == ref, "\n" + string


def test_div_by_zero():
    fig = tpl.figure()
    fig.barh([0, 0], ["Eggs", "Dogs"])
    string = fig.get_string()
    print(string)
    assert (
        string
        == """\
Eggs  [0]
Dogs  [0]\
"""
    )


if __name__ == "__main__":
    # test_horizontal_ascii()
    # test_barh()
    test_barh_floats()
