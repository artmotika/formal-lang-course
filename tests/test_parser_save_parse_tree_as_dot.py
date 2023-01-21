import pytest

from project.grammar_query_language.parser import save_parsing_tree_as_dot


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            "x = 1",
            """strict digraph parsing_tree {
0 [label=prog];
1 [label=stmt];
0 -> 1;
2 [label="'x'", shape=box];
1 -> 2;
3 [label="'='", shape=box];
1 -> 3;
4 [label=expr];
1 -> 4;
5 [label=val];
4 -> 5;
6 [label="'1'", shape=box];
5 -> 6;
7 [label="'<EOF>'", shape=box];
0 -> 7;
}""",
        ),
        (
            "a = (a & star(b))",
            """strict digraph parsing_tree {
0 [label=prog];
1 [label=stmt];
0 -> 1;
2 [label="'a'", shape=box];
1 -> 2;
3 [label="'='", shape=box];
1 -> 3;
4 [label=expr];
1 -> 4;
5 [label="'('", shape=box];
4 -> 5;
6 [label=expr];
4 -> 6;
7 [label=expr];
6 -> 7;
8 [label="'a'", shape=box];
7 -> 8;
9 [label="'&'", shape=box];
6 -> 9;
10 [label=expr];
6 -> 10;
11 [label="'star'", shape=box];
10 -> 11;
12 [label="'('", shape=box];
10 -> 12;
13 [label=expr];
10 -> 13;
14 [label="'b'", shape=box];
13 -> 14;
15 [label="')'", shape=box];
10 -> 15;
16 [label="')'", shape=box];
4 -> 16;
17 [label="'<EOF>'", shape=box];
0 -> 17;
}""",
        ),
    ],
)
def test_save_dot(tmpdir, input, expected):
    file_path = tmpdir.mkdir("test_dir").join("parsing_tree")
    save_parsing_tree_as_dot(input, file_path)
    print(file_path.read().strip())
    assert file_path.read().strip() == expected.strip()
