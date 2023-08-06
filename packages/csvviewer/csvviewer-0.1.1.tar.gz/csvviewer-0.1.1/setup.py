from distutils.core import setup
import setuptools

setup(
  name = 'csvviewer',     
  packages = ['csvviewer'],
  version = '0.1.1', 
  license='MIT',  
  description = 'Command Line Delimited Text Viewer',
  author = 'franklinsijo',
  author_email = 'franklinsijo@gmail.com', 
  url = 'https://github.com/franklinsijo/csvviewer', 
  download_url = 'https://github.com/franklinsijo/csvviewer/archive/refs/tags/0.1.0.tar.gz',
  scripts= ['bin/csvviewer'],
  keywords = ['csv', 'command-line', 'reader'], 
  install_requires=[        
          'prettytable',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Natural Language :: English',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
)