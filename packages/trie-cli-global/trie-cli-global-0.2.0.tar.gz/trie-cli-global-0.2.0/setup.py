from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    longerDesc = readme_file.read()

setup(
    name='trie-cli-global',
    version='0.2.0',
    author = 'c25kenneth',
    description = 'A CLI that allows a user to update or see a data structure that is hosted globally. ',
    long_description=longerDesc,
    packages=find_packages(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    py_modules = ['trie_global', 'appFolder'],
    python_requires='>=3.9.6',
    install_requires=['click', 'requests'],
    entry_points = {
        'console_scripts': [
            'trie-cli-global=trie_global:main',
        ]
    }
)