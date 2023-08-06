from setuptools import setup, Extension, find_packages

import sys
import platform
import subprocess

if sys.version_info[0] == 3 and sys.version_info[1] == 6:
    subprocess.run(
        ["python", "hub_shm/py36_clinic.py", "hub_shm/posixshmem.c"]
    )
elif sys.version_info[0] == 3 and sys.version_info[1] == 7:
    subprocess.run(
        ["python", "hub_shm/py37_clinic.py", "hub_shm/posixshmem.c"]
    )
else:
    raise ValueError("Must run on Python 3.6 or 3.7")


linux_module = Extension(
    "hub_shm/_posixshmem",
    define_macros=[
        ("HAVE_SHM_OPEN", "1"),
        ("HAVE_SHM_UNLINK", "1"),
        ("HAVE_SHM_MMAN_H", 1),
    ],
    libraries=["rt"],
    sources=["hub_shm/posixshmem.c"],
)


darwin_module = Extension(
    "hub_shm/_posixshmem",
    define_macros=[
        ("HAVE_SHM_OPEN", "1"),
        ("HAVE_SHM_UNLINK", "1"),
        ("HAVE_SHM_MMAN_H", 1),
    ],
    sources=["hub_shm/posixshmem.c"],
)


setup(
    name="hub_shm",
    version="1.0.0",
    description="Hub Shared Memory",
    author="activeloop.ai",
    author_email="abhinav@activeloop.ai",
    url="https://www.activeloop.ai",
    download_url="https://github.com/activeloopai/hub_shm/archive/refs/tags/1.0.0.tar.gz",
    py_modules=["hub_shm"],
    packages=find_packages(),
    ext_modules=[linux_module]
    if platform.system() == "Linux"
    else [darwin_module]
    if platform.system() == "Darwin"
    else [],
)
