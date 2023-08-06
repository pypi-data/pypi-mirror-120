import setuptools

setuptools.setup(
    name="ptinsearcher",
    description="Web sources information extractor",
    version="0.0.1",
    url="https://www.penterep.com/",
    author="Penterep",
    author_email="info@penterep.com",
    license="GPLv3+",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Environment :: Console"
    ],
    python_requires = '>=3.6',
    install_requires=["ptlibs", "requests", "bs4", "lxml", "tldextract", "pyexiftool"],
    entry_points = {'console_scripts': ['ptinsearcher = ptinsearcher.ptinsearcher:main']},
    include_package_data= True
)