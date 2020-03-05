import click
import logging
import openstack
import time
import yaml

from pathlib import Path

from prometheus_client.core import REGISTRY
from prometheus_client import start_http_server

from nova_exporter.collector import NovaCollector

LOG = logging.getLogger(__name__)


@click.command()
@click.option('--os-cloud')
@click.option('-l', '--listen', default='0.0.0.0')
@click.option('-p', '--port', default=5113)
@click.option('-v', '--verbose', count=True, default=0,
              type=click.IntRange(0, 2))
def main(os_cloud, verbose, listen, port):
    loglevel = ['WARNING', 'INFO', 'DEBUG'][verbose]
    logging.basicConfig(level=loglevel)

    cloud = openstack.connect(cloud=os_cloud)

    REGISTRY.register(NovaCollector(
        cloud
    ))

    LOG.info('starting server on %s port %d', listen, port)
    start_http_server(port, addr=listen)
    while True:
        time.sleep(3600)


if __name__ == '__main__':
    main()
