# A3-COMP4820

## How to run

- The filename of the distance matrix (a .csv file) (--matrix; required, no default value).
- The algorithm to apply when constructing the tree (--algorithm; optional, default value is wpgma, other value is upgma).
- The filename to write the tree (--output; optional, the default behaviour should be to write to standard output; if this option is set, you should write to that file name instead).

## Example Usages

### writes to standard output

`python buildtree.py --matrix=distances.csv`

### writes to tree.tre with UPGMA

`python buildtree.py --matrix=distances.csv --algorithm=upgma --output=tree.tre`
