# ======================================================================================================================
# EposCMD64.dll is needed, thus, try to copy it
# ======================================================================================================================
import os
import pathlib
import shutil



def copyEposDLL(epos_dll="./EposCMD64.dll", logger=None):
    if logger is None:
        logger = print
    else:
        logger = logger.info

    dll_dir = pathlib.Path(epos_dll)
    dll_name = os.path.basename(epos_dll)
    #epos_dll_name = pathlib.Path(epos_dll_name)
    logger(f"Copying {dll_dir} to {os.getcwd()}")

    if not dll_dir.exists():
         raise FileNotFoundError(f"Could not find {epos_dll}")

    dll_dir = str(dll_dir.resolve())
    dll_dest = f"{os.getcwd()}/{dll_name}"  # Copy the file to the workspace folder
    # Copy the file "EposCMD64.dll" to the current dir
    if not pathlib.Path(dll_dest).exists():
        shutil.copyfile(dll_dir, f"{os.getcwd()}/EposCMD64.dll")
        logger(f"Copied {dll_name} to {os.getcwd()}")
    elif pathlib.Path(dll_dest).exists():
        logger(f"{dll_name} already exists in {os.getcwd()}")


    # Check if the file was copied
    if not pathlib.Path(dll_dest).exists():
        raise FileNotFoundError(f"Could not copy {dll_name} to {os.getcwd()}")

def check_if_git_or_pip():
    # check if a folder .git is present ../../
    git_dir = pathlib.Path(__file__).parent.parent.parent / ".git"
    if git_dir.exists():
        print("git_dir:", git_dir)
    else:
        print("git_dir does not exist")

def get_pyprojecttoml() -> pathlib.Path:
    # is found in ../../pyconfig.toml
    pytoml_via_git = pathlib.Path(__file__).parent.parent.parent / "pyproject.toml"
    # found in ./pyconfig.toml: Copied to the root dir
    pytoml_via_pip = pathlib.Path(__file__).parent / "pyproject.toml"

    if pytoml_via_git.exists():
        #print("pytoml_via_git:", pytoml_via_git)
        return pytoml_via_git.resolve().absolute()
    elif pytoml_via_pip.exists():
        #print("pytoml_via_pip:", pytoml_via_pip)
        return pytoml_via_pip.resolve().absolute()

