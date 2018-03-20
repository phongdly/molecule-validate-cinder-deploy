import os
import re
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.jira('asc-222')
# Experimental test
def test_find_openrc_on_root(host):
    cmd = "find /root -name openrc -print | grep openrc"
    assert host.run(cmd)


# Experimental test
def test_find_openrc_on_opt(host):
    cmd = "find /opt -name openrc -print | grep openrc"
    assert host.run(cmd)


# Experimental test
def test_find_openrc_on_etc(host):
    cmd = "find /etc -name openrc -print | grep openrc"
    assert host.run(cmd)


# Experimental test
def test_cinder_service(host):

    # fail test immediately if no cinder client on the host
    assert host.exists("cinder")
    if host.file('/root/openrc').exists:
        cmd = "sudo bash -c \"source /root/openrc; cinder service-list\""
        output = host.run(cmd)
        assert ("cinder-volume" in output.stdout)


# Experimental test
def test_cinder_api_status(host):
    assert host.service('cinder-api').is_running


# Experimental test
def test_cinder_schuduler_status(host):
    assert host.service('cinder-scheduler').is_running


# Experimental test
def test_cinder_volume_status(host):
    assert host.service('cinder-volume').is_running


# Experimental test
def test_cinder_backup_status(host):
    assert host.service('cinder-backup').is_running