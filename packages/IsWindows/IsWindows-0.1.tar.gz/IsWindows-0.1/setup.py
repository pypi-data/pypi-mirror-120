from distutils.core import setup
setup(
  name = 'IsWindows',
  packages = ['IsWindows'],
  version = '0.1',     
  license='MIT',   
  description = 'Provides IsWindows function returning true if windows os, false otherwise',
  author = 'Matthew Kirkley',
  author_email = 'matt.kirkley@gmail.com',
  url = 'https://github.com/ventralnet/IsWindows',
  download_url = 'https://github.com/ventralnet/IsWindows/archive/refs/tags/v_01.tar.gz',
  keywords = ['OS', 'WINDOWS', 'IS WINDOWS', 'OS detection'],
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)

