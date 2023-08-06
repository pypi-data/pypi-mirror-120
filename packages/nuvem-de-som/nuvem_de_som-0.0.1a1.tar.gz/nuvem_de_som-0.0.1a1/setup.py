from setuptools import setup

setup(
    name="nuvem_de_som",
    version="0.0.1a1",
    description="search soundcloud",
    license="",
    author="JarbasAi",
    url="https://github.com/OpenJarbas/nuvem_de_som",
    packages=["nuvem_de_som"],
    install_requires=[
        "bs4", "youtube-dl", "requests"
    ]
)
