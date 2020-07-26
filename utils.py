from wfc import *


def make_pattern_from_fragments(h=10, w=10):
    input_matrix3 = """
    AFBAFBAFBAFB
    EGDCGEEGDCGE
    DBGGGEEGGGAC
    ACGGACDBGGDB
    EGGAHFFJBGGE
    DFFCEGGEDFFC
    AFFBEGGEAFFB
    EGGDJFFHCGGE
    DBGGDBACGGAC
    ACGGGEEGGGDB
    EGABGEEGABGE
    DFCDFCDFCDFC
    """
    input_matrix3 = [
        list(line.strip())
        for line in input_matrix3.split("\n")
        if len(line.strip()) > 0
    ]
    compatibilities, weights = parse_example_matrix(input_matrix3)
    compatibility_oracle = CompatibilityOracle(compatibilities)
    model = Model((h, w), weights, compatibility_oracle)
    output = model.run()
    print(output)
    pass


def make_pattern_measured():
    pass