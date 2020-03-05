import json
import logging
import re

from prometheus_client.core import GaugeMetricFamily

LOG = logging.getLogger(__name__)
re_invalid_chars = re.compile(r'[^\w]+')


class NovaCollector(object):
    def __init__(self, cloud):
        self.cloud = cloud

    def get_hypervisor_metrics(self):
        metrics = []

        nova_hypervisor_up = GaugeMetricFamily(
            'nova_hypervisor_up',
            'Metadata about a Nova hypervisor',
            labels=[
                'nova_hypervisor_id',
                'nova_hypervisor_name',
                'nova_hypervisor_up',
                'nova_hypervisor_enabled',
                'nova_hypervisor_type',
                'nova_hypervisor_version',
                'nova_hypervisor_cpu_vendor',
                'nova_hypervisor_cpu_model',
                'nova_hypervisor_cpu_arch', 
            ])
        metrics.append(nova_hypervisor_up)

        nova_hypervisor_vcpus = GaugeMetricFamily(
            'nova_hypervisor_vcpus',
            'Number of vcpus available',
            labels=['nova_hypervisor_id'],
        )
        metrics.append(nova_hypervisor_vcpus)

        nova_hypervisor_vcpus_used = GaugeMetricFamily(
            'nova_hypervisor_vcpus',
            'Number of vcpus in use',
            labels=['nova_hypervisor_id'],
        )
        metrics.append(nova_hypervisor_vcpus_used)

        nova_hypervisor_running_vms = GaugeMetricFamily(
            'nova_hypervisor_running_vms',
            'Number of vms running on this hypervisor',
            labels=['nova_hypervisor_id'],
        )
        metrics.append(nova_hypervisor_running_vms)

        nova_hypervisor_local_disk_size = GaugeMetricFamily(
            'nova_hypervisor_local_disk_size',
            'Amount of local disk available on this hypervisor',
            labels=['nova_hypervisor_id'],
        )
        metrics.append(nova_hypervisor_local_disk_size)

        nova_hypervisor_local_disk_used = GaugeMetricFamily(
            'nova_hypervisor_local_disk_used',
            'Amount of local disk used on this hypervisor',
            labels=['nova_hypervisor_id'],
        )
        metrics.append(nova_hypervisor_local_disk_used)

        nova_hypervisor_local_disk_free = GaugeMetricFamily(
            'nova_hypervisor_local_disk_free',
            'Amount of local disk free on this hypervisor',
            labels=['nova_hypervisor_id'],
        )
        metrics.append(nova_hypervisor_local_disk_free)

        nova_hypervisor_memory_size = GaugeMetricFamily(
            'nova_hypervisor_memory_size',
            'Amount of memory available on this hypervisor',
            labels=['nova_hypervisor_id'],
        )
        metrics.append(nova_hypervisor_memory_size)

        nova_hypervisor_memory_used = GaugeMetricFamily(
            'nova_hypervisor_memory_used',
            'Amount of memory used on this hypervisor',
            labels=['nova_hypervisor_id'],
        )
        metrics.append(nova_hypervisor_memory_used)

        nova_hypervisor_memory_free = GaugeMetricFamily(
            'nova_hypervisor_memory_free',
            'Amount of memory free on this hypervisor',
            labels=['nova_hypervisor_id'],
        )
        metrics.append(nova_hypervisor_memory_free)

        nova_hypervisor_current_workload = GaugeMetricFamily(
            'nova_hypervisor_current_workload',
            'Number of hypervisor tasks',
            labels=['nova_hypervisor_id'],
        )
        metrics.append(nova_hypervisor_current_workload)

        for hv in self.cloud.list_hypervisors():
            LOG.debug('gathering metrics for hypervisor %s (%s)',
                      hv.name, hv.id)
            if not isinstance(hv.cpu_info, dict):
                cpu = json.loads(hv.cpu_info)
            else:
                cpu = hv.cpu_info

            hvid = str(hv.id)
            nova_hypervisor_up.add_metric([
                hvid,
                hv.name,
                'true' if hv.state == 'up' else 'false',
                'true' if hv.status == 'enabled' else 'false',
                hv.hypervisor_type,
                str(hv.hypervisor_version),
                cpu['vendor'],
                cpu['model'],
                cpu['arch'],
            ], 1.0)

            nova_hypervisor_vcpus.add_metric([hvid], hv.vcpus)
            nova_hypervisor_vcpus_used.add_metric([hvid], hv.vcpus_used)
            nova_hypervisor_running_vms.add_metric([hvid], hv.running_vms)
            nova_hypervisor_local_disk_size.add_metric([hvid], hv.local_disk_size)
            nova_hypervisor_local_disk_used.add_metric([hvid], hv.local_disk_used)
            nova_hypervisor_local_disk_free.add_metric([hvid], hv.local_disk_free)
            nova_hypervisor_memory_size.add_metric([hvid], hv.memory_size)
            nova_hypervisor_memory_used.add_metric([hvid], hv.memory_used)
            nova_hypervisor_memory_free.add_metric([hvid], hv.memory_free)
            nova_hypervisor_current_workload.add_metric([hvid], hv.current_workload)

        yield from iter(metrics)

    def describe(self):
        return []

    def collect(self):
        LOG.info('start collecting hypervisor information')
        yield from self.get_hypervisor_metrics()
        LOG.info('done collecting hypervisor information')
