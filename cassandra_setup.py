from cassandra.cluster import Cluster

def setup_cassandra(config):
    """Set up and return a Cassandra session."""
    cassandra_conf = config['cassandra']
    cluster = Cluster(
        cassandra_conf['hosts'],
        port=cassandra_conf['port']
    )
    session = cluster.connect('cave_diving')
    return session, cluster
