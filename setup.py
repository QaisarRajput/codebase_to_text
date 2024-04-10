from setuptools import setup, find_packages

setup(
    name="codebase-to-text",
    version="1.0.1",
    packages=find_packages(),
    install_requires=["python-docx"],
    entry_points={
        "console_scripts": [
            "codebase-to-text = codebase_to_text.codebase_to_text:main",
        ]
    },
    author="Qaisar Tanvir",
    author_email="qaisartanvir.dev@gmail.com",
    description="A Python package to convert codebase to text",
    long_description=open("docs/README.md").read(),
    download_url="https://github.com/QaisarRajput/codebase_to_text/archive/refs/tags/1.0.0.tar.gz",
    long_description_content_type="text/markdown",
    keywords = ["codebase, code conversion, text conversion, folder structure, file contents, text extraction, document conversion, Python package, GitHub repository, command-line tool, code analysis, file parsing, code documentation, formatting preservation, readability"],
    license="MIT",
    url="https://github.com/QaisarRajput/codebase_to_text",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)
