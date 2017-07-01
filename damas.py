# coding: utf-8
# Aluno: Matheus Oliveira
# Disciplina: Programação I
# Miniprojeto Damas

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
WHITE = (255, 255, 255)
# fim das constantes.

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
		
	def check_movement(self, new_coord, gameBoard):	# exceção: retorna o ID da peça se ela fizer uma captura
		column = new_coord[0]
		row = new_coord[1]
		
		obligatory = self.obligatory_capture(gameBoard)
		
		if obligatory != []:
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
		
		if column < 0 or column > 7:
			return False
		if row < 0 or row > 7:
			return False
		
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
			
		if gameBoard.board_status[row][column] != 0:
			return False
		
		return True
	
	def move(self, new_coord, gameBoard):
		row = self.coord[1]
		column = self.coord[0]
		
		gameBoard.board_status[row][column] = 0
		self.coord = new_coord
		
		row = self.coord[1]
		column = self.coord[0]
		gameBoard.board_status[row][column] = self.player
		
	def possible_moves(self, gameBoard):
		moves = []
		row = self.coord[1]
		column = self.coord[0]
		
		obligatory = self.obligatory_capture(gameBoard)
		
		if obligatory == []:
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
		adjacents = self.get_adjacent()
		obligatory = []
		
		for coord in adjacents:
			row = coord[1]
			column = coord[0]
			
			if gameBoard.board_status[row][column] != 0:
				if gameBoard.board_status[row][column] != self.player:
					row_piece = self.coord[1]
					column_piece = self.coord[0]
					
					movement = [row_piece-row, column_piece-column]
					
					if row - movement[0] >= 0 and row - movement[1] <= 7:
						if column - movement[1] >= 0 and column - movement[1] <= 7:
							if gameBoard.board_status[row - movement[0]][column - movement[1]] == 0:
								new_place = [column - movement[1], row - movement[0]]
								obligatory.append(new_place)
		
		return obligatory
		
	def possible_captures(self, gameBoard):
		adjacents = self.get_adjacent()
		captures = []
		
		for coord in adjacents:
			row = coord[1]
			column = coord[0]
			
			if gameBoard.board_status[row][column] != 0:
				if gameBoard.board_status[row][column] != self.player:
					row_piece = self.coord[1]
					column_piece = self.coord[0]
					
					movement = [row_piece-row, column_piece-column]		# quanto a peça deslocou
					
					if row - movement[0] >= 0 and row - movement[1] <= 7:
						if column - movement[1] >= 0 and column - movement[1] <= 7:
							if gameBoard.board_status[row - movement[0]][column - movement[1]] == 0:
								new_place = [column - movement[1], row - movement[0]]
								captures.append([column, row])
							
		return captures
	
	#def get_movement(self, movement):
		#if movement == [1, 1]:
			#return 'NORTHWEST'
		#if movement == [1, -1]:
			#return 'NORTHEAST'
		#if movement == [-1, 1]:
			#return 'SOUTHWEST'
		#if movement == [-1, -1]:
			#return 'SOUTHEAST'
		

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
					new_piece = Piece(player, [column*self.square_size+30, row*self.square_size+30], self.amount_pieces)
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
							piece.move(click, gameBoard)
							
							if valid_movement != True:
								multiple_jump = gameBoard.multiple_jump(piece.ID)
								allowed_piece = piece.ID
								
								while multiple_jump:
									gameBoard.update_board()
									click = gameBoard.get_click_coord()
									
									for piece in gameBoard.pieces:
										if piece.coord == click:
											if piece.ID == allowed_piece:
												possible_moves = piece.possible_moves(gameBoard)
												gameBoard.show_possible_moves(possible_moves)
												
												click = gameBoard.get_click_coord()
												valid_movement = piece.check_movement(click, gameBoard)
												
												if valid_movement:
													piece.move(click, gameBoard)
													multiple_jump = gameBoard.multiple_jump(piece.ID)
							
							gameBoard.rounds += 1
						else:
							print 'Invalid movement. Try again.'
							gameBoard.get_info()
				
	gameBoard.update_board()				

pygame.quit()
quit()
