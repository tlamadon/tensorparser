from setuptools import setup

setup(name='tensorparser',
      version='0.11',
      description='Generate code from tensor expressions',
      url='https://github.com/tlamadon/tensorparser',
      author='Thibaut Lamadon',
      author_email='thibaut.lamadon@gmail.com',
      license='MIT',
      packages=['tensorparser'],
      scripts=['bin/tensorparser'],
      zip_safe=False)