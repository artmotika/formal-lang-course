import pytest

from pathlib import Path
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
2 [label=var];
1 -> 2;
3 [label="'x'", shape=box];
2 -> 3;
4 [label="'='", shape=box];
1 -> 4;
5 [label=expr];
1 -> 5;
6 [label=val];
5 -> 6;
7 [label="'1'", shape=box];
6 -> 7;
8 [label="'<EOF>'", shape=box];
0 -> 8;
}""",
        ),
        (
            "a & star(b)",
            """strict digraph parsing_tree {
0 [label=prog];
1 [label=stmt];
0 -> 1;
2 [label=var];
1 -> 2;
3 [label="'a'", shape=box];
2 -> 3;
4 [label="'<EOF>'", shape=box];
0 -> 4;
}""",
        ),
    ],
)
def test_save_dot(tmpdir, input, expected):
    file_path = tmpdir.mkdir("test_dir").join("parsing_tree")
    save_parsing_tree_as_dot(input, file_path)
    assert file_path.read().strip() == expected.strip()
