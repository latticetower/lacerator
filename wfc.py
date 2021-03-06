# Implementation of WFC algorithm is taken from https://github.com/robert/wavefunction-collapse
import random
import math
import numpy as np

UP = (0, 1)
LEFT = (-1, 0)
DOWN = (0, -1)
RIGHT = (1, 0)
DIRS = [UP, DOWN, LEFT, RIGHT]
EMPTY_TILE = "G"

class CompatibilityOracle(object):

    """The CompatibilityOracle class is responsible for telling us
    which combinations of tiles and directions are compatible. It's
    so simple that it perhaps doesn't need to be a class, but I think
    it helps keep things clear.
    """

    def __init__(self, data):
        self.data = data

    def check(self, tile1, tile2, direction):
        return (tile1, tile2, direction) in self.data


class Wavefunction(object):

    """The Wavefunction class is responsible for storing which tiles
    are permitted and forbidden in each location of an output image.
    """

    @staticmethod
    def mk(size, weights, border_tiles):
        """Initialize a new Wavefunction for a grid of `size`,
        where the different tiles have overall weights `weights`.

        Arguments:
        size -- a 2-tuple of (width, height)
        weights -- a dict of tile -> weight of tile
        """
        coefficients = Wavefunction.init_coefficients(size, weights.keys(), border_tiles)
        return Wavefunction(coefficients, weights)

    @staticmethod
    def init_coefficients(size, tiles, border_tiles):
        """Initializes a 2-D wavefunction matrix of coefficients.
        The matrix has size `size`, and each element of the matrix
        starts with all tiles as possible. No tile is forbidden yet.

        NOTE: coefficients is a slight misnomer, since they are a
        set of possible tiles instead of a tile -> number/bool dict. This
        makes the code a little simpler. We keep the name `coefficients`
        for consistency with other descriptions of Wavefunction Collapse.

        Arguments:
        size -- a 2-tuple of (width, height)
        tiles -- a set of all the possible tiles

        Returns:
        A 2-D matrix in which each element is a set
        """
        coefficients = []
        tiles_ = list(border_tiles[UP]) + [EMPTY_TILE]
        row = [ set(tiles_) for i in range(size[1]) ]
        row[0] = (row[0] & border_tiles[LEFT]) | set([EMPTY_TILE])
        row[-1] = (row[-1] & border_tiles[RIGHT]) | set([EMPTY_TILE])
        coefficients.append(row)
        for x in range(1, size[0] - 1):
            row = []
            row.append(set(list(border_tiles[LEFT]) + [ EMPTY_TILE ]))
            for y in range(1, size[1] - 1):
                row.append(set([t for t in tiles if t != EMPTY_TILE ]))
            row.append(set(list(border_tiles[RIGHT]) + [ EMPTY_TILE ]))
            coefficients.append(row)
        
        tiles_ = list(border_tiles[DOWN]) + [EMPTY_TILE]
        row = [ set(tiles_) for i in range(size[1]) ]
        row[0] = (row[0] & border_tiles[LEFT]) | set([EMPTY_TILE])
        row[-1] = (row[-1] & border_tiles[RIGHT]) | set([EMPTY_TILE])

        coefficients.append(row)
        return coefficients

    def __init__(self, coefficients, weights):
        self.coefficients = coefficients
        self.weights = weights

    def get(self, co_ords):
        """Returns the set of possible tiles at `co_ords`"""
        x, y = co_ords
        return self.coefficients[x][y]

    def get_collapsed(self, co_ords):
        """Returns the only remaining possible tile at `co_ords`.
        If there is not exactly 1 remaining possible tile then
        this method raises an exception.
        """
        opts = self.get(co_ords)
        if len(opts) != 1:
            #print(opts)
            return EMPTY_TILE
            #print(opts)
        assert(len(opts) == 1)
        return next(iter(opts))

    def get_all_collapsed(self):
        """Returns a 2-D matrix of the only remaining possible
        tiles at each location in the wavefunction. If any location
        does not have exactly 1 remaining possible tile then
        this method raises an exception.
        """
        width = len(self.coefficients)
        height = len(self.coefficients[0])

        collapsed = []
        for x in range(width):
            row = []
            for y in range(height):
                row.append(self.get_collapsed((x,y)))
            collapsed.append(row)

        return collapsed

    def shannon_entropy(self, co_ords):
        """Calculates the Shannon Entropy of the wavefunction at
        `co_ords`.
        """
        x, y = co_ords

        sum_of_weights = 0
        sum_of_weight_log_weights = 0
        for opt in self.coefficients[x][y]:
            weight = self.weights[opt]
            sum_of_weights += weight
            sum_of_weight_log_weights += weight * math.log(weight)

        return math.log(sum_of_weights) - (sum_of_weight_log_weights / sum_of_weights)


    def is_fully_collapsed(self):
        """Returns true if every element in Wavefunction is fully
        collapsed, and false otherwise.
        """
        for x, row in enumerate(self.coefficients):
            for y, sq in enumerate(row):
                if len(sq) > 1:
                    return False

        return True

    def collapse(self, co_ords):
        """Collapses the wavefunction at `co_ords` to a single, definite
        tile. The tile is chosen randomly from the remaining possible tiles
        at `co_ords`, weighted according to the Wavefunction's global
        `weights`.

        This method mutates the Wavefunction, and does not return anything.
        """
        x, y = co_ords
        opts = self.coefficients[x][y]
        valid_weights = {tile: weight for tile, weight in self.weights.items() if tile in opts}

        total_weights = sum(valid_weights.values())
        # rnd = random.random() * total_weights
        # 
        # chosen = None
        # for tile, weight in valid_weights.items():
        #     rnd -= weight
        #     if rnd < 0:
        #         chosen = tile
        #         break
        chosen = np.random.choice(list(valid_weights.keys()),
            p = list(valid_weights.values())
        )
        #print(valid_weights, chosen)

        self.coefficients[x][y] = set([chosen])
        #return chosen
        
    def choose(self, co_ords):
        """Collapses the wavefunction at `co_ords` to a single, definite
        tile. The tile is chosen randomly from the remaining possible tiles
        at `co_ords`, weighted according to the Wavefunction's global
        `weights`.

        This method mutates the Wavefunction, and does not return anything.
        """
        x, y = co_ords
        opts = self.coefficients[x][y]
        valid_weights = {tile: weight for tile, weight in self.weights.items() if tile in opts}

        total_weights = sum(valid_weights.values())
        # rnd = random.random() * total_weights
        # 
        # chosen = None
        # for tile, weight in valid_weights.items():
        #     rnd -= weight
        #     if rnd < 0:
        #         chosen = tile
        #         break
        chosen = np.random.choice(list(valid_weights.keys()))
        #print(valid_weights, chosen)
        return chosen

    def try_to_collapse(self, co_ords, chosen, output_size, compatibility_oracle):
        stack = [co_ords]
        coefficients = [
            [
                x.copy()
                for x in row
            ]
            for row in self.coefficients
        ]
        while len(stack) > 0:
            cur_coords = stack.pop()
            x, y = cur_coords
            # Get the set of all possible tiles at the current location
            cur_possible_tiles = coefficients[x][y]

            # Iterate through each location immediately adjacent to the
            # current location.
            invalid = False
            for d in valid_dirs(cur_coords, output_size):
                other_coords = (cur_coords[0] + d[0], cur_coords[1] + d[1])

                # Iterate through each possible tile in the adjacent location's
                # wavefunction.
                x1, y1 = other_coords
                for other_tile in set(coefficients[x1][y1]):
                    # Check whether the tile is compatible with any tile in
                    # the current location's wavefunction.
                    other_tile_is_possible = any([
                        compatibility_oracle.check(cur_tile, other_tile, d) for cur_tile in cur_possible_tiles
                    ])
                    # If the tile is not compatible with any of the tiles in
                    # the current location's wavefunction then it is impossible
                    # for it to ever get chosen. We therefore remove it from
                    # the other location's wavefunction.
                    if not other_tile_is_possible:
                        #self.wavefunction.constrain(other_coords, other_tile)
                        if len(coefficients[x1][y1]) < 1:
                            invalid = True
                        coefficients[x1][y1].remove(other_tile)
                        
                        stack.append(other_coords)
        if invalid:
            if len(self.coefficients[x][y]) > 1:
                self.coefficients[x][y].remove(chosen)
        else:
            self.coefficients = coefficients
            self.coefficients[x][y] = set([chosen])


    def constrain(self, co_ords, forbidden_tile):
        """Removes `forbidden_tile` from the list of possible tiles
        at `co_ords`.

        This method mutates the Wavefunction, and does not return anything.
        """
        x, y = co_ords
        self.coefficients[x][y].remove(forbidden_tile)


class Model(object):

    """The Model class is responsible for orchestrating the
    Wavefunction Collapse algorithm.
    """

    def __init__(self, output_size, weights, compatibility_oracle, border_tiles):
        self.output_size = output_size
        self.compatibility_oracle = compatibility_oracle
        self.wavefunction = Wavefunction.mk(output_size, weights, border_tiles)

    def run(self):
        """Collapses the Wavefunction until it is fully collapsed,
        then returns a 2-D matrix of the final, collapsed state.
        """
        while not self.wavefunction.is_fully_collapsed():
            self.iterate()
        return self.wavefunction.get_all_collapsed()

    def iterate(self):
        """Performs a single iteration of the Wavefunction Collapse
        Algorithm.
        """
        # 1. Find the co-ordinates of minimum entropy
        co_ords = self.min_entropy_co_ords()
        #print("coords", co_ords)
        #total = np.sum([len(x)for row in self.wavefunction.coefficients for x in row])
        #print(total)
        x, y = co_ords
        # 2. Collapse the wavefunction at these co-ordinates
        chosen = self.wavefunction.choose(co_ords)
        # 3. Propagate the consequences of this collapse
        #self.propagate(co_ords, chosen)
        self.wavefunction.try_to_collapse(co_ords, chosen,
            self.output_size, self.compatibility_oracle)

    def propagate(self, co_ords, chosen):
        """Propagates the consequences of the wavefunction at `co_ords`
        collapsing. If the wavefunction at (x,y) collapses to a fixed tile,
        then some tiles may not longer be theoretically possible at
        surrounding locations.

        This method keeps propagating the consequences of the consequences,
        and so on until no consequences remain.
        """
        stack = [co_ords]

        while len(stack) > 0:
            cur_coords = stack.pop()
            # Get the set of all possible tiles at the current location
            cur_possible_tiles = self.wavefunction.get(cur_coords)

            # Iterate through each location immediately adjacent to the
            # current location.
            for d in valid_dirs(cur_coords, self.output_size):
                other_coords = (cur_coords[0] + d[0], cur_coords[1] + d[1])

                # Iterate through each possible tile in the adjacent location's
                # wavefunction.
                for other_tile in set(self.wavefunction.get(other_coords)):
                    # Check whether the tile is compatible with any tile in
                    # the current location's wavefunction.
                    other_tile_is_possible = any([
                        self.compatibility_oracle.check(cur_tile, other_tile, d) for cur_tile in cur_possible_tiles
                    ])
                    # If the tile is not compatible with any of the tiles in
                    # the current location's wavefunction then it is impossible
                    # for it to ever get chosen. We therefore remove it from
                    # the other location's wavefunction.
                    if not other_tile_is_possible:
                        self.wavefunction.constrain(other_coords, other_tile)
                        stack.append(other_coords)

    def min_entropy_co_ords(self):
        """Returns the co-ords of the location whose wavefunction has
        the lowest entropy.
        """
        min_entropy = None
        min_entropy_coords = None

        width, height = self.output_size
        for x in range(width):
            for y in range(height):
                if len(self.wavefunction.get((x,y))) == 1:
                    continue

                entropy = self.wavefunction.shannon_entropy((x, y))
                # Add some noise to mix things up a little
                entropy_plus_noise = entropy - (random.random() / 1000)
                if min_entropy is None or entropy_plus_noise < min_entropy:
                    min_entropy = entropy_plus_noise
                    min_entropy_coords = (x, y)

        return min_entropy_coords


def render_colors(matrix, colors):
    """Render the fully collapsed `matrix` using the given `colors.

    Arguments:
    matrix -- 2-D matrix of tiles
    colors -- dict of tile -> `colorama` color
    """
    import colorama
    for row in matrix:
        output_row = []
        for val in row:
            color = colors.get(val, colorama.Fore.BLACK)
            output_row.append(color + val + colorama.Style.RESET_ALL)

        print("".join(output_row))


def valid_dirs(cur_co_ord, matrix_size):
    """Returns the valid directions from `cur_co_ord` in a matrix
    of `matrix_size`. Ensures that we don't try to take step to the
    left when we are already on the left edge of the matrix.
    """
    x, y = cur_co_ord
    width, height = matrix_size
    dirs = []

    if x > 0: dirs.append(LEFT)
    if x < width-1: dirs.append(RIGHT)
    if y > 0: dirs.append(DOWN)
    if y < height-1: dirs.append(UP)

    return dirs


def parse_example_matrix(matrix):
    """Parses an example `matrix`. Extracts:
    
    1. Tile compatibilities - which pairs of tiles can be placed next
        to each other and in which directions
    2. Tile weights - how common different tiles are

    Arguments:
    matrix -- a 2-D matrix of tiles

    Returns:
    A tuple of:
    * A set of compatibile tile combinations, where each combination is of
        the form (tile1, tile2, direction)
    * A dict of weights of the form tile -> weight
    """
    if isinstance(matrix, list):
        matrix = np.asarray(matrix)
    compatibilities = set()
    matrix_width = len(matrix)
    matrix_height = len(matrix[0])

    weights = {}

    for x, row in enumerate(matrix):
        for y, cur_tile in enumerate(row):
            if cur_tile not in weights:
                weights[cur_tile] = 0
            weights[cur_tile] += 1

            for d in valid_dirs((x,y), (matrix_width, matrix_height)):
                other_tile = matrix[x+d[0]][y+d[1]]
                compatibilities.add((cur_tile, other_tile, d))
    print(matrix[:, 0])
    border_tiles = {
        UP: set(matrix[0]),
        DOWN: set(matrix[-1]),
        LEFT: set(matrix[:, 0]),
        RIGHT: set(matrix[:, -1])
    }

    return compatibilities, weights, border_tiles

# custom
def make_edges_from_pairs(hpairs, vpairs):
    pairs = set()
    tiles = set()
    keys = {"->": RIGHT, "<-": LEFT, "^": DOWN, "v": UP}
    for x, y in hpairs:
        pairs.add((x, y, "->"))
        pairs.add((y, x, "<-"))
        tiles.update([x, y])
    for x, y in vpairs:
        pairs.add((y, x, "^"))
        pairs.add((x, y, "v"))
        tiles.update([x, y])
    pairs = {(k, v, keys[c]) for k, v, c in pairs}
    tiles = {k: 1 for k in tiles}
    return tiles, pairs

def get_():
    edges_v = [
        ["a90", "a270"],
        ["a90",   "a0"],
        ["a90",  "l90"],
        
        ["a180",  "a270" ],
        ["a180",   "a0" ],
        ["a180", "l270" ],
        
        ["l90",  "a270" ],
        ["l90",   "a0" ],
        ["l90", "l270" ],
        ["l90", "l90" ],
        
        ["l270", "a270"],
        ["l270", "a0"],
        ["l270", "l270"],
        ["l270", "l90"]
    ]
    edges_h = [
        ["a90", "a180"],
        ["a90", "a270"],
        ["a90", "l0"],
        ["a90", "l180"],
        
        ["a0", "a180"],
        ["a0", "a270"],
        ["a0", "l0"],
        ["a90", "l180"],
        
        ["l0", "a180"],
        ["l0", "a270"],
        ["l0", "l0"],
        ["l0", "l180"],
        
        ["l180", "a180"],
        ["l180", "a270"],
        ["l180", "l0"],
        ["l180", "l180"],
    ]
    tiles, pairs = make_edges_from_pairs(edges_v, edges_h)


    pass

if __name__ == "__main__":
    import colorama
    input_matrix = [
        ['L','L','L','L'],
        ['L','L','L','L'],
        ['L','L','L','L'],
        ['L','C','C','L'],
        ['C','S','S','C'],
        ['S','S','S','S'],
        ['S','S','S','S'],
    ]
    input_matrix2 = [
        ['A','A','A','A'],
        ['A','A','A','A'],
        ['A','A','A','A'],
        ['A','C','C','A'],
        ['C','B','B','C'],
        ['C','B','B','C'],
        ['A','C','C','A'],
    ]
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
    input_matrix3 = np.asarray(input_matrix3)
    
    compatibilities, weights, border_tiles = parse_example_matrix(input_matrix3)
    compatibility_oracle = CompatibilityOracle(compatibilities)
    model = Model((10, 50), weights, compatibility_oracle, border_tiles)
    output = model.run()

    colors = {
        'A': colorama.Fore.GREEN,
        'B': colorama.Fore.BLUE,
        'C': colorama.Fore.YELLOW,
        'D': colorama.Fore.CYAN,
        'E': colorama.Fore.MAGENTA,
        'F': colorama.Fore.RED,
        'G': colorama.Fore.MAGENTA,
        'H': colorama.Fore.WHITE,
        'J': colorama.Fore.MAGENTA,
    }

    render_colors(output, colors)