import setuptools

setuptools.setup(
    name="py-code",
    version="0.0.3",
    description="Script to generate boilerplate code",
    author="Anh Tong",
    author_email="somebody@somewhere.com",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "pycode = src.main:main",
        ]
    },
)
