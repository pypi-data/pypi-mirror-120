import os
import shutil

import typer
from loguru import logger
from pyfzf.pyfzf import FzfPrompt


def create_link(
    fname: str,
    is_delete: bool = typer.Option(False, "--d", help="delete dst if exists"),
):
    """
    create softlink to another disk, mostly for data disk
    """
    cwd = os.getcwd()
    if cwd.startswith(f"/home/{os.getlogin()}"):
        path_split = cwd.split("/")
        path_relative_home = path_split[3:]
        dst = os.path.join(cwd, fname)
        if os.path.exists(dst):
            logger.warning(f"{dst} already exists")
            if is_delete:
                if os.path.islink(dst):
                    os.unlink(dst)
                else:
                    shutil.rmtree(dst, ignore_errors=True)
            else:
                exit(0)
        src_dist = [
            fdir
            for fdir in os.listdir("/")
            if "hd" in fdir or "hhd" in fdir or "ssd" in fdir or "scratch" in fdir
        ]
        try:
            select = os.environ["DATA_DISK"]
        except Exception as error:  # pylint: disable=broad-except
            logger.warning("Env DATA_DISK not SET, use FZF")
            try:
                fzf = FzfPrompt()
                select = fzf.prompt(src_dist)
            except Exception as error:  # pylint: disable=broad-except
                print("FZF error: {}".format(error))

        logger.warning(f"src select disk: {select[0]}")
        src = os.path.join("/", select[0], os.getlogin(), *path_relative_home, fname)
        os.makedirs(src, exist_ok=True)
        logger.info(f"{src} ====> {dst}")
        os.symlink(src, dst)


def delete_link(
    fname: str,
    is_delete: bool = typer.Option(False, "--d", help="delete src folder"),
):
    """
    delete link
    """
    cwd = os.getcwd()
    dst = os.path.join(cwd, fname)
    if os.path.exists(dst):
        if os.path.islink(dst):
            src = os.readlink(dst)
            if is_delete:
                logger.warning(f" Deleting SRC: {src} ==> {dst}")
            else:
                logger.warning(f" Deleting link: {src} ==> {dst}")
            shutil.rmtree(dst, ignore_errors=True)
            if is_delete:
                shutil.rmtree(src, ignore_errors=True)
        else:
            logger.warning(f"{dst} is not a link")


def link():
    typer.run(create_link)


def unlink():
    typer.run(delete_link)
