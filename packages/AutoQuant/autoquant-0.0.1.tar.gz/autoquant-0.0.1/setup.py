import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoquant",
    version="0.0.1",
    author='Marcnuth',
    author_email='hxianxian@gmail.com',
    description="Auto Quant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Marcnuth/AutoQuant",
    project_urls={
        "Bug Tracker": "https://github.com/Marcnuth/AutoQuant/issues",
    },
    classifiers=[
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3'
    ],
    package_dir={"": "autoquant"},
    packages=setuptools.find_packages(where="autoquant"),
    python_requires=">=3.6",
)