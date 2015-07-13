from containers import PriorityQueue, OrderedSet
import geojson
import json

class Path:
    def __init__(self, end=None, cost=0):
        self.previous = None
        self.end = end
        self.cost = cost
        self.nodes = OrderedSet([] if end is None else [end])

    def __len__(self):
        return len(self.nodes)

    @property
    def points(self):
        return list(self.nodes)

    @property
    def __geo_interface__(self):
        features = []
        for node in self.nodes:
            features.append(self.as_geojson_feature(node))
        return {
            'status': 'ok',
            'content': {
                'cost': self.cost,
                'route_nodes': {
                    'type': 'FeatureCollection',
                    'features': features
                }
            }
        }

    def as_geojson_feature(self, node):
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': (
                    node.geolocation.longitude if node.geolocation else 0.0,
                    node.geolocation.latitude if node.geolocation else 0.0
                )
            },
            'properties': {
                'node-name': node.name,
                'transport-type': node.transport_type,
                'provider': node.provider,
                'routes': list(node.routes)
            }
        }

    @classmethod
    def as_geojson(cls, path):
        if path is None:
            return json.dumps({'status': 'fail'})
        return geojson.dumps(path.__geo_interface__,
                             indent=4, separators=(',', ': '))

    def estimated_final_cost(self, destination):
        return self.cost + self.end.estimate_cost(destination)

    def append(self, node):
        self.nodes.add(node)

    def is_transfer(self, expansion_node):
        return self.previous and not self.previous.shares_route(expansion_node)

    def clone(self):
        path = Path()
        path.nodes = OrderedSet(self.nodes)
        path.end = self.end
        path.previous = self.previous
        path.cost = self.cost
        return path

    def extend(self, node, network):
        if node in self.nodes:
            return None

        new_path = self.clone()
        new_path.append(node)

        if not self.is_transfer(node):
            transfer_cost = 0
        else:
            transfer_routes = (self.end.routes - self.previous.routes) & node.routes
            assert len(transfer_routes) == 1
            transfer_cost = self.end.transfer_cost(transfer_routes.pop())

        # print 'transfer_cost between %s and %s is %f' % \
        #     (self.end.name, node.name, transfer_cost)
        new_path.cost += (
            new_path.end.cost +
            network.connection_cost(new_path.end, node) +
            transfer_cost
        )
        new_path.previous = new_path.end
        new_path.end = node
        new_path.nodes.add(node)

        return new_path

    def __repr__(self):
        nodes = str(map(lambda n: n.name, self.nodes))
        return 'Cost: %f\n%s' % (self.cost, nodes)


class Router:
    def __init__(self, connections):
        self.connections = connections

    def ensure_node(self, obj):
        if type(obj) is str or type(obj) is unicode:
            obj = self.connections.node(obj)
        return obj

    def enroute(self, origin, destination):
        origin = self.ensure_node(origin)
        destination = self.ensure_node(destination)

        if origin is None or destination is None:
            return None

        if origin == destination:
            return Path(end=origin)

        empty_path = Path(origin)
        item = (empty_path.estimated_final_cost(destination), empty_path)
        paths = PriorityQueue([item])
        while not paths.is_empty():
            cost, path = paths.pop()
            if path.end == destination:
                return self.compress_path(path)

            for node in path.end.connections:
                extended_path = path.extend(node, self.connections)
                if extended_path:
                    item = (extended_path.estimated_final_cost(destination),
                            extended_path)
                    paths.add(item)

        # If there was no complete path, we return the path that came closest
        return self.compress_path(paths.pop()) if not paths.is_empty() else None

    def compress_path(self, path):
        assert len(path) > 0

        segment_start = path.points[0]
        crucial_nodes = [segment_start]
        previous = segment_start
        for node in path.points[1:]:
            if segment_start.routes & node.routes == set(): # a transfer has been done
                crucial_nodes.append(previous)
                segment_start = previous
            previous = node

        if len(path) > 1:
            crucial_nodes.append(path.points[-1])
        compressed_path = Path(cost=path.cost)
        compressed_path.end = path.end
        compressed_path.nodes = OrderedSet(crucial_nodes)
        return compressed_path
