from setuptools import setup, find_packages

setup(name="cudistutils",
      author="Thejaswi Rao",
      author_email="rao.thejaswi@gmail.com",
      description="Support for building cuda+cython extension modules",
      install_requires=["Cython"],
      license="https://github.com/rmcgibbo/npcuda-example/blob/master/LICENSE",
      keywords="setuptools cuda gpus nvidia",
      version="0.1",
      packages=find_packages())
