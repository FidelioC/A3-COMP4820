import pandas as pd
from pandas import DataFrame
import click


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

    return min_indices, float(min_distance)


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
    cluster_dict = {}

    while len(current_matrix) > 1:
        # find min indices
        min_indices, min_distance = find_min_in_matrix(current_matrix)
        i, j = min_indices
        # print(min_indices)

        # calculate all distances
        all_distances = calculate_all_distances(current_matrix, i, j, algorithm)
        # print(all_distances)

        current_matrix = merge(current_matrix, i, j, all_distances)
        # print(f"{current_matrix}")

        new_cluster = f"({i},{j})"
        # print(f"new cluster: {new_cluster}")

        cluster_dict[new_cluster] = min_distance

    return cluster_dict


def create_newick_tree(cluster_dict: dict):
    newick_dict = {}
    distances = {}
    i_have_merged = False
    j_have_merged = False
    for key, value in cluster_dict.items():
        i, j = tuple(key.strip("()").split(","))

        distance = value / 2

        # check if previous the leaf is part of a merged cluster
        if i in newick_dict:
            cluster_i = newick_dict[i]
            i_have_merged = True
        else:
            cluster_i = i

        if j in newick_dict:
            cluster_j = newick_dict[j]
            j_have_merged = True
        else:
            cluster_j = j

        # print(f"i:{i} j:{j}")
        # print(f"curr_distance:{distance}, value:{value}")
        # print(f"distances:{distances}")
        # print(f"cluster_i:{cluster_i} cluster_j:{cluster_j}")

        if i_have_merged or j_have_merged:
            if j_have_merged:
                cluster = (
                    f"({cluster_i}:{distance}, {cluster_j}:{distance-distances[j]})"
                )
            elif i_have_merged:
                cluster = (
                    f"({cluster_i}, {cluster_j}:{distance}:{distance-distances[i]})"
                )
        else:
            cluster = f"({cluster_i}:{distance}, {cluster_j}:{distance})"

        # print(f"cluster:{cluster}")

        newick_dict[f"{i}{j}"] = cluster
        distances[f"{i}{j}"] = distance

        # print(newick_dict)
        # print(distances)
        # print("\n")

        i_have_merged = False
        j_have_merged = False
    return f"{list(newick_dict.values())[-1]}:0;"


def output_tree(newick_string, output):
    if output:
        with open(output, "w", encoding="utf-8") as file:
            file.write(newick_string)
            print(f"File written successfully to {output}")
    else:
        print(newick_string)


@click.command()
@click.option("--matrix", required=True)
@click.option("--algorithm", default="wpgma")
@click.option("--output")
def commands_processing(matrix, algorithm, output):
    matrix = pd.read_csv(matrix, index_col=0)

    cluster_dict = run_algorithm(matrix, algorithm)

    newick_string = create_newick_tree(cluster_dict)

    output_tree(newick_string, output)


if __name__ == "__main__":
    commands_processing()
