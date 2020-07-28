from svgutils.transform import fromfile
from svgutils.transform import SVGFigure, GroupElement
from svgutils.templates import VerticalLayout, ColumnLayout
from PIL import Image
import numpy as np
import hashlib
import os
from wfc import *


def get_fragment_vocab():
    vocab = {
        x: Image.open(f"assets/{x}.png")
        for x in "ABCDEFGHJ"
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
    compatibilities, weights, border_tiles = parse_example_matrix(input_matrix3)
    compatibility_oracle = CompatibilityOracle(compatibilities)
    model = Model((h, w), weights, compatibility_oracle, border_tiles)
    output = model.run()
    h = len(output)
    w = len(output[0])
    vocab = get_fragment_vocab()
    print(get_fragment_vocab)
    print(h, w)
    lines = [
        np.hstack([ np.asarray(vocab.get(x, "G")) for x in row ])
        for row in output
    ]
    arr = np.vstack(lines)
    fileinfo = "\n".join(["".join(row) for row in output])
    name = hashlib.sha224(fileinfo.encode()).hexdigest()
    if not os.path.exists("images"):
        os.makedirs("images")
    path = f"images/{name}.png"
    Image.fromarray(arr).save(path)
    return path


def make_pattern_measured():
    pass