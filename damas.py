# coding: utf-8
# Aluno: Matheus Oliveira
# Disciplina: Programação I
# Miniprojeto 1: Damas
# Data: Junho de 2017

import os, sys
import pygame
from pygame.locals import *

pygame.init()

# início das constantes
BOARD_SIZE = 8
PIECE_RADIUS = 20

BOARD_COLOR_1 = (192, 108, 37)
BOARD_COLOR_2 = (236, 174, 118)
POSSIBLE_MOVEMENT = (125, 202, 92)

PLAYER1_COLOR = (197, 20, 16)
PLAYER2_COLOR = (23, 98, 167)

BLACK = (0, 0, 0)
GOLD = (255, 223, 0)
WHITE = (255, 255, 255)
# fim das constantes.

def help_page():
	
	screen = pygame.display.set_mode((680, 480))
	pygame.display.set_caption('Damas')
	
	screen.fill(BLACK)
	
	myfont = pygame.font.SysFont('Ubuntu', 18)
	textsurface = myfont.render('Pressione qualquer tecla para voltar ao menu', False, (255, 255, 255))
	screen.blit(textsurface,(0,0))
	pygame.display.update()
	
	while True:
		
		pygame.event.set_blocked(pygame.MOUSEMOTION)
		event = pygame.event.wait()
		
		if event.type == pygame.KEYDOWN:
			screen.fill(BLACK)
			pygame.display.update()
			break
		
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

#def menu():
   #screen = pygame.display.set_mode((680, 480))
   #pygame.display.set_caption('Damas')

   #menu = #OPÇÕES DO MENU
               #[('Iniciar partida', 1, None),
                #('Ajuda/Regras',  2, None),
                #('Creditos',    3, None),
                #('Sair',       4, None)])

   #menu.set_center(True, True)
   #menu.set_alignment('center', 'center')
   
   #myfont = pygame.font.Font(None, 45)
   #textsurface = myfont.render('Menu', False, (255, 0, 0))
   #screen.blit(textsurface,(270, 120))
   #pygame.display.update()

   #state = 0
   #prev_state = 1
   
   #rect_list = []

   #pygame.event.set_blocked(pygame.MOUSEMOTION)

   #while True:
      #if prev_state != state:
         #pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
         #prev_state = state

      #e = pygame.event.wait()

      #if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
         #if state == 0:
            #rect_list, state = menu.update(e, state)
         #elif state == 1:
            #print 'Jogo iniciado'
            #state = 0
         #elif state == 2:
            #print 'Ajuda/Regras'
            #help_page()
            #state = 0
         #elif state == 3:
            #print 'Créditos'
            #state = 0
         #else:
            #print 'Saindo...'
            #pygame.quit()
            #sys.exit()

      #if e.type == pygame.QUIT:
         #pygame.quit()
         #sys.exit()

      #pygame.display.update(rect_list)

class Piece(pygame.sprite.Sprite):
	def __init__(self, player, position, piece_id):
		colors = [PLAYER1_COLOR, PLAYER2_COLOR]
		
		self.color = colors[player-1]
		self.player = player
		
		self.position = position
		self.coord = [position[0]/60, position[1]/60]
		
		self.ID = piece_id
		self.status = 'man'
		
	def draw_piece(self, gameBoard):
		row = self.coord[1]
		column = self.coord[0]
		
		pygame.draw.circle(gameBoard, self.color, [column*60+30, row*60+30], PIECE_RADIUS)
		
		if self.status == 'king':	# desenho da 'coroa'
			pygame.draw.circle(gameBoard, GOLD, [column*60+30, row*60+30], PIECE_RADIUS-11)
		
	def check_movement(self, new_coord, gameBoard):
		# retorna True se o movimento for válido, False caso o contrário ocorra.
		# exceção: retorna o ID da peça se ela fizer uma captura durante o movimento.
		
		column = new_coord[0]
		row = new_coord[1]
		
		if self.status == 'king':
			captures = self.possible_captures(gameBoard)
		
		obligatory = self.obligatory_capture(gameBoard)
		
		if obligatory != []:
			if self.status == 'man':
				for i in xrange(len(obligatory)):
					if [column, row] == obligatory[i]:
						captures = self.possible_captures(gameBoard)
						
						cap_row = captures[i][1]
						cap_column = captures[i][0]
						
						for i in xrange(len(gameBoard.pieces)-1, -1, -1):
							if gameBoard.pieces[i].coord == [cap_column, cap_row]:
								gameBoard.pieces.pop(i)
								gameBoard.board_status[cap_row][cap_column] = 0
						
						return self.ID
			
				return False
			else:
				# IMPORTANTE: se a peça for uma dama, captures terá os ID's das possíveis
				# peças a serem capturadas.
				
				if [column, row] in obligatory:
					self_row = self.coord[1]
					self_column = self.coord[0]
					
					movement = [column - self_column, row - self_row]
								
					if abs(movement[0]) > 1:
						if movement[0] < 0: movement[0] = -1
						else: movement[0] = 1
					if abs(movement[1]) > 1:
						if movement[1] < 0: movement[1] = -1
						else: movement[1] = 1
						
					position_captured = [self_column + movement[0], self_row + movement[1]]
					
					while self.check_coord(position_captured):
						for i in xrange(len(gameBoard.pieces)):
							if gameBoard.pieces[i].coord == position_captured:
								
								gameBoard.board_status[gameBoard.pieces[i].coord[1]][gameBoard.pieces[i].coord[0]] = 0
								gameBoard.pieces.pop(i)
								
								return self.ID
						
						position_captured = [position_captured[0] + movement[0], position_captured[1] + movement[1]]
				
				return False
						
		
		if column < 0 or column > 7:
			return False
		if row < 0 or row > 7:
			return False
		
		if gameBoard.board_status[row][column] != 0:
			return False
		
		if self.status == 'man':
			if self.player == 2:
				if row != self.coord[1]-1:
					return False
				if column != self.coord[0]+1 and column != self.coord[0]-1:
					return False
			else:
				if row != self.coord[1]+1:
					return False
				if column != self.coord[0]+1 and column != self.coord[0]-1:
					return False
		else:
			adjacents = [self.get_NE(), self.get_NW(), self.get_SE(), self.get_SW()]
			valid = False	
			
			for i in xrange(len(adjacents)):
				for j in xrange(len(adjacents[i])):
					coord = adjacents[i][j]
					
					if [column, row] == coord:
						valid = True
					
			return valid
		
		return True
	
	def move(self, new_coord, gameBoard):
		# além de mover a peça, retorna True caso ela seja
		# coroada naquele movimento.
		
		row = self.coord[1]
		column = self.coord[0]
		
		gameBoard.board_status[row][column] = 0
		self.coord = new_coord
		
		row = self.coord[1]
		column = self.coord[0]
		gameBoard.board_status[row][column] = self.player
		
		if self.player == 2:	# condições para promoção da peça a Dama.
			if row == 0 and self.status == 'man':
				self.status = 'king'
		else:
			if row == 7 and self.status == 'man':
				self.status = 'king'
		
		gameBoard.update_board()
		
	def possible_moves(self, gameBoard):
		moves = []
		row = self.coord[1]
		column = self.coord[0]
		
		obligatory = self.obligatory_capture(gameBoard)
		
		if obligatory == []:
			if self.status == 'man':
				if self.player == 2:
					if self.check_movement([column-1, row-1], gameBoard):
						moves.append([column-1, row-1])
						
					if self.check_movement([column+1, row-1], gameBoard):
						moves.append([column+1, row-1])
				else:
					if self.check_movement([column-1, row+1], gameBoard):
						moves.append([column-1, row+1])
						
					if self.check_movement([column+1, row+1], gameBoard):
						moves.append([column+1, row+1])
				
				return moves
				
			else:
				adjacents = [self.get_NE(), self.get_NW(), self.get_SE(), self.get_SW()]
				
				for i in xrange(len(adjacents)):
					for j in xrange(len(adjacents[i])):
						row = adjacents[i][j][1]
						column = adjacents[i][j][0]
						
						if gameBoard.board_status[row][column] == 0:
							moves.append([column, row])
						else:
							break
				
				return moves
				
		else:
			return obligatory
	
	def get_adjacent(self):
		adjacents = []
		
		row = self.coord[1]
		column = self.coord[0]
		
		for i in xrange(row-1, row+2):
			for j in xrange(column-1, column+2):
				if i == row and j == column:
					continue
					
				if i >= 0 and j >= 0:
					if i <= 7 and j <= 7:
						adjacents.append([j, i])
			
		return adjacents
		
	def obligatory_capture(self, gameBoard):
		if self.status == 'man':
			adjacents = self.get_adjacent()
			obligatory = []
			
			for coord in adjacents:
				row = coord[1]
				column = coord[0]
				
				if gameBoard.board_status[row][column] != 0:		# verifica se há uma peça adjacente
					if gameBoard.board_status[row][column] != self.player:	# se houver, verifica se é inimiga
						row_piece = self.coord[1]
						column_piece = self.coord[0]
						
						# deslocamento necessário para chegar à posição da inimiga
						movement = [row_piece-row, column_piece-column]
						
						if self.status != 'king':
							if row - movement[0] >= 0 and row - movement[0] <= 7:
								if column - movement[1] >= 0 and column - movement[1] <= 7:
									if gameBoard.board_status[row - movement[0]][column - movement[1]] == 0:
										new_place = [column - movement[1], row - movement[0]]
										obligatory.append(new_place)
		else:
			# retorna os movimentos possíveis que a peça atual pode
			# fazer caso seja possível capturar uma  peça inimiga.
			
			adjacents = [self.get_NE(), self.get_NW(), self.get_SE(), self.get_SW()]
			obligatory = []
			
			for i in xrange(len(adjacents)-1, -1, -1):
				break_piece_loop = False
				
				for j in xrange(len(adjacents[i])):
					if break_piece_loop: break
					coord = adjacents[i][j]
					
					for piece in gameBoard.pieces:
						if piece.coord == coord:
							if piece.player != self.player:
								break_piece_loop = False
								
								row = coord[1]
								column = coord[0]
								
								row_self = self.coord[1]
								column_self = self.coord[0]
								
								movement = [column - column_self, row - row_self]
								
								if abs(movement[0]) > 1:
									if movement[0] < 0: movement[0] = -1
									else: movement[0] = 1
								if abs(movement[1]) > 1:
									if movement[1] < 0: movement[1] = -1
									else: movement[1] = 1
									
								new_place = [column + movement[0], row + movement[1]]
								
								if self.check_coord(new_place):
									if gameBoard.board_status[new_place[1]][new_place[0]] == 0:
										aux = new_place[:]
										obligatory.append(aux)
								
										new_place[0] += movement[0]
										new_place[1] += movement[1]
										
										while self.check_coord(new_place):
											if gameBoard.board_status[new_place[1]][new_place[0]] == 0:
												aux = new_place[:]
												obligatory.append(aux)
												
												new_place[0] += movement[0]
												new_place[1] += movement[1]
												
											else:
												adjacents.pop(i)
												break_piece_loop = True
												break
									else:
										adjacents.pop(i)
										break_piece_loop = True
								else:
									adjacents.pop(i)
									break_piece_loop = True
							
							if break_piece_loop:
								break
								
		return obligatory
		
	def possible_captures(self, gameBoard):
		# função parecida com a "obligatory_capture", dessa mesma classe, mas ao
		# invés de retornar as posições obrigatórias da peça naquele movimento,
		# ela retorna as coordenadas da peça inimiga que será capturada
		# se o movimento obrigatório for realizado.
		
		adjacents = self.get_adjacent()
		captures = []
		
		for coord in adjacents:
			row = coord[1]
			column = coord[0]
			
			if gameBoard.board_status[row][column] != 0:
				if gameBoard.board_status[row][column] != self.player:
					row_piece = self.coord[1]
					column_piece = self.coord[0]
					
					# deslocamento necessário para chegar à posição da inimiga
					movement = [row_piece-row, column_piece-column]
					
					if self.status != 'king':
						if row - movement[0] >= 0 and row - movement[0] <= 7:
							if column - movement[1] >= 0 and column - movement[1] <= 7:
								if gameBoard.board_status[row - movement[0]][column - movement[1]] == 0:
									captures.append([column, row])				
							
		return captures
	
	def get_NE (self):
		NE_aux = [1, 1]
		NE = [1, 1]
		
		row = self.coord[1]
		column = self.coord[0]
		
		x = []
		
		while True:
			possible = False
			if column + NE[0] <= 7 and column + NE[0] >= 0:
				if row + NE[1] <= 7 and row + NE[1] >= 0:
					x.append([column + NE[0], row + NE[1]])
					possible = True
					
			if not possible: break
			for j in xrange(2): NE[j] += NE_aux[j]
		
		return x
	
	def get_NW (self):
		NW_aux = [1, -1]
		NW = [1, -1]
		
		row = self.coord[1]
		column = self.coord[0]
		
		x = []
			
		while True:
			possible = False
			if column + NW[0] <= 7 and column + NW[0] >= 0:
				if row + NW[1] <= 7 and row + NW[1] >= 0:
					x.append([column + NW[0], row + NW[1]])
					possible = True
			
			if not possible: break
			for j in xrange(2): NW[j] += NW_aux[j]
		
		return x
		
	def get_SE (self):
		SE_aux = [-1, 1]
		SE = [-1, 1]
		
		row = self.coord[1]
		column = self.coord[0]
		
		x = []
		
		while True:
			possible = False	
			if column + SE[0] <= 7 and column + SE[0] >= 0:
				if row + SE[1] <= 7 and row + SE[1] >= 0:
					x.append([column + SE[0], row + SE[1]])
					possible = True
			
			if not possible: break
			for j in xrange(2): SE[j] += SE_aux[j]
		
		return x
		
	def get_SW (self):
		SW_aux = [-1, -1]
		SW = [-1, -1]
		
		row = self.coord[1]
		column = self.coord[0]
		
		x = []
			
		while True:
			possible = False	
			if column + SW[0] <= 7 and column + SW[0] >= 0:
				if row + SW[1] <= 7 and row + SW[1] >= 0:
					x.append([column + SW[0], row + SW[1]])
					possible = True
			
			if not possible: break
			for j in xrange(2): SW[j] += SW_aux[j]
		
		return x
	
	def check_coord(self, coord):
		# checa se a coordenada está contida no tabuleiro
		
		if coord[0] <= 7 and coord[0] >= 0:
			if coord[1] <= 7 and coord[1] >= 0:
				return True
		
		return False
		

class Board(pygame.sprite.Sprite):
	def __init__(self, board_size):
		self.colors = [BOARD_COLOR_1, BOARD_COLOR_2, POSSIBLE_MOVEMENT]	# cores do quadriculado alternado.
		
		self.grid_size = board_size		# tamanho do tabuleiro (n x n).
		self.surface_size = 480			# tamanho da tela em pixels.
		
		self.square_size = 60
		self.surface = pygame.display.set_mode((self.surface_size, self.surface_size)) # +220 1ºp (MENU)
		
		self.board_status = []
		self.amount_pieces = 0
		
		self.rounds = 1
		
		for i in xrange(board_size):
			self.board_status.append([])
			for j in xrange(0, board_size):
				self.board_status[i].append(0)
				
		for i in xrange(board_size):	# adicionando peças iniciais ao board_status.
			if i == 3 or i == 4: continue
			
			if(i <= 3): player = 1
			else: player = 2
			
			ini = i%2	
			
			for j in xrange(ini, board_size, 2):
				if player == 1: 
					self.board_status[i][j] = 1
				elif player == 2:
					self.board_status[i][j] = 2
		
	def initialize_board(self):
		for row in xrange(self.grid_size):
			actual_color = row%2
			
			for column in xrange(self.grid_size):	# desenhando o tabuleiro
				square = (column*self.square_size, row*self.square_size, self.square_size, self.square_size)
				
				self.surface.fill(self.colors[actual_color], square)
				actual_color = (actual_color+1)%2
	
	def get_info(self):
		print 'Board status: '
		
		for i in xrange(self.grid_size):	# exibição do status atual do tabuleiro ao programador.
			print self.board_status[i]
		
		print
		
	def initialize_pieces(self):
		self.pieces = []
		
		for row in xrange(self.grid_size):

			actual_color = row%2
			
			if(row <= 3): player = 1
			else: player = 2
			
			for column in xrange(self.grid_size):
				if self.board_status[row][column] != 0:
					new_piece = Piece(player, [column*self.square_size+30, row*self.square_size+30], self.amount_pieces+2)
					new_piece.draw_piece(self.surface)
					
					self.pieces.append(new_piece)
					self.amount_pieces += 1
	
	def update_board(self):
		self.surface.fill(BLACK)
		
		self.initialize_board()
		
		for piece in self.pieces:
			piece.draw_piece(self.surface)
		
		pygame.display.update()
	
	def show_possible_moves(self, possible_moves):
		for coord in possible_moves:
		
			column = coord[0]
			row = coord[1]
			
			square = (column*self.square_size, row*self.square_size, self.square_size, self.square_size)
			self.surface.fill(self.colors[2], square)
		
		pygame.display.update()
	
	def blind_pieces(self):
		quantity_pieces = len(self.pieces)
		blind_pieces = []
		
		for i in xrange(quantity_pieces):	# checando as peças de mov obrigatório do player da vez
			if self.pieces[i].player % 2 == (self.rounds-1)%2:
				obligatory = self.pieces[i].obligatory_capture(gameBoard)
				
				if obligatory != []:
					blind_pieces.append(self.pieces[i].ID)
		
		return blind_pieces
	
	def multiple_jump(self, piece_ID):
		blind_pieces_id = self.blind_pieces()
		multiple_jump = False
		
		if blind_pieces_id != []:
			for ID in blind_pieces_id:
				if piece_ID == ID:
					multiple_jump = True
					break
		
		return multiple_jump
	
	def get_click_coord(self):
		new_click = pygame.event.wait()
					
		while new_click.type != pygame.MOUSEBUTTONDOWN:
			new_click = pygame.event.wait()
		
		new_position = pygame.mouse.get_pos()
		new_coord = [new_position[0]/60, new_position[1]/60]
		
		return new_coord
						
gameBoard = Board(BOARD_SIZE)
sqr_size = gameBoard.square_size
gameBoard.initialize_pieces()

#menu()

pygame.display.set_caption('Damas')
pygame.display.update()

gameExit = False

while not gameExit:
	event = pygame.event.wait()
	
	if event.type == pygame.QUIT:
		gameExit = True
		
	if event.type == pygame.MOUSEBUTTONDOWN:
		mouse_position = pygame.mouse.get_pos()
		
		actual_column = mouse_position[0]/60
		actual_row = mouse_position[1]/60
		
		actual_coordinate = [actual_column, actual_row]
		
		print 'You clicked at', [actual_row, actual_column]
		
		for piece in gameBoard.pieces:
			if piece.coord == actual_coordinate:
				if piece.player%2 == (gameBoard.rounds-1)%2:	# checando se a peça clicada é do player da vez
					
					blind_pieces_id = gameBoard.blind_pieces()
					
					if blind_pieces_id != []:	# se houver peças de movimento obrigatório...
						allowed_piece = False
						
						for ID in blind_pieces_id:	# ... checa se a peça clicada é uma delas.
							if piece.ID == ID:
								allowed_piece = True
								
						if not allowed_piece:
							continue
					
					possible_moves = piece.possible_moves(gameBoard)
					
					if possible_moves != []:
						gameBoard.show_possible_moves(possible_moves)
						
						click = gameBoard.get_click_coord()
						valid_movement = piece.check_movement(click, gameBoard)
						
						if valid_movement != False:
							status = piece.status
							piece.move(click, gameBoard)
							
							if status != piece.status:	# quando a peça for promovida
								valid_movement = True
							
							if valid_movement != True:	# quando a peça que se moveu capturar uma peças
								multiple_jump = gameBoard.multiple_jump(piece.ID)
								allowed_piece = piece.ID
								
								while multiple_jump:
									click = gameBoard.get_click_coord()
									
									for piece in gameBoard.pieces:
										if piece.coord == click:
											if piece.ID == allowed_piece:
												possible_moves = piece.possible_moves(gameBoard)
												gameBoard.show_possible_moves(possible_moves)
												
												click = gameBoard.get_click_coord()
												valid_movement = piece.check_movement(click, gameBoard)
												
												if valid_movement != False:
													piece.move(click, gameBoard)
													multiple_jump = gameBoard.multiple_jump(piece.ID)
																						
									gameBoard.update_board()
							
							gameBoard.rounds += 1
						else:
							print 'Invalid movement. Try again.'
							gameBoard.get_info()
				
	gameBoard.update_board()				

pygame.quit()
quit()
