
from distutils.core import setup
setup(
  name = 'phyphoxBLE',         # How you named your package folder (MyLib)
  packages = ['phyphoxBLE'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The purpose of this library is to use the phyphox app (see www.phyphox.org) to plot sensor data on your phone with the open source app phyphox. In the other direction you can also use this library to access sensor data from your phone to use in your ESP32 project with Micropython.',   # Give a short description about your library
  author = 'YOUR NAME',                   # Type in your name
  author_email = 'your.email@domain.com',      # Type in your E-Mail
  url = 'https://github.com/Marcelhag/phyphoxBLE',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Marcelhag/phyphoxBLE/archive/refs/tags/v_01.tar.gz',    # I explain this later on
  keywords = ['PHYPHOX', 'BLE', 'PHYPHOXBLE', 'RWTH'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)