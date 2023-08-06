import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yolov5_inference",
    version="0.8",
    author="cuongngm",
    author_email="cuonghip0908@gmail.com",
    description="code de inference yolov5",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ultralytics/yolov5",
    packages=setuptools.find_packages(),
    install_requires=[
        'matplotlib',
        'seaborn'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)