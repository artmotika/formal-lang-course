from cfpq_data import download
from cfpq_data import graph_from_csv
from cfpq_data import labeled_two_cycles_graph
from networkx.drawing.nx_pydot import to_pydot


# Takes graph from cfpq_data.dataset.DATASET and returns MultiDiGraph from networkx
def get_graph(graph_name):
    graph_path = download(graph_name)
    return graph_from_csv(graph_path)


# Returns number of vertecies and edges also returns all labels
def get_graph_count_vertex_edges_labels(graph_name):
    graph = get_graph(graph_name)
    return (
        graph.number_of_nodes(),
        graph.number_of_edges(),
        {el["label"] for (_, _, el) in graph.edges(data=True)},
    )


# Builds graph and saves in dot format file
def build_two_cycles_graph_dot_format(
    num_vertexes_first_cycle: int,
    num_vertexes_second_cycle: int,
    labels: (str, str),
    file_path,
):
    graph = labeled_two_cycles_graph(
        num_vertexes_first_cycle, num_vertexes_second_cycle, labels=labels
    )
    # remove '\n' because read_dot from networkx create vertex '\n'
    open(file_path, "w").write(to_pydot(graph).to_string().replace("\n", ""))
