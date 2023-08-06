from setuptools import setup


__project__ = "cin_term3"
__version__ = "0.0.3"
__description__ = "In this version of cin_term, you can do many things, check the commands and syntax in github.com/RgTheGreat/cin_term"
__packages__ = ["cin_term3"]
__author__ = "Rigved Aneesh"
__author_email__ = "rigved.bob@gmail.com"
__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3",
]
__keywords__ = ["cin_term3", "terminal"]
__scripts__ = ["bin/cin_term3"]
setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email = __author_email__,
    classifiers = __classifiers__,
    keywords = __keywords__,
    scripts = __scripts__
)


