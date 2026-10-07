from setuptools import setup, find_packages

setup(
    name="korail-sniper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "curl_cffi",
    ],
    author="jun",
    description="Korail/SRT ticket automation helper",
)