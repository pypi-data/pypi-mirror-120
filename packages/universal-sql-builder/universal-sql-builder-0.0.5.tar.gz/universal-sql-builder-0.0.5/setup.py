import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="universal-sql-builder",                     # This is the name of the package
    version="0.0.5",                        # The initial release version
    author="Shantanu SHarma",                     # Full name of the author
    description="""Create sql query with the help of sql builder magic function help to 
    make automatic sql query its help in build sql query string for Microsoft SQL, MySql, SqlLite,
     PostgreSQL, ORACLE, Apache Hive, Django, FLASK, HBASE and Apache Spark etc. """,
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.0',                # Minimum version requirement of the package
    py_modules=["UniversalSqlBuilder"],             # Name of the python package
    package_dir={'':'universal-sql-builder/src'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)