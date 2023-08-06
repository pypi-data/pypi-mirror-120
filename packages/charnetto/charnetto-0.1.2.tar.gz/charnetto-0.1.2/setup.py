from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="charnetto",
    version="0.1.2",
    packages=find_packages(),
    
    author="Coline Métrailler",
    author_email="coline.metrailler@unil.ch",
    license="MIT",
    
    url="https://gitlab.com/maned_wolf/charnetto",
    project_urls = {
        "Documentation": "https://charnetto.readthedocs.io/en/latest/",
        "Tracker": "https://gitlab.com/maned_wolf/charnetto/-/issues",
    },
    
    description="automated character networks for books and movie scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    install_requires=[
        "tqdm>=1.0",
        "networkx>=2.5",
        "numpy>=1.19.2",
        "pandas>=1.0.5",
    ],

    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
    ],
)
