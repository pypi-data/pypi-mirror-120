from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name='trie-global',
    version='1.0.0',
    description='A Python Package that allows a user to change or view a global trie.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/thequickbrownfoxjumpedoverthelazydog/trie-global-state-cli',
    author='c25kenneth', 
    licesnse='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages = find_packages(),
    install_package_data = True, 
    install_requires=['requests==2.25.1', 'typer==0.4.0'],
    entry_points={
        'console_scripts' : [
            'global-trie-cli=code.cli:typerApp',
        ]
    },
)