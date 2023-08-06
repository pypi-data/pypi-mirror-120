from setuptools import setup, find_packages

# with open("requirements.txt", "r") as f:
#     requirements = f.read().splitlines()

setup(
    name="fuego",
    version='0.0.4',
    author="Nathan Raw",
    author_email="naterawdata@gmail.com",
    description="Tools for running experiments in the cloud",
    license="MIT",
    install_requires=['sagemaker>=2.59.1', 'huggingface_hub>=0.0.17', 'typer>=0.3.2'],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['fuego=fuego.cli:app'],
    }
)