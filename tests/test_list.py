"""Test zedenv create command"""

import datetime

import pytest

import pyzfsutils.lib.zfs.utility as zfs_utility

import zedenv.lib.check
import zedenv.cli.list
import zedenv.cli.create

require_root_dataset = pytest.mark.require_root_dataset


@require_root_dataset
def test_boot_environment_listed(root_dataset, capsys):
    parent_dataset = zfs_utility.dataset_parent(root_dataset)

    boot_environment = f"zedenv-{datetime.datetime.now().isoformat()}"

    verbose = True
    existing = False

    zedenv.cli.create.zedenv_create(parent_dataset, root_dataset,
                                    boot_environment, verbose, existing)

    be_list = zedenv.cli.list.configure_boot_environment_list(
        zfs_utility.dataset_parent(root_dataset))

    print(be_list)

    assert any(f"{boot_environment}" in s for s in be_list)