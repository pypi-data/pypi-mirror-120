from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='adoniram',
    version='0.0.3',
    packages=find_packages(where='src'),
    url='https://github.com/sinri/Adoniram',
    license='MIT',
    author='Sinri Edogawa',
    author_email='e.joshua.s.e@gmail.com',
    description='A Server-Client Communication Framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
    ],
    package_dir={"": "src"},
    install_requires=[
        'nehushtan~=0.4.18',
    ]
)
