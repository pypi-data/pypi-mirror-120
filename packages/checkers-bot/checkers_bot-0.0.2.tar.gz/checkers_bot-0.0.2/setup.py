from setuptools import setup, find_packages


l = """[GitHub:](https://github.com/ruslan-ilesik/tic-tac-toe-bot-pip-package)
Usage Example
```python
```"""


setup(name='checkers_bot',
      version='0.0.2',
      description='Checkers bot using min max alghoritm',
      long_description=l,
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
      ],
      keywords='checkers bot api game_api ',
      url='https://github.com/ruslan-ilesik/Checkers-bot',
      author='lesikr',
      license='MIT',
      packages=['checkers'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False,
      )