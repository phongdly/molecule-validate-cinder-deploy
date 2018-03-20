import os
import re
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.jira('asc-222')
# Experimental test
def test_find_openrc_on_root(host):
    assert host.file("/root/openrc").exists


# Experimental test
def test_find_openrc_on_opt(host):
    assert host.file("/opt/openrc").exists


# Experimental test
def test_find_openrc_on_etc(host):
    assert host.file("/etc/openrc").exists

# Experimental test
def test_find_cinder_client(host):
    assert host.exists("cinder")


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