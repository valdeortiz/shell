from setuptools import setup
setup(
     name="shell",
     version='0.1',
     py_modules=['shell'],
     install_requires=[
                    'Click',
     ],
     entry_points='''
     [console_scripts]
     shell=shell:cli
''',
)