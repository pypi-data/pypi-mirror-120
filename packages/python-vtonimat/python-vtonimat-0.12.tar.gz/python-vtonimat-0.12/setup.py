import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

NAME = 'python-vtonimat'
VERSION = '0.12'

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

srcdir = 'convert_imaterialist'

for dirpath, dirnames, filenames in os.walk(srcdir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[(len(srcdir) + 1):]  # Strip "$srcdir/" or "$srcdir\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))


try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
    long_description = f.read().strip()
    f.close()
except:
    long_description = ''

setup(name=NAME,
      version=VERSION,
      description='Simple VTON and Imaterialist data parser written in pure Python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Arti.B',
      install_requires=['numpy>=1.19.5'],
      author_email=' ',
      license='BSD',
      url='https://github.com/aarti-b/vton-imaterialist',
      package_dir={'vtonimat': 'vtonimat'},
      packages=packages,
      package_data={'vtonimat': data_files},
      classifiers=[
          'Intended Audience :: Science/Research',
          'Operating System :: MacOS',
          'Programming Language :: Python :: 3.7'],
      )
