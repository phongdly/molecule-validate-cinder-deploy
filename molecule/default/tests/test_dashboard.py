import os
import re
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('cinder_volume')


@pytest.mark.jira('asc-222')
def test_cinder_service(host):
    """Test to verify that cinder service is running on the cinder nodes

    Args:
        host(testinfra.host.Host): A hostname in dynamic_inventory.json/molecule.yml
    """
    if not host.file('/root/openrc').exists:
        pytest.skip('openrc file not found')
    elif host.file('/root/openrc').exists:
        cmd = "sudo bash -c \"source /root/openrc; cinder service-list\""
        output = host.run(cmd)
        if output.rc != 0:
            pytest.skip('cinder client is not available')
        elif output.rc == 0:
            assert ("cinder-volume" in output.stdout)
