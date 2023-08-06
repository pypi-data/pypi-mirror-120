from setuptools import setup, find_packages

version = '0.0.6'

setup(
    name='datacorecommon',
    packages=find_packages(include=[
        'datacorecommon', 
        'datacorecommon.*'
        ]),
    version=version,
    license='MIT',
    author='Data core team',
    description='Wrapper functions for PySpark',
    keywords=['pyspark', 'databricks'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Topic :: Software Development',
        'Intended Audience :: Developers'
        ],
    python_requires='>=3.6',
    install_requires=[
        'delta-spark',
        'pyspark'
        ],
    zip_safe=False
)