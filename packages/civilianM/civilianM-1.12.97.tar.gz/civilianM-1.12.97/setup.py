import setuptools

with open("README.md", "r",encoding="UTF-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="civilianM",
  version="1.12.97",
  author="AC",
  author_email="ehcemc@163.com",
  description="Common functions,More will be added in the future",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
