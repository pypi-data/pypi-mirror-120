from setuptools import setup

setup(
    name="thundra-foresight-inst-helpers",
    version="0.1.0",
    description="A collection of instrumentation methods for Thundra Foresight",
    url="https://github.com/thundra-io/thundra-foresight-inst-helpers",
    author="Oguzhan Ozdemir",
    author_email="oguzhan.ozdemir@thundra.io",
    license="MIT",
    package_dir={"": "src"},
    packages=[
        "thundra_foresight_inst_helpers",
        "thundra_foresight_inst_helpers.utils",
        "thundra_foresight_inst_helpers.maven",
    ],
    install_requires=["urllib3"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
