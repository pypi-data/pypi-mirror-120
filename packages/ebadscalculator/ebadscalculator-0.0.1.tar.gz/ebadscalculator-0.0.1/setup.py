from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ebadscalculator',
  version='0.0.1',
  description='A very basic calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Muhammad Ebaad Ullah Khan',
  author_email='ebadullah371@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=['ebadscalculator'],
  install_requires=[''] 
)