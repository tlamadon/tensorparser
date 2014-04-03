from setuptools import setup

setup(name='tensorparser',
      version='0.1',
      description='Generate code from tensor expressions',
      url='http://github.com/storborg/funniest',
      author='Thibaut Lamadon',
      author_email='thibaut.lamadon@gmail.com',
      license='MIT',
      packages=['tensorparser'],
      scripts=['bin/tensorparser'],
      zip_safe=False)