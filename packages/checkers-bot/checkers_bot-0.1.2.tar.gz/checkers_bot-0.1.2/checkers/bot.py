import copy
import time
import random

from .field import Field

class Bot():
    def __init__(self) -> None:
        self.my_king = 2
        self.my_checker = 1
        self.enemy_checker = -0.5
        self.enemy_king = -1.5

    def move(self,field: Field,depth: int):
        def recursive_check(field = field,times_left = depth):
            times_left  -= 1
            best = []
            if times_left <= 0 :
                scores =  0
                for row in field.map:
                    for item in row:
                        if item:
                            if item.color == color:
                                scores += (self.my_king if item.is_king else self.my_checker)
                            else:
                                scores += (self.enemy_king if item.is_king else self.enemy_checker)

                return scores

            for move in field.posible_moves:
                field_copy = copy.deepcopy(field)
                field_copy.move(move)
                best.append(recursive_check(field_copy,times_left))
            
            
            if len(best):
                if field.turn == color:
                    return random.choice([i for i, x in enumerate(best,0) if x == max(best)])
                else:
                    return random.choice([i for i, x in enumerate(best,0) if x == min(best)])  
            else:
                return 0    

        color = field.turn

        if len(field.posible_moves):
            try:
                best_move = field.posible_moves[recursive_check()]
                return field.move(best_move)
            except:
                return field.move(field.posible_moves[0])
        else:
            Exception('not moves awaible')




if __name__ == '__main__':
    field = Field()
    g_time = time.time()
    bot = Bot()
    bot1 = Bot()
    while True:
        
        print(bot.move(field,3))

        print(field)

        print(bot.move(field,3))

        print(field)
        if field.check_winer():
            break
