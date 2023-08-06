from setuptools import find_packages, setup
setup(
    name='geodesicDome',
    packages=find_packages(include=['geodesicDome']),
    version='2.0.11',
    
    long_description_content_type="text/markdown",
    install_requires=["numpy", "numba"],
    description='Geodesic Dome',
    author='Sam, Lewis, James, Kevin, Jacob, Manan',
    license='MIT',
    
   
)