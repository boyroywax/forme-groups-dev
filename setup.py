from setuptools import setup, find_packages

setup(
    name='groups',
    version='0.0.1',
    packages=find_packages('src', exclude=['*tests*']),
    package_dir={'': 'src'},
    install_requires=[
        'uuid'
    ],
    entry_points={
        'console_scripts': [
            'groups=groups.cli:main'
        ]
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A package for grouping decentralizzed data',
    license='MIT',
    keywords='grouping data',
    url='https://github.com/boyroywax/forme-groups-dev',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)
