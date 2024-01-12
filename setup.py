from setuptools import find_namespace_packages, setup

requires = [
    'mako',
    'ruamel.yaml>=0.17.21',
]

setup(
    name='mlx.xunit2rst',
    use_scm_version={
        'write_to': 'mlx/xunit2rst/__version__.py'
    },
    url='https://github.com/melexis/xunit2rst',
    license='Apache License Version 2.0',
    author='JasperCraeghs',
    author_email='jce@melexis.com',
    description='Python script for converting xUnit/JUnit XML format to reStructuredText (.rst) with traceable items',
    long_description=open("README.rst").read(),
    long_description_content_type='text/x-rst',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_namespace_packages(where='.'),
    package_dir={"": "."},
    package_data={
        'mlx.xunit2rst': ['*.mako'],
        'mlx.xunit2rst.assets': ['*.css']
    },
    include_package_data=True,
    install_requires=requires,
    python_requires='>=3.8',
    keywords=['xUnit', 'JUnit', 'XML', 'reStructuredText', 'sphinx', 'rst', 'testing', 'traceability', 'documentation'],
    entry_points={
        'console_scripts': [
            'mlx.xunit2rst = mlx.xunit2rst.xunit2rst:main',
            'xunit2rst = mlx.xunit2rst.xunit2rst:main',
        ]
    },
)
