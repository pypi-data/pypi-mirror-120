from setuptools import setup, find_packages

NAME = 'mdo_outlier_detector'
DESCRIPTION = """
            Detection of outlier with mahanalobis distance 
            which have access of the parameters (means and precision matrice) with algo GMM or Bayesian GMM provide by sklearn
            """
URL = "https://github.com/JonathanNdambaPro/MDO"
EMAIL = "jonathan.ndamba.pro@gmail.com"
AUTHOR = "JonathanNdambaPro"
REQUIRES_PYTHON = ">=3.6.0"

def list_reqs(fname="requirements.txt"):
    with open(fname) as fd:
        return fd.read().splitlines()

about = {}
with open("VERSION") as f:
    _version = f.read().strip()
    about["__version__"] = _version

setup(
    name=NAME,
    version=about["__version__"],
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    description=DESCRIPTION,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(),
    install_requires=list_reqs(),
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)



