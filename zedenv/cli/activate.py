"""List boot environments cli"""

import click
import pyzfsutils.lib.zfs.linux as zfs_linux
import pyzfsutils.lib.zfs.utility as zfs_utility
from pyzfsutils.lib.zfs.command import ZFS

import zedenv.lib.configure
import zedenv.lib.boot_environment as be
from zedenv.lib.logger import ZELogger


def zedenv_activate(boot_environment, verbose, bootloader, legacy):
    """
    :Parameters:
      boot_environment : str
        Name of boot environment to activate
      verbose : bool
        Print information verbosely.
    :return:
    """

    if bootloader:
        plugins = zedenv.lib.configure.get_plugins()
        if bootloader in plugins:
                ZELogger.verbose_log({
                    "level": "INFO",
                    "message": "Configuring boot environment "
                               f"bootloader with {bootloader}\n"
                }, verbose)
                bootloader_plugin = plugins[bootloader]()
                ZELogger.verbose_log({
                    "level": "INFO",
                    "message": f"Plugin {bootloader_plugin}\n"
                }, verbose)
        else:
            ZELogger.log({
                "level": "EXCEPTION",
                "message": f"bootloader type {bootloader} does not exist\n"
                           "Check available plugins with 'zedenv --plugins'\n"
            }, exit_on_error=True)

    ZELogger.verbose_log({
        "level": "INFO",
        "message": f"Activating Boot Environment: {boot_environment}\n"
    }, verbose)


@click.command(name="activate",
               help="Activate a boot environment.")
@click.option('--verbose', '-v',
              is_flag=True,
              help="Print verbose output.")
@click.option('--bootloader', '-b',
              help="Use bootloader type.")
@click.option('--legacy', '-l',
              is_flag=True,
              help="Legacy mountpoint type.")
@click.argument('boot_environment')
def cli(boot_environment, verbose, bootloader, legacy):
    zedenv_activate(boot_environment, verbose, bootloader, legacy)