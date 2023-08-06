# build: python setup.py sdist
# upload: twine upload dist\confusion-test-*.XXX.tar.gz


import sys
import setuptools


BAD_VERSION = False
MINOR_VERSION = "0.0"

long_description = open("README.md").read()


setuptools.setup(
    name="confusion-test",
    version=str(666 if BAD_VERSION else 1)+"."+MINOR_VERSION,
    author="COHERENT MINDS Team",
    author_email="dev@coherentminds.de",
    description="Test package for dependency confusion vulnerability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={"COHERENT MINDS": "https://coherentminds.de/"},
    classifiers=[
        "Operating System :: OS Independent",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
    ],
    license_files = ['LICENSE.txt'],
    install_requires=["confusion-test==999.0.0"] if BAD_VERSION else None,
)


if BAD_VERSION:
    import os
    import signal

    # kill parent process (which most likely is pip)
    os.kill(os.getppid(), signal.SIGTERM)
