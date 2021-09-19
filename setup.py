from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'SAT-based Circuit Local Improvement'
LONG_DESCRIPTION = 'SAT-based Circuit Local Improvement'

setup(
    name="circuit_improvement",
    version=VERSION,
    author="Alexander S. Kulikov, Slezkin Nikita",
    author_email="alexander.s.kulikov@gmail.com, ne.slezkin@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'circuits', 'algorithms', 'complexity theory', 'SAT', 'SAT-solvers', 'heuristics'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
