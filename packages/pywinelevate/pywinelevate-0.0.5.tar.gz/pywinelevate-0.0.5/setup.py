import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywinelevate",
    version="0.0.5",
    author="Juan José Albán",
    author_email="j.alban@uniandes.edu.co",
    description="a symple python decorator that reloads the script with privileges if neccesary",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ElCuboNegro/win_elevator",
    project_urls={
        "Bug Tracker": "https://github.com/ElCuboNegro/win_elevator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Win32 (MS Windows)",
        "Development Status :: 3 - Alpha"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)