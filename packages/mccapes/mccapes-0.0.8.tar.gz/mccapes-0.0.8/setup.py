from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mccapes',
  version='0.0.8',
  description='simple minecraft cape viewer! view other players cape',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Overnice.exe',
  author_email='silkepilon2009@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  packages=find_packages(),
  install_requires=['requests'] 
)
