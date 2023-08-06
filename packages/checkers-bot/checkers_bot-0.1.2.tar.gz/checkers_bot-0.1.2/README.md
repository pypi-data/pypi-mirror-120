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
> False