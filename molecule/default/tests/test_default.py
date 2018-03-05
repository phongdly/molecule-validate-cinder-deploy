import os
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('aio1')


pre_cmd = "sudo bash -c \"source /root/openrc; "


def test_cinder_service(host):
    cmd = pre_cmd + "cinder service-list\""
    output = host.run(cmd)
    assert ("cinder-volume" in output.stdout)


def test_cinder_lvm_volume(host):
    cmd = pre_cmd + "pushd /opt/openstack-ansible; " \
          "ansible storage_hosts -m shell -a 'vgs cinder-volumes'\""
    output = host.run(cmd)
    assert re.search("cinder-volumes\s+[0-9]*\s+[0-9]*\s+", output.stdout)
    host.run('popd')


def test_cinder_volume_group(host):
    cmd = pre_cmd + "pushd /opt/openstack-ansible; " \
          "ansible cinder_volume -m shell -a " \
          "'grep volume_group /etc/cinder/cinder.conf'\""
    output = host.run(cmd)
    assert ("SUCCESS" in output.stdout)
    assert ("volume_group=cinder-volumes" in output.stdout)
    host.run('popd')


def test_verify_no_excess_free_extents(host):
    cmd = pre_cmd + "pushd /opt/openstack-ansible; " \
          "ansible compute_hosts -m shell -a 'vgs -o '" \
          "-pv_count,lv_count,snap_count,vg_attr,vg_size,vg_free " \
          "-o +vg_free_count\""
    output = host.checkout_outut(cmd)
    # debug
    if "cinder-volumes" in output:
        free_extents_count = re.search('(cinder-volumes\s+)[d+]*', output)
        if free_extents_count:
            assert('1234' in free_extents_count)
