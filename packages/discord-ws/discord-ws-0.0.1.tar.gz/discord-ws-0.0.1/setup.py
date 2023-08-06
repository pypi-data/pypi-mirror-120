from setuptools import setup

packages = [
    'discordws'
]

requires = [
    "websockets",
    "altflags"
]

setup(
    name="discord-ws",
    version="0.0.1",
    packages=packages,
    install_requires=requires,
    python_requires='>=3.8.0',
)