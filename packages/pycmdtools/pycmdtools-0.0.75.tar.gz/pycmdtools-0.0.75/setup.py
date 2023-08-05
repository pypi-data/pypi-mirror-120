import setuptools


def get_readme():
    with open('README.rst') as f:
        return f.read()


setuptools.setup(
    # the first three fields are a must according to the documentation
    name="pycmdtools",
    version="0.0.75",
    packages=[
        'pycmdtools',
    ],
    # from here all is optional
    description="pycmdtools is set of useful command line tools written in python",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Mark Veltzer",
    author_email="mark.veltzer@gmail.com",
    maintainer="Mark Veltzer",
    maintainer_email="mark.veltzer@gmail.com",
    keywords=[
        'utils',
        'command line',
        'python',
        'shell',
        'utilities',
    ],
    url="https://veltzer.github.io/pycmdtools",
    download_url="https://github.com/veltzer/pycmdtools",
    license="MIT",
    platforms=[
        'python3',
    ],
    install_requires=[
        'pylogconf',
        'pytconf',
        'requests',
        'tqdm',
        'numpy',
        'pandas',
        'unidecode',
        'pyyaml',
        'jsonschema',
        'pytidylib',
        'beautifulsoup4',
        'lxml',
    ],
    extras_require={
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    data_files=[
    ],
    entry_points={"console_scripts": [
        'pycmdtools=pycmdtools.main:main',
    ]},
    python_requires=">=3.7",
)
