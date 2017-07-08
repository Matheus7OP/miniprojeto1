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
BLUE = (23, 98, 167)
RED = (197, 20, 16)
# fim das constantes.

class Piece():
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

class Board():
	def __init__(self, board_size):
		self.colors = [BOARD_COLOR_1, BOARD_COLOR_2, POSSIBLE_MOVEMENT]	# cores do quadriculado alternado.
		
		self.grid_size = board_size		# tamanho do tabuleiro (n x n).
		self.surface_size = 480			# tamanho da tela em pixels.
		
		self.square_size = 60
		self.surface = pygame.display.set_mode((self.surface_size+220, self.surface_size)) # +220 1ºp (MENU)
		
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
		self.interface()
		square = (0, 0, 480, 480)
		self.surface.fill(BLACK, square)
		
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
	
	def interface(self):
		square = (480, 0, 220, 480)
		self.surface.fill(BLACK, square)
		
		myfont = pygame.font.Font(None, 24)
		total_pieces = 12
		
		player_1_captures = total_pieces
		player_2_captures = total_pieces
		
		for piece in self.pieces:
			if piece.player == 1:
				player_2_captures -= 1
			else:
				player_1_captures -= 1
		
		infos_p1_1 = myfont.render('O jogador Azul fez:', False, (PLAYER2_COLOR))
		infos_p1_2 = myfont.render(str(player_2_captures) + ' captura(s)', False, (WHITE))
		infos_p1_3 = myfont.render(str(gameBoard.rounds/2) + ' jogada(s)', False, (WHITE))
		
		infos_p2_1 = myfont.render('O jogador Vermelho fez:', False, (PLAYER1_COLOR))
		infos_p2_2 = myfont.render(str(player_1_captures) + ' captura(s)', False, (WHITE))
		infos_p2_3 = myfont.render(str( (gameBoard.rounds-1) / 2) + ' jogada(s)', False, (WHITE))
		
		self.surface.blit(infos_p2_1,(500,80))
		self.surface.blit(infos_p2_3,(502,100))
		self.surface.blit(infos_p2_2,(502,120))
		
		self.surface.blit(infos_p1_1,(500,320))
		self.surface.blit(infos_p1_3,(502,340))
		self.surface.blit(infos_p1_2,(502,360))
		
		player_turn = (gameBoard.rounds-1)%2
		
		if player_turn == 1: 
			player_turn = 'Vermelho'
			actual_round = myfont.render('Vez do jogador ' + player_turn, False, (PLAYER1_COLOR))
		else:
			player_turn = 'Azul'
			actual_round = myfont.render('Vez do jogador ' + player_turn, False, (PLAYER2_COLOR))
		
		self.surface.blit(actual_round,(500,220))
		pygame.display.update()
	
	def help_page(self):
		self.surface.fill(BLACK)

		myfont = pygame.font.Font(None, 30)
		important = myfont.render('Pressione qualquer tecla para voltar ao menu.', False, (255, 255, 255))
		self.surface.blit(important, (5, 455))

		myfont = pygame.font.Font(None, 25)
		
		info1 = myfont.render('O jogo de damas e praticado em um tabuleiro de 64 casas.', False, (BOARD_COLOR_1))
		info2 = myfont.render('O objetivo do jogo e capturar todas as pecas do adversario.', False, (BOARD_COLOR_2))
		info3 = myfont.render('A peca anda so para frente, uma casa de cada vez, na diagonal.', False, (BOARD_COLOR_2))
		info4 = myfont.render('Quando a peca atinge a oitava linha do tabuleiro ela e promovida a dama.', False, (BOARD_COLOR_2))
		info5 = myfont.render('A dama e uma peca de movimentos mais amplos. Ela anda para frente e para tras,', False, (BOARD_COLOR_1))
		info6 = myfont.render('quantas casas quiser, nao podendo saltar sobre uma peca da mesma cor. ', False, (BOARD_COLOR_1))
		info7 = myfont.render('A captura e obrigatoria, ou seja, nao existe sopro.', False, (BOARD_COLOR_2))
		info8 = myfont.render('Duas ou mais pecas juntas, na mesma diagonal, nao podem ser capturadas.', False, (BOARD_COLOR_2))
		info9 = myfont.render('A peca e a dama podem capturar tanto para frente como para tras.', False, (BOARD_COLOR_1))
		info10 = myfont.render('O movimento de captura pode ser encadeado sem que o jogador passe a vez.', False, (BOARD_COLOR_1))
		
		game1 = myfont.render('Durante o jogo, ao clicar em uma peca, sera exibido em verde os movimentos', False, (BLUE))
		game2 = myfont.render('possiveis da mesma. Se nada acontecer ao clicar em uma peca, significa que', False, (BLUE))
		game3 = myfont.render('ela nao tem movimentos possiveis ou o turno pertence ao outro jogador.', False, (BLUE))
		game4 = myfont.render('Divirta-se!   =)', False, (RED))
		
		self.surface.blit(info1, (5, 45))
		self.surface.blit(info2, (5, 75))
		self.surface.blit(info3, (5, 95))
		self.surface.blit(info4, (5, 115))
		self.surface.blit(info5, (5, 145))
		self.surface.blit(info6, (5, 165))
		self.surface.blit(info7, (5, 195))
		self.surface.blit(info8, (5, 215))
		self.surface.blit(info9, (5, 245))
		self.surface.blit(info10, (5, 265))
		
		self.surface.blit(game1, (5, 295))
		self.surface.blit(game2, (5, 315))
		self.surface.blit(game3, (5, 335))
		self.surface.blit(game4, (5, 365))
		
		pygame.display.update()

		while True:
			event = pygame.event.wait()

			if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
				self.surface.fill(BLACK)
				pygame.display.update()
				break

			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
	
	def mcredits(self):
		self.surface.fill(BLACK)

		myfont = pygame.font.Font(None, 30)
		important = myfont.render('Pressione qualquer tecla para voltar ao menu.', False, (255, 255, 255))
		self.surface.blit(important, (5, 455))

		myfont = pygame.font.Font(None, 25)
		
		info1 = myfont.render('Programador: Matheus Oliveira', False, (BLUE))
		info2 = myfont.render('Disciplina: Programacao 1 / Laboratorio de Programacao 1', False, (RED))
		info3 = myfont.render('Data: Junho de 2017', False, (RED))
		info4 = myfont.render('Versao do Python utilizada: 2.7', False, (BOARD_COLOR_2))
		info5 = myfont.render('Versao do Pygame utilizada: 1.9.1', False, (BOARD_COLOR_2))
		
		
		self.surface.blit(info1, (5, 55))
		self.surface.blit(info2, (5, 105))
		self.surface.blit(info3, (5, 125))
		self.surface.blit(info4, (5, 165))
		self.surface.blit(info5, (5, 185))
		
		pygame.display.update()

		while True:
			event = pygame.event.wait()

			if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
				self.surface.fill(BLACK)
				pygame.display.update()
				break

			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

	def menu(self):
		while True:
			self.surface.fill(BLACK)
			menu_quit = False

			myfont = pygame.font.Font(None, 45)
			menu = myfont.render('Menu', False, (BLUE))
			self.surface.blit(menu,(295, 120))
			
			myfont = pygame.font.Font(None, 30)
			
			opt_1 = myfont.render('Iniciar partida', False, (WHITE))
			opt_2 = myfont.render('Ajuda/Regras', False, (WHITE))
			opt_3 = myfont.render('Creditos', False, (WHITE))
			opt_4 = myfont.render('Sair', False, (WHITE))
			
			self.surface.blit(opt_1,(270, 180))
			self.surface.blit(opt_2,(270, 210))
			self.surface.blit(opt_3,(270, 240))
			self.surface.blit(opt_4,(272, 270))
			
			pygame.display.update()
			
			intervals = [ [ [272, 400], [183, 197] ], [ [272, 400], [215, 227] ],
						[ [272, 400], [242, 258] ], [ [272, 395], [273, 288] ] ]
			
			
			e = pygame.event.wait()

			if e.type == pygame.MOUSEBUTTONDOWN:
				mouse_position = pygame.mouse.get_pos()
				
				if mouse_position[1] >= 170 and mouse_position[1] <= 305:
					if mouse_position[0] >= 270 and mouse_position[0] <= 405:		
						for i in xrange(len(intervals)):
							interval = intervals[i]
							
							if mouse_position[0] >= interval[0][0] and mouse_position[0] <= interval[0][1]:
								if mouse_position[1] >= interval[1][0] and mouse_position[1] <= interval[1][1]:
									
									if i == 0:		# Iniciar partida
										menu_quit = True
										break
										
									elif i == 1:	# Ajuda/Regras
										self.help_page()
										
									elif i == 2:	# Creditos
										self.mcredits()
										
									else:			# Sair do jogo
										pygame.quit()
										sys.exit()
										
						
						if menu_quit:
							break

			if e.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

						
gameBoard = Board(BOARD_SIZE)
sqr_size = gameBoard.square_size

pygame.display.set_caption('Damas')
gameBoard.initialize_pieces()
gameBoard.menu()

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
