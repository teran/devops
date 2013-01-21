from django.test import TestCase
from ipaddr import IPNetwork, IPv4Network
from devops.helpers.network import IpNetworksPool
from devops.manager import Manager


class TestManager(TestCase):

    manager = Manager()

    def test_getting_subnetworks(self):
        pool = IpNetworksPool(networks=[IPNetwork('10.1.0.0/22')], prefix=24)
        pool.set_allocated_networks([IPv4Network('10.1.1.0/24')])
        networks  = list(pool)
        self.assertTrue(IPv4Network('10.1.0.0/24') in networks)
        self.assertFalse(IPv4Network('10.1.1.0/24') in networks)
        self.assertTrue(IPv4Network('10.1.2.0/24') in networks)
        self.assertTrue(IPv4Network('10.1.3.0/24') in networks)

    def test_getting_ips(self):
        self.assertEquals('10.1.0.254', str(IPv4Network('10.1.0.0/24')[-2]))

    def test_network_iterator(self):
        environment = self.manager.environment_create('test_env')
        node = self.manager.node_create('test_node', environment)
        network = self.manager.network_create(
            environment=environment, name='internal', ip_network='10.1.0.0/24')
        interface = self.manager.network_create_interface(network=network, node=node)
        self.manager.network_create_address(str('10.1.0.1'),interface=interface)
        ip = network.next_ip()
        self.manager.network_create_address(str('10.1.0.3'),interface=interface)
        ip = network.next_ip()
        self.assertEquals('10.1.0.4', str(ip))

    def test_environment_values(self):
        environment = self.manager.environment_create('test_env')
        print environment.volumes

    def test_network_pool(self):
        environment = self.manager.environment_create('test_env')
        self.assertEqual('10.0.0.0/24', str(self.manager.network_create(
            environment=environment, name='internal', pool=None).ip_network))
        self.assertEqual('10.0.1.0/24', str(self.manager.network_create(
            environment=environment, name='external', pool=None).ip_network))
        self.assertEqual('10.0.2.0/24', str(self.manager.network_create(
            environment=environment, name='private', pool=None).ip_network))
        environment = self.manager.environment_create('test_env2')
        self.assertEqual('10.0.3.0/24', str(self.manager.network_create(
            environment=environment, name='internal', pool=None).ip_network))
        self.assertEqual('10.0.4.0/24', str(self.manager.network_create(
            environment=environment, name='external', pool=None).ip_network))
        self.assertEqual('10.0.5.0/24', str(self.manager.network_create(
            environment=environment, name='private', pool=None).ip_network))


    def test_node_creationw(self):
        node = self.manager.node_create(name='test_node', environment=None)
        node.define()

    def test_node_creation(self):
        environment = None
        try:
            print 1
            environment = self.manager.environment_create('test_env2')
            internal = self.manager.network_create(
                environment=environment, name='internal', pool=None)
#            external = self.manager.create_network(
#                environment=environment, name='external', pool=None)
#            private = self.manager.create_network(
#                environment=environment, name='private', pool=None)
            node = self.manager.node_create(name='test_node', environment=environment)
            self.manager.network_create_interface(node=node, network=internal)
#            self.manager.create_interface(node=node, network=external)
#            self.manager.create_interface(node=node, network=private)
            environment.define()
        except:
            if environment:
                environment.erase()
            raise

    def test_use_exist_volume(self):
        volume = self.manager.volume_get_predefined('/var/lib/libvirt/images/disk-135871063107.qcow2')
        print volume.format
        print volume.capacity
        print volume.uuid

    def test_create_volume(self):
        volume = self.manager.volume_get_predefined('/var/lib/libvirt/images/disk-135871063107.qcow2')
        v3 = self.manager.volume_create('test_vp7', None, volume.capacity, volume.format, backing_store=volume)
        v3.define()





