from setuptools import find_packages, setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "geodesic_dome.md").read_text()
setup(
    name='geodesicDome',
    packages=find_packages(include=['geodesicDome']),
    version='2.0.1',
    long_description = README,
    long_description_content_type="text/markdown",
    install_requires=["numpy", "numba"],
    description='Geodesic Dome',
    author='Sam, Lewis, James, Kevin, Jacob, Manan',
    license='MIT',
)