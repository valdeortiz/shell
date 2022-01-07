from setuptools import setup
setup(
     name="shell",
     version='0.1',
     install_requires=[
                    'Click','click-shell','signals',
     ],
     entry_points='''
     [console_scripts]
     shell=main:cli
''',
)
