import setuptools
import locapip

name = locapip.__name__
version = locapip.__version__

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=name,
    version=version,
    author="sjtu_6547",
    author_email="88172828@qq.com",
    description="A scene data processing toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://locapidio.com/",
    keywords="ITK VTK OpenCASCADE IGL CGAL USD OpenVDB",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["numpy"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
