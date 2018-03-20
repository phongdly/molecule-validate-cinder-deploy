import os
import re
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.jira('asc-222')
def test_cinder_service_on_all(host):
    """Test to verify that cinder service is running on the cinder nodes

    Args:
        host(testinfra.host.Host): A hostname in dynamic_inventory.json/molecule.yml
    """

    if not host.file('/root/openrc').exists:
        raise Exception('openrc file not found')
    elif host.file('/root/openrc').exists:
        cmd = "sudo bash -c \"source /root/openrc; cinder service-list\""
        output = host.run(cmd)
        if output.rc != 0:
            raise Exception('cinder client is not available')
        elif output.rc == 0:
            assert ("cinder-volume" in output.stdout)


# Experimental tess
def test_cinder_api_status_on_all_host(host):
    assert host.service('cinder-api').is_running


# Experimental tess
def test_cinder_schuduler_status_on_all_host(host):
    assert host.service('cinder-scheduler').is_running


# Experimental tess
def test_cinder_volume_status_on_all_host(host):
    assert host.service('cinder-volume').is_running


# Experimental tess
def test_cinder_backup_status_on_all_host(host):
    assert host.service('cinder-backup').is_running