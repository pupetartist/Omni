# -*- coding: utf-8 -*-

from model import Network, Route, GenericFactory
from routing import Path, Router


def add_connection(network, route, from_index, to_index):
    def is_valid_index(index, sequence):
        return 0 <= index < len(sequence)

    if not is_valid_index(from_index, route.nodes) or \
       not is_valid_index(to_index, route.nodes):
        return

    key = route.nodes[from_index][0]
    geolocation = route.nodes[from_index][1]
    from_node = network.get_or_create_node(key, route.name, geolocation)

    key = route.nodes[to_index][0]
    geolocation = route.nodes[to_index][1]
    from_node.add_connection(network.get_or_create_node(key, route.name, geolocation))


def load_network():
    network = Network()
    #build_route_nodes(network, route2)
    #build_route_nodes(network, route7)
    #build_route_nodes(network, route1)

    return network


def build_weighted_path(network, nodes_names):
    n = len(nodes_names)
    path = Path(network.node(nodes_names[0]))
    for i in range(1, n):
        path = path.extend(network.node(nodes_names[i]), network)
    return path


def test1():
    network = load_network()
    path0 = build_weighted_path(
        network,
        ['Cuatro Caminos', 'Panteones', 'Tacuba', 'Cuitlahuac'])

    print path0
    print

    path1 = build_weighted_path(
        network,
        ['Cuatro Caminos', 'Panteones', 'Tacuba', 'Refineria', 'Camarones'])
    print path1
    print


def test_route(begin, end):
    network = load_network()
    router = Router(network)
    path = router.enroute(network.node(begin), network.node(end))
    if path is None:
        print 'Cannot find path between %s and %s' % (begin, end)
    else:
        print path


def smoke_test():
    test_route('Cuatro Caminos', 'Cuatro Caminos')
    test_route('Cuatro Caminos', 'Tacuba')
    test_route('Cuatro Caminos', 'Colegio Militar')
    test_route('Cuatro Caminos', 'Tasqueña')


def functional_test():
    test_route('Cuatro Caminos', 'Insurgentes')


def geojson_test(begin='Cuatro Caminos', end='Juanacatlan'):
    network = load_network()
    router = Router(network)
    path = router.enroute(network.node(begin), network.node(end))
    print Path.as_geojson(path)


if __name__ == "__main__":
    # geojson_test()

    f = GenericFactory.get_instance()

    #node = f.create_object('00c17928-b42c-42e6-ba26-20e83799ca4a')
    #print (node)

    #route = f.create_object('a213390f-b6ff-44e7-ace7-a920c9051cc2')
    #print (route)

    routes = Route.all_routes()
    print (routes)
