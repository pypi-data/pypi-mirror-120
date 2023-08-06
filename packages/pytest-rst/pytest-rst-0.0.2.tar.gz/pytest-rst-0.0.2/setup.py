from setuptools import setup, find_packages


setup(
    name='pytest-rst',
    version='0.0.2',
    author='Dmitry Orlov',
    author_email='me@mosquito.su',
    license='MIT',
    description='Test code from RST documents with pytest',
    long_description=open("README.rst").read(),
    platforms="all",
    classifiers=[
        "Framework :: Pytest",
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=[
        "pytest",
        "py",
        "docutils",
        "pygments",
    ],
    entry_points={
        "pytest11": ["pytest-rst = pytest_rst"]
    },
    url='https://github.com/mosquito/pytest-rst'
)
