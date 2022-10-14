import os

from setuptools import setup
from distutils.core import Extension
from distutils.sysconfig import customize_compiler
from Cython.Build import build_ext
import glob

# module = Extension("crypto_market_making", ["crypto_market_making/**/*.pyx"])
def collect_extensions():
    kwargs = {"language": "c++"}
    extensions = []
    crypto_market_making_dir = glob.glob(
        "crypto_market_making/**/*.pyx", recursive=True
    )

    for file in crypto_market_making_dir:
        file_list = file.split("\\")
        module_name = file_list[-1].replace(".pyx", "")
        directory = "\\".join(file_list[:-1])
        extensions.append(
            Extension(
                module_name,
                sources=[file],
                include_dirs=[directory, "."],
                build_dir=directory,
                **kwargs
            )
        )

    return extensions


class crypto_mm_build_ext(build_ext):
    """
    Custom build command to allow for any dlls to be included in future
    """

    def build_extensions(self):
        customize_compiler(self)

        try:
            self.compiler.compiler_so.remove("-Wstrict-prototypes")
        except (AttributeError, ValueError):
            pass

        build_ext.build_extensions(self)


setup(
    name="crypto_market_making",
    version="0.1",
    author="Caleb Migosi",
    ext_modules=collect_extensions(),
    setup_requires=["Cython"],
    cmdclass={"build_ext": build_ext},
    compiler_directives={"language_level": "3"},
)
