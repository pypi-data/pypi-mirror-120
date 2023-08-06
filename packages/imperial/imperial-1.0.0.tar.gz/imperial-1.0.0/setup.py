from setuptools import setup

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="imperial",
    version="1.0.0",
    url="https://github.com/imperialbin/imperial.py",
    author="Hexiro",
    description="A mirror package for imperial.py. Please install that instead.",
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=[],
    install_requires=["imperial.py"],
    zip_safe=True
)
