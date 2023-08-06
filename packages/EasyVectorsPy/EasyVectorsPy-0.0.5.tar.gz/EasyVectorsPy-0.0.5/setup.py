from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="EasyVectorsPy",
    version="0.0.5",
    author="Nellle",
    description="library that helps when working with coordinates like(Pillow, Pygame)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nellle/EasyVectorsPy",
    project_urls={
        "Bug Tracker": "https://github.com/nellle/EasyVectorsPy/issues",
        "Wiki": "https://github.com/nellle/EasyVectorsPy/wiki"
    },
    packages = find_packages(),
    install_requires=[],
    keywords=['python', 'vectors', 'easy', 'easy vectors'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)