from scipy.sparse import csc_matrix
from numpy import array


def get_direct_sum(matrix1: csc_matrix, matrix2: csc_matrix) -> csc_matrix:
    data, row, col = [], [], []
    for i, j in zip(*matrix1.nonzero()):
        data.append(True)
        row.append(i)
        col.append(j)
    shape1 = matrix1.shape[0]
    shape2 = matrix2.shape[0]
    shape = shape1 + shape2
    for i, j in zip(*matrix2.nonzero()):
        data.append(True)
        row.append(i + shape1)
        col.append(j + shape1)
    return csc_matrix(
        (
            array(data),
            (array(row), array(col)),
        ),
        shape=(shape, shape),
        dtype=bool,
    )


def get_submatrix(matrix: csc_matrix, range1: tuple, range2: tuple) -> csc_matrix:
    data, row, col = [], [], []
    shape1 = range1[1] - range1[0]
    shape2 = range2[1] - range2[0]
    for i, j in zip(*matrix.nonzero()):
        if range1[0] <= i < range1[1] and range2[0] <= j < range2[1]:
            data.append(True)
            row.append(i - range1[0])
            col.append(j - range2[0])
    return csc_matrix(
        (
            array(data),
            (array(row), array(col)),
        ),
        shape=(shape1, shape2),
        dtype=bool,
    )
