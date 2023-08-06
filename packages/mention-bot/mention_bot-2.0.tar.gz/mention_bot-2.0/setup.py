from distutils.core import setup
setup(
  name = 'mention_bot',
  packages = ['mention_bot'],
  version = '2.0',
  license='MIT',
  description = 'A generic infrastructure to create a Twitter bot that acts on mentions of it',
  author = 'Yuval Garti',
  author_email = 'yuvalgarti@gmail.comm',
  url = 'https://github.com/yuvalgarti/generic-mention-bot',
  download_url = 'https://github.com/yuvalgarti/generic-mention-bot/archive/refs/tags/v2.0.tar.gz',
  keywords = ['Twitter', 'Bot'],
  install_requires=[            # I get to this in a second
        'tweepy'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.9',
  ],
)