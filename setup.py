from setuptools import setup, find_packages

import password

with open("README.md", "r") as readme_file:
    readme = readme_file.read()
    
requirements = ['PyQt', 'sqlite3', 'werkzeug']

setup(
      name="password",
      version=password.__version__,
      author="Daniel Gallagher",
      author_email="daniel-gallagher@outlook.com",
      description="Password",
      long_description=readme,
      long_description_content_type="text/markdown",
      url="https://github.com/danielgallagher8/password.git",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requirements,
      classifiers=[
              "Programming Language :: Python :: 3.7",
              "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
              ],
      )
