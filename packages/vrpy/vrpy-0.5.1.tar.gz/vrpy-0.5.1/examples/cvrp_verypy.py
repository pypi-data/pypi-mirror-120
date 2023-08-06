from networkx import from_numpy_matrix, set_node_attributes, relabel_nodes, DiGraph
from numpy import array
from examples.data import DISTANCES, DEMANDS

from vrpy import VehicleRoutingProblem

import sys

sys.path.append("../VeRyPy/")

from classic_heuristics.parallel_savings import (
    parallel_savings_init,
)

from classic_heuristics.cheapest_insertion import (
    cheapest_insertion_init,
)
from classic_heuristics.nearest_neighbor import (
    nearest_neighbor_init,
)
from util import sol2routes, objf

# Transform distance matrix to DiGraph
A = array(DISTANCES, dtype=[("cost", int)])
G = from_numpy_matrix(A, create_using=DiGraph())

# Set demands
set_node_attributes(G, values=DEMANDS, name="demand")

# Relabel depot
G = relabel_nodes(G, {0: "Source", 17: "Sink"})

if __name__ == "__main__":

    prob = VehicleRoutingProblem(G, load_capacity=15)
    # prob.solve()
    # print(prob.best_value)
    # print(prob.best_routes)
    # assert prob.best_value == 6208

    from networkx import to_numpy_array

    nodes = [v for v in prob.G.nodes() if v != "Sink"]
    # nodes = ["Source", 1, 2]

    matrix = to_numpy_array(
        prob.G, weight="cost", nodelist=nodes, nonedge=100000000000000
    )
    demands = list(dict(prob.G.nodes(data="demand")).values())
    for row in range(len(matrix)):
        matrix[row][0] = matrix[0][row]

    # print(dict(G.nodes(data="demand")))
    print(list(dict(G.nodes(data="demand")).values()))

    solution = parallel_savings_init(
        D=matrix,
        d=demands,
        C=prob.load_capacity,
    )

    print(
        "total cost =",
        objf(
            solution,
            matrix,
        ),
    )
    for route_idx, route in enumerate(sol2routes(solution)):
        print("Route #%d : %s" % (route_idx + 1, route), sum(DEMANDS[v] for v in route))

    solution = nearest_neighbor_init(D=matrix, d=demands, C=prob.load_capacity, L=None)

    print(
        "total cost =",
        objf(
            solution,
            matrix,
        ),
    )
