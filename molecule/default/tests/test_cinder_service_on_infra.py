import os
import re
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('compute-infra_hosts')


@pytest.mark.jira('asc-222')
# Experimental test
def test_cinder_service(host):

    # fail test immediately if no cinder client on the host
    assert host.exists("cinder")
    if host.file('/root/openrc').exists:
        cmd = "sudo bash -c \"source /root/openrc; cinder service-list\""
        output = host.run(cmd)
        assert ("cinder-volume" in output.stdout)
