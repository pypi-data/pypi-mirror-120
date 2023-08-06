import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PythMC", # Replace with the pkg name
    version="1.2.2",
    author="Alexandre Silva // MrKelpy",
    author_email="alexandresilva.coding@gmail.com",
    description="A Library used to interact with the Minecraft Environment in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrKelpy/PythMC",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["mouse", "keyboard"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)