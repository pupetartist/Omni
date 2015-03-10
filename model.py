from geopy.distance import vincenty
from bluemix.cloudant_manager import account

__author__ = 'fer'


class Route:
    def __init__(self, _id, d):
        self.__id = _id
        self.__name = d['name']
        self.__transport_type = d['transport_type']
        self.__provider = d['transport_provider']
        self.__components = []
        self.__start_node = None
        self.__finish_node = None

    @property
    def start_node(self):
        return self.__start_node

    @start_node.setter
    def start_node(self, value):
        self.__start_node = value

    @property
    def finish_node(self):
        return self.__finish_node

    @finish_node.setter
    def finish_node(self, value):
        self.__finish_node = value

    @property
    def key(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def transport_type(self):
        return self.__transport_type

    @property
    def provider(self):
        return self.__provider

    @property
    def components(self):
        return self.__components

    def add_component(self, node_obj):
        self.__components.append(node_obj)

    @classmethod
    def all_routes(cls):
        ret = []
        db = account.database('omnimobi')
        d = db.design('routes').view('routes_index')
        factory = GenericFactory.get_instance()

        for x in d.iter():
            ret.append(factory.create_object(x['id']))

        return ret


class NodeConnection:
    def __init__(self):
        self.__backward = None
        self.__forward = None
        self.__route = None

    @property
    def backward(self):
        return self.__backward

    @backward.setter
    def backward(self, value):
        self.__backward = value

    @property
    def forward(self):
        return self.__forward

    @forward.setter
    def forward(self, value):
        self.__forward = value

    @property
    def route(self):
        return self.__route

    def __str__(self):
        forward_id = '' if self.forward is None else self.forward.key
        backward_id = '' if self.backward is None else self.backward.key
        route_id = '' if self.route is None else self.route.key
        return 'NodeConnection${0}${1}${2}'.format(route_id, forward_id, backward_id)

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        if not isinstance(other, NodeConnection):
            return False
        return self.__str__() == other.__str__()


class MetroNode:
    def __init__(self, _id, d):
        self.__id = _id
        self.__name = d['name']
        self.__geolocation = d['geolocation']
        self.__transport_type = d['transport_type']
        self.__provider = d['transport_provider']
        self.__routes = dict()
        self.__connections = dict()

    # For this model, cost is time in minutes
    @property
    def cost(self):
        return 0.5 # 30 seconds

    @property
    def key(self):
        return self.__id

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
        return self.__transport_type

    @property
    def provider(self):
        return self.__provider

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

    def add_route(self, route_id, route_obj):
        self.__routes[route_id] = route_obj

    def add_connection(self, route_id, conn_obj):
        self.__connections[route_id] = conn_obj

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
        if not isinstance(other, MetroNode):
            return False
        return self.__id == other.__id

    def __hash__(self):
        return hash(self.__id)

    def __repr__(self):
        connections_repr = str(self.__connections.keys())
        return '%s; Connections: %s' % (self.full_name, connections_repr)


class Network:
    def __init__(self):
        self.nodes = {}

    def get_or_create_node(self, node_id):
        factory = GenericFactory.get_instance()
        if node_id not in self.nodes:
            self.nodes[node_id] = factory.create_object(node_id)
        self.nodes[node_id]
        return self.nodes[node_id]

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


class GenericFactory:
    __instance = None

    def __init__(self, db_name='omnimobi'):
        self.db_name = db_name
        self.db = account.database(db_name)
        self.object_instances = dict()

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = GenericFactory()

        return cls.__instance

    def create_connection(self, conn_data):
        forward_id = '' if not 'node_id_foward' in conn_data else conn_data['node_id_foward']
        backward_id = '' if not 'node_id_backward' in conn_data else conn_data['node_id_backward']
        route_id = '' if not 'route_id' in conn_data else conn_data['route_id']
        conn_id = 'NodeConnection${0}${1}${2}'.format(route_id, forward_id, backward_id)

        if conn_id in self.object_instances:
            return self.object_instances[conn_id]

        conn = NodeConnection()
        self.object_instances[conn_id] = conn

        factory = GenericFactory.get_instance()
        if forward_id != '':
            conn.forward = factory.create_object(forward_id)
        if backward_id != '':
            conn.backward = factory.create_object(backward_id)
        if route_id != '':
            conn.route = factory.create_object(route_id)

        return conn

    def create_object(self, node_id):
        if node_id in self.object_instances:
            return self.object_instances[node_id]

        resp = self.db.document(node_id)
        req = resp.get()
        d = req.json()
        factory = GenericFactory.get_instance()

        if d['type'] == 'node':
            req = MetroNode(node_id, d)
            self.object_instances[node_id] = req
            for conn in d['connections']:
                x = factory.create_connection(conn)
                req.add_connection(conn['route_id'], x)
            for r in d['routes']:
                req.add_route(r, factory.create_object(r))
        elif d['type'] == 'route':
            req = Route(node_id, d)
            self.object_instances[node_id] = req
            req.start_node = factory.create_object(d['start_node_id'])
            req.finish_node = factory.create_object(d['finish_node_id'])
            for node_id in d['components']:
                req.add_component(factory.create_object(node_id))

        return req


class RouteSequence:
    def __init__(self, name, nodes):
        self.name = name
        self.nodes = nodes
