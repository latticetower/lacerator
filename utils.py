from svgutils.transform import fromfile
from svgutils.transform import SVGFigure, GroupElement
from svgutils.templates import VerticalLayout, ColumnLayout


from wfc import *


def get_fragment_vocab():
    vocab = {
        "A": fromfile("assets/"),
        #"B",
        #"C",
        #"D",
        #"E",
        #"F",
        #"G",
        #"H",
        ##"I",
        #"J"
    }
    return vocab
    
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
    h = len(output)
    w = len(output[0])
    vocab = get_fragment_vocab()
    print(get_fragment_vocab)
    print(h, w)
    pass


def make_pattern_measured():
    pass