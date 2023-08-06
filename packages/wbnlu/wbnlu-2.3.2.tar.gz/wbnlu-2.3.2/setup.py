# -*- coding: utf-8 -*-
from setuptools import setup
LONGDOC = """
wbnlu

To be completed

"""

setup(name='wbnlu',
      version='2.3.2',
      description='WB NLU toolkit',
      long_description=LONGDOC,
      packages=['wbnlu'],
      package_dir={'wbnlu':'wbnlu'},
      package_data={'wbnlu':['*.*', 'configs/*', 'extractors/*', 'components/*', 'midlevel/*', 'uplevel/*', 'extractors/time/*', 'resources/*', 'resources/features/*', 'resources/features/emojis/*',
                             'resources/features/entity/*','resources/features/segmentation/*','resources/features/sentiment/*','resources/features/wbtag/*',
                              'resources/features/timex/*',
                             'resources/patterns/*', 'resources/patterns/beauty/*', 'resources/patterns/entity/*', 'resources/patterns/segmentation/*', 'resources/patterns/relation/*'
                              'resources/patterns/sentiment/*', 'resources/patterns/timex/*', 'resources/pos/*', 'resources/statistics/*',
                             'userdict/*', 'similarity/*', 'utils/*', 'logs/*']},
      install_requires=[            # I get to this in a second
          'spacyWB',
          'wbjieba',
          'PyYAML',
          'OpenCC',
          'emoji',
          'pkseg',
          'jsonschema',
      ],
)
