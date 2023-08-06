import pathlib
from setuptools import setup, find_packages
import dxy

requirements = [
    'jupyter',
    'numpy',
    'matplotlib',
    'requests',
    'pandas'
]
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dxy",
    version=dxy.__version__,
    python_requires='>=3.5',
    description="It summarizes some data science functions",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/wwwxqq/dxy",
    author="Xueyuan Du",
    author_email="aaa@aaa.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=True,
    # entry_points={
    #     "console_scripts": [
    #         "dxy=dxy.__main__:main",
    #     ]
    # },
)