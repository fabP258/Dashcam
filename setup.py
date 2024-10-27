from setuptools import setup, find_packages

setup(name="recorder", version="0.0.1", description="Data recording application",author="Fabio Petzenhauser", author_email="fabio894@gmail.com", packages=find_packages(where="src"), package_dir={"": "src"}, install_requires=[], python_requires=">=3.10")