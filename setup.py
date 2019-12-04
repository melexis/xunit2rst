from setuptools import setup, find_packages

requires = ['mako']

setup(
    name='mlx.xunit2rst',
    use_scm_version={
        'write_to': 'mlx/__xunit2rst_version__.py'
    },
    setup_requires=['setuptools_scm'],
    url='https://github.com/melexis/xunit2rst',
    license='Apache License Version 2.0',
    author='JasperCraeghs',
    author_email='jce@melexis.com',
    description='Python script for converting xUnit/JUnit XML format to reStructuredText format',
    long_description=open("README.rst").read(),
    long_description_content_type='text/x-rst',
    zip_safe=False,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Environment :: Console',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Packaging',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(exclude=['tests', 'doc']),
    package_data={'mlx.xunit2rst': ['mlx/*.mako']},
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['mlx'],
    keywords=['xUnit', 'JUnit', 'XML', 'reStructuredText', 'sphinx', 'rst', 'testing', 'traceability', 'documentation'],
    entry_points={
        'console_scripts': ['xunit2rst = mlx.xunit2rst.xunit2rst:main']
    },
)
