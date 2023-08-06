import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="abcd_yt98",
    version="1.0.0",
    author="tongye",
    author_email="791161009@qq.com",
    description="test install requires",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://blog.xiaoqying.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["numpy","matplotlib"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
