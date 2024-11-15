import pandas as pd
from pandas import DataFrame


def UPGMA_formula(matrix: DataFrame, i: str, j: str, k: str):
    """"""
    return (len(i) * matrix.at[i, k] + len(j) * matrix.at[j.k]) / (len(i) + len(j))


def WPGMA_formula(matrix: DataFrame, i: str, j: str, k: str):
    """"""
    return (matrix.at[i, k] + matrix.at[j, k]) / 2


def find_min_in_matrix(matrix: DataFrame):
    min_distance = float("inf")
    min_indices = None
    for i in matrix.index:  # iterate by rows
        for j in matrix.columns:  # iterate by columns
            curr_distance = matrix.at[i, j]
            # only consider the one side of the matrix
            # change min if curr_distance is less
            if i != j and curr_distance < min_distance:
                min_distance = curr_distance
                min_indices = (i, j)

    return min_indices, int(min_distance)


def main():
    """"""
    matrix = pd.read_csv("distances.csv", index_col=0)

    print(WPGMA_formula(matrix, "a", "b", "d"))
    print(WPGMA_formula(matrix, "a", "b", "c"))

    print(find_min_in_matrix(matrix))


if __name__ == "__main__":
    main()
