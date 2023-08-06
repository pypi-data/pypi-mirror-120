import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()
	
setuptools.setup(
	name="pybodytrack-serotonin",
	version="0.0.1",
	author="serotonin",
	author_email="ezeq.david0611@gmail.com",
	description="use tools like hand tracking or body tracking with python",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/serotoninx/pytools/pybodytrack",
	project_urls={
        "Bug Tracker": "https://github.com/pytools/pybodytrack/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)