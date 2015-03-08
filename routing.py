from containers import PriorityQueue, OrderedSet
import copy

class Path:
    def __init__(self, end, cost=0):
        self.previous = None
        self.end = end
        self.cost = cost
        self.nodes = OrderedSet([end])

    def estimated_final_cost(self, destination):
        return self.cost + self.end.estimate_cost(destination)

    def append(self, node):
        self.nodes.add(node)

    def is_transfer(self, expansion_node):
        return self.previous and not self.previous.shares_route(expansion_node)

    def extend(self, node, network):
        if node in self.nodes:
            return None

        new_path = Path(self)

        if not self.is_transfer(node):
            transfer_cost = 0
        else:
            transfer_routes = (self.end.routes - self.previous.routes) & node.routes
            assert len(transfer_routes) == 1
            transfer_cost = self.end.transfer_cost(transfer_routes.pop())

        print 'transfer_cost between %s and %s is %f' % \
            (self.end.name, node.name, transfer_cost)
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

    def enroute(self, origin, destination):
        if origin == destination:
            return Path(end=origin)

        empty_path = Path(origin)
        item = (empty_path.estimated_final_cost(destination), empty_path)
        paths = PriorityQueue([item])
        while not paths.is_empty():
            cost, path = paths.pop()
            if path.end == destination:
                return path

            for node in path.end.connections:
                extended_path = path.extend(node, self.connections)
                if extended_path:
                    item = (extended_path.estimated_final_cost(destination),
                            extended_path)
                    paths.add(item)

        # If there was no complete path, we return the path that came closest
        return paths.pop() if not paths.is_empty() else None
