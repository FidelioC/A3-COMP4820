def generate_newick(clustering_iterations):
    # Initialize a dictionary to track Newick strings for clusters
    newick_dict = {}

    for pair in clustering_iterations:
        i, j = pair  # Extract the two clusters being merged
        print(f"pair: {pair}")
        # Get the Newick strings for i and j; use the cluster names if not yet in the dictionary
        i_newick = newick_dict.get(i, i)
        j_newick = newick_dict.get(j, j)
        print(f"i_newick: {i_newick} j_newick: {j_newick}")
        # Create a new Newick string for the merged cluster
        new_cluster_newick = f"({i_newick},{j_newick})"

        # Add the new cluster's Newick string to the dictionary
        newick_dict[f"{i}{j}"] = new_cluster_newick

        # Print the current state of the Newick string
        print(f"New cluster: {new_cluster_newick}")

        print(f"{newick_dict} \n")
    # The last cluster's Newick string is the full tree
    final_cluster = f"{clustering_iterations[-1][0]}{clustering_iterations[-1][1]}"
    return f"{newick_dict[final_cluster]};"


# Example clustering iterations
clustering_iterations = [("x4", "x5"), ("x1", "x2"), ("x3", "x4x5"), ("x1x2", "x3x4x5")]

# Generate the Newick string
final_newick = generate_newick(clustering_iterations)
print(f"Final Newick Tree: {final_newick}")
