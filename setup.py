#!/usr/bin/env python

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(name="aidebate",
          version="0.0.3-SNAPSHOT",
          description="Easily automate a debate between 2 or more AI agents.",
          author="PyU Team",
          author_email="posh.bc@gmail.com",
          install_requires=["langchain", "arxiv", "wikipedia", "duckduckgo-search", "langsmith",
                            "openai", "google-search-results", "langchain-community",
                            "langchain-openai", "pyu>=0.1.3"],
          license="MIT",
          classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
          ],
          url="https://github.com/poshjosh/aidebate",
          packages=find_packages(
              where='src',
              include=['aidebate', 'aidebate.*'],
          ),
          package_dir={"": "src"},
          )
