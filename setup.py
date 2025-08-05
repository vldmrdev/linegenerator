from setuptools import setup, find_packages

setup(
    name="llgen",
    version="0.1.0a3",
    author="Vladimir(vldmrdev)",
    author_email="70532790+vldmrdev@users.noreply.github.com",
    description="CLI tool for generating log lines with customizable templates",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vldmrdev/llgen",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0"
    ],
    entry_points={
        "console_scripts": [
            "llgen=llgen.llgen:main",
        ],
    },
)