import importlib.util
import os

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py as _build_py

# Read package meta-data from version.py
# see https://packaging.python.org/guides/single-sourcing-package-version/
pkg_dir = os.path.dirname(os.path.abspath(__file__))
version_path = os.path.join(pkg_dir, "dvclive", "version.py")
spec = importlib.util.spec_from_file_location("dvclive.version", version_path)
dvclive_version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dvclive_version)
version = dvclive_version.__version__


# To achieve consistency between the build version and the one provided
# by your package during runtime, you need to **pin** the build version.
#
# This custom class will replace the version.py module with a **static**
# `__version__` that your package can read at runtime, assuring consistency.
#
# References:
#   - https://docs.python.org/3.7/distutils/extending.html
#   - https://github.com/python/mypy
class build_py(_build_py):
    def pin_version(self):
        path = os.path.join(self.build_lib, "dvclive")
        self.mkpath(path)
        with open(os.path.join(path, "version.py"), "w") as fobj:
            fobj.write("# AUTOGENERATED at build time by setup.py\n")
            fobj.write('__version__ = "{}"\n'.format(version))

    def run(self):
        self.execute(self.pin_version, ())
        _build_py.run(self)


image = ["pillow"]
plots = ["scikit-learn"]
mmcv = ["mmcv"]
tf = ["tensorflow"]
xgb = ["xgboost"]
lgbm = ["lightgbm"]
hugginface = ["transformers", "datasets"]
catalyst = ["catalyst<=21.12"]
fastai = ["fastai"]
pl = ["pytorch_lightning"]

all_libs = mmcv + tf + xgb + lgbm + hugginface + catalyst + fastai + pl + plots

tests_requires = [
    "pylint==2.5.3",
    "pytest>=6.0.1",
    "pre-commit",
    "pylint-plugin-utils>=0.6",
    "pytest-cov>=2.12.1",
    "pytest-mock>=3.6.1",
    "pandas>=1.3.1",
    "funcy>=1.14",
    "dvc>=2.0.0",
] + all_libs

setup(
    name="dvclive",
    version=version,
    author="Paweł Redzyński",
    author_email="pawel@iterative.ai",
    packages=find_packages(exclude="tests"),
    description="Metric logger for ML projects.",
    long_description=open("README.rst", "r", encoding="UTF-8").read(),
    extras_require={
        "tests": tests_requires,
        "all": all_libs,
        "tf": tf,
        "xgb": xgb,
        "lgbm": lgbm,
        "mmcv": mmcv,
        "huggingface": hugginface,
        "catalyst": catalyst,
        "fastai": fastai,
        "pytorch_lightning": pl,
        "sklearn": plots,
        "image": image,
        "plots": plots,
    },
    keywords="data-science metrics machine-learning developer-tools ai",
    python_requires=">=3.6",
    cmdclass={"build_py": build_py},
    url="https://dvc.org/doc/dvclive",
    download_url="https://github.com/iterative/dvclive",
)
