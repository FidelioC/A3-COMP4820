import pandas as pd
from pandas import DataFrame


def UPGMA_formula(matrix: DataFrame, i: str, j: str, k: str):
    return (len(i) * matrix.at[i, k] + len(j) * matrix.at[j, k]) / (len(i) + len(j))


def WPGMA_formula(matrix: DataFrame, i: str, j: str, k: str):
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


def calculate_all_distances(matrix: DataFrame, i: str, j: str, algorithm):
    all_distances = {}
    distance = 0
    for k in matrix.index:
        if k != i and k != j:
            if algorithm.lower() == "wpgma":
                distance = WPGMA_formula(matrix, i, j, k)
            elif algorithm.lower() == "upgma":
                distance = UPGMA_formula(matrix, i, j, k)

            all_distances[k] = distance

    return all_distances


def merge(matrix: DataFrame, i, j, all_distances):
    merge_cluster_name = i + j

    # drop the to be merged row/column
    matrix = matrix.drop([i, j])
    matrix = matrix.drop([i, j], axis=1)

    # add the new merged row/column
    matrix[merge_cluster_name] = None  # column
    matrix.loc[merge_cluster_name] = None  # row

    for entry, distance in all_distances.items():
        matrix.at[entry, merge_cluster_name] = distance
        matrix.at[merge_cluster_name, entry] = distance

    matrix.at[merge_cluster_name, merge_cluster_name] = 0

    return matrix


def run_algorithm(matrix: DataFrame, algorithm: str):
    current_matrix = matrix.copy()

    while len(current_matrix) > 1:
        # find min indices
        min_indices, _ = find_min_in_matrix(current_matrix)
        i, j = min_indices
        print(min_indices)

        # calculate all distances
        all_distances = calculate_all_distances(current_matrix, i, j, algorithm)
        print(all_distances)

        current_matrix = merge(current_matrix, i, j, all_distances)
        print(f"{current_matrix}\n")


def main():
    matrix = pd.read_csv("distances_test.csv", index_col=0)

    run_algorithm(matrix, "upgma")


if __name__ == "__main__":
    main()
