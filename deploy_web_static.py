#!/usr/bin/python3
"""A module for web application deployment with Fabric."""
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ['100.26.246.108', '34.239.207.152']
"""The list of host server IP addresses."""


@runs_once
def do_pack():
    """Archives the dynamic files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_dynamic_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_dynamic to {}".format(output))
        local("tar -cvzf {} web_dynamic".format(output))
        archize_size = os.stat(output).st_size
        print("web_dynamic packed: {} -> {} Bytes".format(output, archize_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """Deploys the dynamic files to the host servers.
    Args:
        archive_path (str): The path to the archived dynamic files.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_dynamic/releases/{}/".format(folder_name)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_dynamic/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_dynamic".format(folder_path))
        run("rm -rf /data/web_dynamic/current")
        run("ln -s {} /data/web_dynamic/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """Archives and deploys the dynamic files to the host servers.
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False

