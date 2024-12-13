from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")


from credlawn import __version__ as version

setup(
    name="credlawn",
    version=version,
    description="A platform designed to simplify and streamline processes",
    author="Arun Singh",
    author_email="info@credlawn.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)