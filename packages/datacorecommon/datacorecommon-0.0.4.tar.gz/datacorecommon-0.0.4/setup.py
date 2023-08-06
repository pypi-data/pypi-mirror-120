from setuptools import setup, find_packages

version = '0.0.4'

setup(
    name='datacorecommon',
    packages=find_packages(),
    version=version,
    license='MIT',
    author='Data core team',
    description='Wrapper functions for PySpark',
    keywords=['pyspark', 'databricks'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development',
    ],
    python_requires='>=3.6',
    install_requires=['delta'],
    zip_safe=False
)