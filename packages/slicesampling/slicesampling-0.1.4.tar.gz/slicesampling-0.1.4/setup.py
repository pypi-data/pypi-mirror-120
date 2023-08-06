from setuptools import setup

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

exec(open('slicesampling/version.py').read())

setup(name='slicesampling',
      version=__version__,
      description='Set of Markov chain Monte Carlo (MCMC) sampling methods based on slice_sampler sampling',
      url='https://code.ornl.gov/2kv/slicesampling',
      author='Kris Villez',
      author_email='villezk@ornl.gov',
      install_requires=['numpy', 'scipy'],
      license='MIT',
      packages=['slicesampling'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)