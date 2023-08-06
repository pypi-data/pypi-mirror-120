from setuptools import setup, find_packages


l = """[GitHub:](https://github.com/ruslan-ilesik/tic-tac-toe-bot-pip-package)
Usage Example
```python
from checkers import Field,Bot
game = Field(turn = 'white') #could be white and black
bot = Bot() #init bot
print(game)
```
> .b.b.b.b
    b.b.b.b.
    .b.b.b.b
    ........
    ........
    w.w.w.w.
    .w.w.w.w
    w.w.w.w.
```python
print(game.turn)
```
> white
```python
print(game.posible_moves)
```
> [[[5, 0], [4, 1]], [[5, 2], [4, 1]], [[5, 2], [4, 3]], [[5, 4], [4, 3]], [[5, 4], [4, 5]], [[5, 6], [4, 5]], [[5, 6], [4, 7]]]
```python
print(game.move(game.posible_moves[0])) #make move returns False, draw, white or black  (who wins)
```
> False
```python
print(game)
```
> .b.b.b.b
    b.b.b.b.
    .b.b.b.b
    ........
    .w......
    ..w.w.w.
    .w.w.w.w
    w.w.w.w.
```python
print(game.check_winer()) #returns False, draw, white or black  (who wins)
```
> False
```python
print(bot.move(game,depth = 3)) #depth - int
```
> False"""


setup(name='checkers_bot',
      version='0.1.2',
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