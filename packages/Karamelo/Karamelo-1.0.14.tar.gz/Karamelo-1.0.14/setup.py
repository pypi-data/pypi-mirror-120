from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Karamelo',
  version='1.0.14',
  description='Selection menus without asking for a string input',
  long_description="This tool helps you easily create a selection menu that doesn't require the user to manually type in the option they want to choose",
  url='https://github.com/Kylyby/karamelo_dialog',  
  author='Kylyby',
  license='GNU GPLv3', 
  classifiers=classifiers,
  keywords='dialog', 
  packages=find_packages(),
  install_requires=['curtsies'] 
)
