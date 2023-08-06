from setuptools import setup
__project__ = "collatzconj"
__version__ = "0.0.1"
__description__ = "collatz conjecture calculation tool"
__packages__ = ["collatzconj"]
__classifiers__ = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Math',
    'Programming Language :: Python :: 3',
    ]
setup(
        name =__project__,
        version = __version__,
        description = __description__,
        packages = __packages__,
        classifiers = __classifiers__,
)