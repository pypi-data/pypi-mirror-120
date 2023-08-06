import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
project_name = "percetron_pypi"
user_name = 'sandeepjena7'

setuptools.setup(
    name=f"{project_name}-{user_name}",
    version="0.0.3",
    author=user_name,
    author_email="sandeepjena777@gmail.com",
    description="Its a implementation of percetron",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{user_name}/{project_name}",
    project_urls={
        "Bug Tracker": f"https://github.com/{user_name}/{project_name}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "tqdm",
        "matplotlib",
        "pandas",
        "joblib",

    ]
)