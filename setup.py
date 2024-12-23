from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        name="ipc_pyx",
        sources=[
            "src/recorder/mw/msgq/ipc.cc",
            "src/recorder/mw/msgq/ipc_pyx.pyx",
            "src/recorder/mw/msgq/msgq.cc",
        ],
        language="c++",
        extra_compile_args=["-std=c++11"],
        include_dirs=[],
        libraries=[],
        library_dirs=[],
    )
]

setup(
    name="recorder",
    version="0.1.1",
    description="Data recording application",
    author="Fabio Petzenhauser",
    author_email="fabio894@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    python_requires=">=3.10",
    ext_modules=cythonize(extensions),
    zip_safe=False,
)
