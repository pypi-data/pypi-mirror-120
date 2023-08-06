from distutils.core import setup
setup(
  name = 'PyByteReader',
  packages = ['PyByteReader'],
  version = '0.2',     
  license='MIT',   
  description = 'Provides utilities to read bytes from an open binary file (big endian is assumed)',
  author = 'Matthew Kirkley',
  author_email = 'matt.kirkley@gmail.com',
  url = 'https://github.com/ventralnet/PyByteReader',
  download_url = 'https://github.com/ventralnet/PyByteReader/archive/refs/tags/v_02.tar.gz',
  keywords = ['BINARY', 'BYTES', 'FILE', 'FILE UTILITIES', 'FILE UTIL', 'FILE', 'FILE UTILS'],
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

