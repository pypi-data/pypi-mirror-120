try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


import os

readme = "README.md"
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, readme)
if os.path.exists(readme_path):
    with open(readme_path, "rb") as stream:
        readme = stream.read().decode("utf8")

setup(
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://mcaapi.readthedocs.io',
    name="mcaapi",
    version="0.1.1",
    description="A Python wrapper for the Maricopa County Assessor API.",
    python_requires="==3.*",
    project_urls={"repository": "https://github.com/foxbatcs/mcaapi"},
    author="foxbatcs",
    author_email="fbcs@foxbatcs.com",
    license="MIT",
    packages=[
        "mcaapi",
        "mcaapi.datasets"
    ],
    package_dir={"": "."},
    package_data={
        'mcaapi': ['mcaapi/datasets/*.csv']
    },
    install_requires= find_packages(),
    extras_require={
        "dev": [
            "wheel==0.*,>=0.30.0"
        ],
    },
)
