import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mumuzi",
    version="0.1.3",
    author="mumuzi_fans",
    author_email="mumuzi@mumuzi.mumuzi",
    description="ctf全栈全自动解题姬mumuzi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://blog.csdn.net/qq_42880719/",
    project_urls={
        "Bug Tracker": "https://blog.csdn.net/qq_42880719/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "mumuzi"},
    packages=setuptools.find_packages(where="mumuzi"),
    python_requires=">=3.6",
)