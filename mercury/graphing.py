
class NodeGraphBuilder:
    """
    Class that remembers the index of nodes as they are put in.
    """
    def __init__(self):
        self.nodes = []
        self.links = []

    def add_link(self, node1, node2, value=1):
        if node1 not in self.nodes:
            self.nodes.append(node1)
        if node2 not in self.nodes:
            self.nodes.append(node2)

        self.links.append({
            "source": self.nodes.index(node1),
            "target": self.nodes.index(node2),
            "value": value
        })

    def to_hash(self):
        nodes = map(lambda x: {
            "ip": x.ip_address,
            "names": [
                x.dns_name,
            ],
        }, self.nodes)
        return { "nodes": list(nodes), "links": self.links }
