from os import pathsep, truncate
from typing import ContextManager, List
import copy


class Field():
	def __init__(self,turn = "white"):
		def add(color):
			for i in range(3):
				self.map.append([])
				for b in range(4):
					if len(self.map)%2 !=0:
						self.map[-1].append(None)
						self.map[-1].append(_Checker(color,self))
					else:
						self.map[-1].append(_Checker(color,self))
						self.map[-1].append(None)
		self.turn = turn			
		self.map = []
		add("black")
		for i in range(2):
			self.map.append([None for i in range(8)])
		add("white")

		self.__correct_positions()

		self.posible_moves = self.__posible_moves()
		self.__big_road_cords = [[0,1],[0,7],[1,0],[1,2],[1,6],[2,1],[2,3],[2,5],[3,2],[3,4],[4,3],[4,5],[5,2],[5,4],[5,6],[6,1],[6,5],[6,7],[7,0],[7,6]]
		self.__draw_rules = {'3k_b_r':0,'3k_n_b_r':0,'p_s':0,'n_e_n_t':0}
		self.__last_moves = []
		self.__recount_figures()

	def __str__(self) -> str:
		string = ''
		for b in self.map:
			for i in b:
				string +=("." if not i else (("B" if i.is_king else 'b') if i.color == "black" else ("W" if i.is_king else 'w')))
			string += '\n'
		return string[0:-1:]

	def get_map (self):
		return self.map
	def is_player_turn(self):
		return self.turn =="white"
	
	def move(self,path: list,place_anyway = False) -> str:
		eated = False
		if not path in self.posible_moves and not place_anyway:
			raise Exception('Path not in `self.posible_moves`. If you  want to make move anyway add argument `place_anyway` to function with value `True`')
		
		if not place_anyway:
			self.turn = ('white' if self.turn == 'black' else 'black')

			pr_p = path[0]
			for i in enumerate(path[1::],1):
				if abs(pr_p[0] - i[1][0]) > 1 or  abs(pr_p[1] - i[1][1]) > 1:
					if int(pr_p[0]-(pr_p[0] - i[1][0])/2) < len(self.map) and int(pr_p[1]-(pr_p[1] - i[1][1])/2) < len(self.map[0]) and self.map[int(pr_p[0]-(pr_p[0] - i[1][0])/2)][int(pr_p[1]-(pr_p[1] - i[1][1])/2)] and self.map[int(pr_p[0]-(pr_p[0] - i[1][0])/2)][int(pr_p[1]-(pr_p[1] - i[1][1])/2)].is_king:
						if self.turn == 'black':
							self.__black_k_amount -=1
						else:
							self.__white_k_amount -= 1
					else:
						if self.turn == 'black':
							self.__black_ch_amount -=1
						else:
							self.__white_ch_amount -= 1		

					self.map[int(pr_p[0]-(pr_p[0] - i[1][0])/2)][int(pr_p[1]-(pr_p[1] - i[1][1])/2)] = None
					eated = True

				self.map[i[1][0]][i[1][1]] , self.map[pr_p[0]][pr_p[1]] = self.map[pr_p[0]][pr_p[1]], self.map[i[1][0]][i[1][1]]
				pr_p = i[1]

			#change rules win/lose
			if eated:
				self.__draw_rules = {'3k_b_r':0,'3k_n_b_r':0,'p_s':0,'n_e_n_t':0}
			else:
				self.__draw_rules['n_e_n_t']+=1
			
			if self.__black_ch_amount == 0 and self.__black_k_amount == 3 and self.__white_ch_amount == 0 and self.__white_k_amount == 1: 
				white_k = [item   
								for row in self.map
								    for item in row
									  if item and item.color == 'white' and item.is_king  ][0]
				if white_k.position in self.__big_road_cords:
					self.__draw_rules['3k_b_r'] +=1
				else:
					self.__draw_rules['3k_n_b_r'] +=1
			elif self.__white_ch_amount == 0 and self.__white_k_amount == 3 and self.__black_ch_amount == 0 and self.__black_k_amount == 1: 
				black_k = [item
							   for row in self.map
							    	for item in row  
										if item and item.color == 'white' and item.is_king  ][0]
				if black_k.position in self.__big_road_cords:
					self.__draw_rules['3k_b_r'] +=1
				else:
					self.__draw_rules['3k_n_b_r'] +=1
			
		else:
			self.map[path[-1][0]][path[-1][1]]	 = self.map[path[0][0]][path[0][1]]
			self.map[path[0][0]][path[0][1]] = None
			self.__draw_rules['n_e_n_t'] = 0

		self.__last_moves.append(str(self))
		if len(self.__last_moves) > 4:
			self.__last_moves.pop(0)

			if self.__last_moves[-1] == self.__last_moves[1] or self.__last_moves[-2] == self.__last_moves[0]:
				if self.turn == 'white':
					self.__draw_rules['p_s'] += 1
			else:
				self.__draw_rules['p_s'] = 0

		self.__correct_positions()
		self.__make_kings()
		self.posible_moves  =  self.__posible_moves()
		self.__recount_figures()
		return self.check_winer()

	def check_winer(self):
		is_white = False
		is_black = False

		if not len(self.posible_moves):
			if self.turn == 'white':
				is_black = True
			elif self.turn == 'black':
				is_white = True
		if is_white:
			return 'white'
		elif is_black:
			return 'black'
		else:
			if self.__draw_rules['n_e_n_t'] >= 32 or self.__draw_rules['3k_b_r'] >= 5 or self.__draw_rules['3k_n_b_r'] >= 15 or self.__draw_rules['p_s'] >= 3: 
				return 'draw'
			elif ((self.__white_ch_amount <= 1 and self.__white_k_amount == 1) or (self.__white_ch_amount == 0 and self.__white_k_amount == 2)) and self.__black_ch_amount == 0 and self.__black_k_amount == 1:
				return 'draw'
			elif ((self.__black_ch_amount <= 1 and self.__black_k_amount == 1) or (self.__black_ch_amount == 0 and self.__black_k_amount == 2)) and self.__white_ch_amount == 0 and self.__white_k_amount == 1:
				return 'draw'

		return False	


	def figures_left(self):
		return {'black_ch':self.__black_ch_amount,'black_k':self.__black_k_amount,'white_ch':self.__white_ch_amount,'white_k':self.__white_k_amount}


	def __recount_figures(self):
			self.__black_k_amount = 0
			self.__white_k_amount = 0
			self.__black_ch_amount = 0
			self.__white_ch_amount = 0
			for i in self.map:
				for b in i:
					if b:
						if b.color == 'black':
							if b.is_king:
								self.__black_k_amount +=1
							else:
								self.__black_ch_amount +=1
						else:
							if b.is_king:
								self.__white_k_amount +=1
							else:
								self.__white_ch_amount +=1

	def __make_kings (self):
		for i in [0,7]:
			for obj in self.map[i]:
				if obj and not obj.is_king:
					self.__draw_rules = {'3k_b_r':0,'3k_n_b_r':0,'p_s':0,'n_e_n_t':0}
					if obj.color == 'white' and i == 0:
						obj.is_king = True
						self.__white_k_amount += 1
						self.__white_ch_amount -=1
					elif obj.color == 'black' and i == 7:
						obj.is_king = True
						self.__black_k_amount += 1
						self.__black_ch_amount -=1

	def __correct_positions(self):
		for y in enumerate(self.map):
			for x in enumerate(self.map[y[0]]):
				if x[1]:
					x[1].position = [y[0],x[0]]

	def __posible_moves(self):
		moves = []
		for i in self.map:
			for b in i:
				if b  and b.color == self.turn:
					moves.append(b.get_moves(self))
		eat_moves = []
		for i in moves:
			if i[0]:
				eat_moves.append(i)
		if len(eat_moves):
			moves = eat_moves

		real_moves = []
		for i in moves:
			real_moves += i[1]

		return real_moves			
					
class _Checker():
	def __init__(self,color,field ): #color - white, black
		self.is_king = False
		self.color = color
		self.position = [len(field.get_map())-1,len(field.get_map()[-1])]
	
	def get_moves(self,field: Field):	
		if field.turn != self.color:
			return [False,[]]

		def circle(path,pr_way):
			mp = copy.deepcopy(path[-1])
			p = copy.deepcopy(path)
			for way in ways:
				if [-way[0],-way[1]] == pr_way:
					continue
				path = copy.deepcopy(p)
				

				mp2 = [mp[0]+way[0],mp[1]+way[1]]
				if mp2[0] > 7  or mp2[0] <0 or mp2[1] > 7  or mp2[1] <0 :
					continue
				
				if not field.map[mp2[0]][mp2[1]]:
					if way == pr_way or self.is_king:
						moves.append(path)
				else:
					if (not field.map[mp2[0]][mp2[1]])  or field.map[mp2[0]][mp2[1]].color == self.color:
						continue
					if mp2[0]+way[0] < len(field.map) and mp2[1]+way[1] < len(field.map[0]) and  not  field.map[mp2[0]+way[0]][mp2[1]+way[1]]:
						path.append([mp2[0]+way[0],mp2[1]+way[1]])
						circle(path,way)
					else:
						moves.append(path)

		if self.is_king:
			ways = [[1,1],[1,-1],[-1,-1],[-1,1]]
		elif field.turn == "black":
			ways = [[1,1],[1,-1]] # [y,х]
		else:
			ways = [[-1,-1],[-1,1]]
			
		moves = []
				
		if self.is_king:
			for way in ways:			
				pos = self.position
				while True:
					path = [self.position]
					pos = [pos[0]+way[0],pos[1]+way[1]]
					if pos[0] > 7  or pos[0] <0 or pos[1] > 7  or pos[1] <0:
						break
					
					if field.map[pos[0]][pos[1]]:
						if pos[0]+way[0] < len(field.map) and pos[1]+way[1] < len(field.map[0]) and field.map[pos[0]][pos[1]].color != self.color and not field.map[pos[0]+way[0]][pos[1]+way[1]]:
							path.append([pos[0]+way[0],pos[1]+way[1]])
							circle(path,way)
					else:	
						path.append(pos)
						moves.append(path)

		else:		
			for way in ways:
				place = self.position
				path = [self.position]
				place = [place[0]+way[0],place[1]+way[1]]
				
				if place[0] > 7  or place[0] <0 or place[1] > 7  or place[1] <0:
					continue
				
				if field.map[place[0]][place[1]]:
					
					if field.map[place[0]][place[1]].color == self.color or place[0]+way[0] > 7  or place[0]+way[0] <0 or place[1]+way[1] > 7  or place[1]+way[1] <0:
						continue
					
					if not field.map[place[0]+way[0]][place[1]+way[1]]:
						path.append([place[0]+way[0],place[1]+way[1]])
						
						circle(path,way)
				else:
					path.append(place)
					moves.append(path)

		# filter moves:
		#find moves where eating:
		eat_moves = []
		for i in moves:
			p_p = i[0]
			for b in i:
				if not self.is_king and abs(b[0] - p_p[0]) > 1 and abs(b[1] - p_p[1]) > 1:
					eat_moves.append(i)
					break
				
				elif self.is_king and b != p_p:
					way = [(1 if b[0] - p_p[0] > 0 else -1),(1 if b[1] - p_p[1] > 0 else -1)]
					t_p = b
					while t_p != p_p:		
						if field.map[t_p[0]][t_p[1]]:
							eat_moves.append(i)
							break
						t_p = [t_p[0]-way[0],t_p[1]-way[1]]
				p_p = b

		if len(eat_moves) != 0 :
			moves = eat_moves
		
		#clear from copies:
		o = []
		for e in moves:
			if e not in o:
				o.append(e)

		# clear from partly eating
		o.sort(key=lambda s: len(s))

		full_parts = []
		for i in o:
			for part in full_parts:
				includes = True
				for d in enumerate(part,0):
					if d[1] != i[d[0]]:
						includes = False

				if includes:
					full_parts.remove(part)
			if not i in full_parts:
				full_parts.append(i)

		moves = full_parts

		return [len(eat_moves)>0,moves]



if __name__ == '__main__':	
	a = Field("white")
	print(a)
	print(a.posible_moves)
	print(a.figures_left())
