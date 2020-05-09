from setuptools import setup


setup(
    name="compounds-research",
    install_requires=[
        "pandas",
        "matplotlib",
        "seaborn",
        "statsmodels",
        "web3",
    ],
    extras_require={
        "dev": [
            "jupyter",
            "pylint",
        ]
    }
)
