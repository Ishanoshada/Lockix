from setuptools import setup, find_packages

setup(
    name="lockix",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "cryptography",
    ],
    entry_points={
        'console_scripts': [
            'lockix=lockix.cli:main',
        ],
    },
    author="Ishan Oshada",
    author_email="ishan.kodithuwakku.official@gmail.com",
    description="A secure file encryption and decryption tool",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ishanoshada/Lockix",
    keywords="encryption, security, files, cryptography",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)