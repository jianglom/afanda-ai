#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="afanda-ai",
    version="1.0.0",
    description="阿-凡达 · 凡人AI - 有原则、懂时宜、会成长的AI框架",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Afanda Team",
    author_email="jianglom@gmail.com",
    url="https://github.com/jianglom/afanda-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],
    },
    project_urls={
        "Documentation": "https://github.com/jianglom/afanda-ai/docs",
        "Source": "https://github.com/jianglom/afanda-ai",
        "Tracker": "https://github.com/jianglom/afanda-ai/issues",
    },
)