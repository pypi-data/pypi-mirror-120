# This file is placed in the Public Domain.

from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name="botd",
    version="64",
    url="https://github.com/bthate/botd",
    author="Bart Thate",
    author_email="bthate67@gmail.com",
    description="24/7 channel daemon",
    long_description=read(),
    license="Public Domain",
    packages=["bot"],
    zip_safe=True,
    include_package_data=True,
    data_files=[('share/doc/botd', [
                                    'files/bot.1.md',
                                    'files/botcmd.8.md',
                                    'files/botctl.8.md',
                                    'files/botd.8.md'
                                   ]),
                ("etc/rc.d/", ["files/botd"]),
                ("lib/systemd/system", ["files/botd.service"]),
                ("man/man1", ["files/bot.1.gz"]),
                ("man/man8", ["files/botctl.8.gz", "files/botcmd.8.gz", "files/botd.8.gz"])],
    scripts=["bin/bot", "bin/botcmd", "bin/botctl", "bin/botd"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Utilities",
    ]
)
