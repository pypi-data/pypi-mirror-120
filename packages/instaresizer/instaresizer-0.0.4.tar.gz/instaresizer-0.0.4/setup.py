import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="instaresizer",
    version="0.0.4",
    author="Roshan Thomas",
    author_email="roshan@secvibe.com",
    description="Returns a PIL Image object of instagram compatible aspect ratio when supplied with an image URL or an image object.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/roshanpty/instaresizer",
    project_urls={
        "Bug Tracker": "https://github.com/roshanpty/instaresizer",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
          'Pillow',
          'requests',
          'python-resize-image'
      ],
    python_requires=">=3.6",
)