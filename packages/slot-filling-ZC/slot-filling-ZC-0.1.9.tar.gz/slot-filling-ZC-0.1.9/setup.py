import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="slot-filling-ZC",
    version="0.1.9",
    author="Zichu",
    author_email="zichuu@gwu.edu",
    description="train(train_file,test_file,vocab_intent_file,vocab_slot_file)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(include=['slot_ZC','slot_ZC.*']),
    package_data={'slot_ZC': ['config.json']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)