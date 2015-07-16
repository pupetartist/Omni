# -*- coding: utf-8 -*-

#from geopy.distance import vincenty
from routing import Path, Router
from geopy.point import Point

class MetroNode:
    def __init__(self, name, geolocation=None, connections=[]):
        self.__name = name
        self.__connections = set(connections)
        self.__geolocation = geolocation
        self.__routes = set()

    # For this model, cost is time in minutes
    @property
    def cost(self):
        return 0.5 # 30 seconds

    @property
    def key(self):
        return self.name

    @property
    def name(self):
        return self.__name

    @property
    def geolocation(self):
        return self.__geolocation

    @property
    def connections(self):
        return self.__connections

    @property
    def transport_type(self):
        return 'Subway'

    @property
    def provider(self):
        return 'STC Metro'

    @property
    def routes(self):
        return self.__routes

    # This is to take into account when stations are closed
    @property
    def status(self):
        pass

    @property
    def full_name(self):
        plural = 's' if len(self.routes) > 0 else ''
        return '%s (Route%s %s)' % (self.name, plural, ', '.join(self.routes))

    def shares_route(self, other):
        return (self.routes & other.routes) != set()

    def add_route(self, route):
        self.routes.add('metro-' + route)

    def add_connection(self, node):
        self.connections.add(node)

    def transfer_cost(self, route):
        if route not in self.routes:
            return float('inf')
        return 5.0 # minutes

    def estimate_cost(self, destination):
        if self.geolocation is None:
            return 0.0
        distance = vincenty(self.geolocation, destination.geolocation).km
        average_velocity_in_kmh = 30.0
        return distance / average_velocity_in_kmh

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __repr__(self):
        connections_repr = str(map(lambda node: node.full_name, self.connections))
        return '%s; Connections: %s' % (self.full_name, connections_repr)


class Network:
    def __init__(self):
        self.nodes = {}

    def get_or_create_node(self, node_name, route_name, geolocation):
        if node_name not in self.nodes:
            self.nodes[node_name] = MetroNode(node_name)
            self.nodes[node_name].geolocation = geolocation
        self.nodes[node_name].add_route(route_name)
        return self.nodes[node_name]

    def __repr__(self):
        s = ''
        for node in self.nodes.values():
            s += '%s\n' % str(node)
        return s

    def nodes(self):
        return self.nodes.keys()

    def node(self, name):
        return self.nodes.get(name)

    def node_connections(self, node_name):
        node = self.node(node_name)
        return node and node.connections()

    def connection_cost(self, from_node, to_node):
        return 1.5 # minutes


def is_valid_index(index, sequence):
    return index >= 0 and index < len(sequence)


def add_connection(network, route, from_index, to_index):
    if not is_valid_index(from_index, route.nodes) or \
       not is_valid_index(to_index, route.nodes):
        return

    key = route.nodes[from_index][0]
    geolocation = route.nodes[from_index][1]
    from_node = network.get_or_create_node(key, route.name, geolocation)

    key = route.nodes[to_index][0]
    geolocation = route.nodes[to_index][1]
    from_node.add_connection(network.get_or_create_node(key, route.name, geolocation))


def build_route_nodes(network, route):
    n = len(route.nodes)
    for i in range(n):
        add_connection(network, route, i, i+1)
        add_connection(network, route, i, i-1)

class RouteSequence:
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes

def load_network():
    route2 = RouteSequence('2', [
        ('Cuatro Caminos', Point()),
        ('Panteones', Point()),
        ('Tacuba', Point(19.459394, -99.189238)),
        ('Cuitlahuac', Point()),
        ('Popotla', Point()),
        ('Colegio Militar', Point()),
        ('Normal', Point()),
        ('San Cosme', Point()),
        ('Revolucion', Point()),
        ('Hidalgo', Point()),
        ('Bellas Artes', Point()),
        ('Allende', Point()),
        ('Zocalo', Point()),
        ('Pino Suarez', Point(19.425645, -99.132888)),
        ('San Antonio Abad', Point()),
        ('Chabacano', Point()),
        ('Viaducto', Point()),
        ('Xola', Point()),
        ('Villa de Cortes', Point()),
        ('Nativitas', Point()),
        ('Portales', Point()),
        ('Ermita', Point()),
        ('General Anaya', Point()),
        ('Tasqueña', Point()),
    ])

    route7 = RouteSequence('7', [
        ('El Rosario', Point()),
        ('Aquiles Serdan', Point()),
        ('Camarones', Point()),
        ('Refineria', Point()),
        ('Tacuba', Point()),
        ('San Joaquin', Point()),
        ('Polanco', Point()),
        ('Auditorio', Point()),
        ('Constituyentes', Point()),
        ('Tacubaya', Point(19.403140, -99.187113)),
        ('San Pedro de los Pinos', Point()),
        ('San Antonio', Point()),
        ('Mixcoac', Point()),
        ('Barranca del Muerto', Point()),
    ])

    route1 = RouteSequence('1', [
        ('Observatorio', Point()),
        ('Tacubaya', Point()),
        ('Juanacatlan', Point()),
        ('Chapultepec', Point()),
        ('Sevilla', Point()),
        ('Insurgentes', Point(19.423678, -99.163103)),
        ('Cuauhtemoc', Point()),
        ('Balderas', Point(19.427707, -99.149083)),
        ('Salto del Agua', Point()),
        ('Isabel la Catolica', Point()),
        ('Pino Suarez', Point()),
        ('Merced', Point()),
        ('Candelaria', Point()),
        ('San Lazaro', Point()),
        ('Moctezuma', Point()),
        ('Balbuena', Point()),
        ('Boulevard Puerto Aereo', Point()),
        ('Gomez Farías', Point()),
        ('Zaragoza', Point()),
        ('Pantitlan', Point()),
    ])

    network = Network()
    build_route_nodes(network, route2)
    build_route_nodes(network, route7)
    build_route_nodes(network, route1)

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

#geojson_test()
