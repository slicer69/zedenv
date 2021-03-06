"""Test zedenv setup"""

import pytest
import pyzfscmds.cmd
import pyzfscmds.check

import zedenv.main
import zedenv.lib.check
import zedenv.lib.be

from click.testing import CliRunner

require_zpool = pytest.mark.require_zpool
require_root_dataset = pytest.mark.require_root_dataset


@require_zpool
@require_root_dataset
@pytest.fixture(scope="function")
def set_bootfs_failure(request, zpool, root_dataset):
    print("bootfs setup:")
    pyzfscmds.cmd.zpool_set(zpool, 'bootfs=')

    def fin():
        print("Re-set bootfs teardown")
        pyzfscmds.cmd.zpool_set(zpool, f'bootfs={root_dataset}')

    request.addfinalizer(fin)
    return set_bootfs_failure


@require_zpool
def check_startup(zpool, set_bootfs_failure):
    with pytest.raises(RuntimeError):
        zedenv.lib.be.bootfs_for_pool(zpool)


@require_zpool
def test_boot_no_bootfs():
    try:
        exit_val = pyzfscmds.check.is_root_on_zfs()
    except RuntimeError:
        exit_val = False

    runner = CliRunner()
    result = runner.invoke(zedenv.main.cli, ['list'])

    """
    If system is root on ZFS the exit code will be zero,
    and there will not be an exception.
    """
    assert (result.exit_code == 0) is exit_val
    assert result.exception is not exit_val
