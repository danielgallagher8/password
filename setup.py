from setuptools import setup, find_packages

import password_keeper

with open("README.md", "r") as readme_file:
    readme = readme_file.read()
    
requirements = ['PyQt5', 'werkzeug']

setup(
      name="password_keeper",
      version=password_keeper.__version__,
      author="Daniel Gallagher",
      author_email="daniel-gallagher@outlook.com",
      description="Password Keeper",
      long_description=readme,
      long_description_content_type="text/markdown",
      url="https://github.com/danielgallagher8/password_keeper.git",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requirements,
      classifiers=[
              "Programming Language :: Python :: 3.7",
              "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
              ],
      )
