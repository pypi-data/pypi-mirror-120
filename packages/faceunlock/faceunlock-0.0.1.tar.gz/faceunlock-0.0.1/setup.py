import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="faceunlock", #
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version="0.0.1",
    license='MIT',
    author="Ray&Happy",
    author_email="wdnmd@114514.com",
    description="ranking metrics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/happy_is_i",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        ],
    keywords=['pypi', 'Ray', 'Happy', 'opencv'],
    install_requires=[
        'numpy',
        'opencv-python',
        'opencv-contrib-python',
        'pillow'
    ],
)
