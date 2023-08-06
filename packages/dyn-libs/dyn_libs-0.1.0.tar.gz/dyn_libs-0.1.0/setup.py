import os

from setuptools import setup
# import setuptools

# cython detection
try:
    from Cython.Build import cythonize

    CYTHON = False
except ImportError:
    CYTHON = False

SOURCE_PATH = './mobio'

ext_modules = []


# if CYTHON:
#     ext_modules = cythonize([SOURCE_PATH + "/**/*.py"], compiler_directives=dict(always_allow_keywords=True))


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


# extra_files = package_files('mobio/profiling')

# setup(
#     name='dynamic_field',
#     version='0.1',
#     scripts=['dynamic_field'],
#     author='MOBIO',
#     author_email='contact@mobio.vn',
#     description='Mobio Dynamic Fields',
#     long_description_content_type="text/markdown",
#     url='https://github.com/mobiovn',
#     # packages=setuptools.find_packages(),
#     classifiers=[
#         "Topic :: Software Development",
#         "Development Status :: 4 - Beta",
#         "Intended Audience :: Developers",
#         "License :: OSI Approved :: MIT License",
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.4",
#         "Programming Language :: Python :: 3.5",
#         "Programming Language :: Python :: 3.6",
#         "Programming Language :: Python :: 3.7",
#         "Programming Language :: Python :: Implementation :: CPython",
#         "Programming Language :: Python :: Implementation :: PyPy",
#     ],
#
# )

setup(name='dyn_libs',
      version='0.1.0',
      description='Mobio Dynamic Fields',
      url='https://github.com/mobiovn',
      author='MOBIO',
      author_email='contact@mobio.vn',
      license='MIT',
      packages=['mobio/libs/dyn', 'mobio/libs/dyn/common',
                'mobio/libs/dyn/controllers', 'mobio/libs/dyn/filters',
                'mobio/libs/dyn/helpers', 'mobio/libs/dyn/models',
                'mobio/libs/dyn/models/mongo'],
      install_requires=['m-singleton', 'pymongo', 'Flask', 'flask_cors', 'requests', 'unidecode', 'elasticsearch>=5.0.0,<6.0.0'],
      # package_data={'': extra_files},
      include_package_data=True,
      ext_modules=ext_modules,
      classifiers=[
          "Topic :: Software Development",
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
      ]
      )
