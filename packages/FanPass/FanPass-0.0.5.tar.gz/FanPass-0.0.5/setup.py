from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))

setup(
  name = 'FanPass',        
  packages = ['fpass'],   
  version = '0.0.5',    
  license='MIT',     
  description = 'password generator by iFanpS#9347', 
  author = 'iFanpS',                  
  author_email = 'imezz8424@gmail.com',     
  keywords = ['passgen', 'ifanpspassgen'], 
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)