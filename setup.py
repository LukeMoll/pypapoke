from distutils.core import setup

setup(
    name="pypapoke",
    version="1.0",
    description="Switch PulseAudio sinks with a USB keyboard",
    author="Luke Moll",
    url="https://github.com/lukemoll/pypapoke",
    packages=["pypapoke"],
    install_requires=["evdev"],
    python_requires=">3.6", # for fstrings
    entry_points={
        "console_scripts":["pypapoke=pypapoke.main:main"]
    }
)