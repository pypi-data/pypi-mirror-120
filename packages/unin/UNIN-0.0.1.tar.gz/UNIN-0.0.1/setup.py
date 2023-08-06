from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: Apache Software License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='UNIN',
  version='0.0.1',
  description='Data manipulation package.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(), 
  author='David Kundih',
  author_email='kundihdavid@gmail.com',
  url='http://www.davidkundih.iz.hr',
  license='Apache Software License', 
  classifiers=classifiers,
  keywords='data science, machine learning, artificial intelligence, AI, alunari, alunariTools',
  packages=find_packages(),
  install_requires=['alunari', 'alunariTools'] 
)