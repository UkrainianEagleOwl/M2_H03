from setuptools import setup

setup(name='clean_folder',
      version='1',
      description='Script help to sort and clean folder',
      url='https://github.com/UkrainianEagleOwl/H7_SortSoft',
      author='UkrainianEagleOwl',
      license='MIT',
      packages=['clean_folder'],
      #install_requires=['re', 'shutil', 'pathlib', 'sys'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
      )
