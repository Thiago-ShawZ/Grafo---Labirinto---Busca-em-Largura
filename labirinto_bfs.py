import tkinter as tk
from collections import deque

class MazeEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de Labirinto")

        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()

        self.tool_var = tk.StringVar(value='Caminho')
        self.labirinto = [[' ' for _ in range(30)] for _ in range(20)]
        self.grid_cells = [[None for _ in range(30)] for _ in range(20)]
        self.inicio_pos = None
        self.fim_pos = None
        self.fila = deque()
        self.visitados = set()
        self.predecessores = {}
        self.job_after = None
        
        self.desenhar_grid_inicial()
        self.criar_controles()

    def desenhar_grid_inicial(self):
        cell_width = 600 // 30
        cell_height = 400 // 20
        
        for i in range(20):
            for j in range(30):
                x1 = j * cell_width
                y1 = i * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='gray')
                self.grid_cells[i][j] = rect

    def criar_controles(self):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Radiobutton(frame, text="Parede", variable=self.tool_var, value='Parede').pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="Caminho", variable=self.tool_var, value='Caminho').pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="Início", variable=self.tool_var, value='Início').pack(side=tk.LEFT)
        tk.Radiobutton(frame, text="Fim", variable=self.tool_var, value='Fim').pack(side=tk.LEFT)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        tk.Button(button_frame, text="Iniciar Busca (BFS)", command=self.iniciar_busca).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Resetar Busca", command=self.resetar_busca).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Limpar Labirinto", command=self.limpar_labirinto).pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)

    def on_canvas_click(self, event):
        self.editar_celula(event.x, event.y)

    def on_canvas_drag(self, event):
        self.editar_celula(event.x, event.y)

    def editar_celula(self, x, y):
        cell_width = 600 // 30
        cell_height = 400 // 20

        col = x // cell_width
        row = y // cell_height

        if self.tool_var.get() == 'Parede':
            self.labirinto[row][col] = '#'
            self.canvas.itemconfig(self.grid_cells[row][col], fill='black')
        elif self.tool_var.get() == 'Caminho':
            self.labirinto[row][col] = ' '
            self.canvas.itemconfig(self.grid_cells[row][col], fill='white')
        elif self.tool_var.get() == 'Início':
            if self.inicio_pos:
                self.labirinto[self.inicio_pos[0]][self.inicio_pos[1]] = ' '
                self.canvas.itemconfig(self.grid_cells[self.inicio_pos[0]][self.inicio_pos[1]], fill='white')

            self.inicio_pos = (row, col)
            self.labirinto[row][col] = 'S'
            self.canvas.itemconfig(self.grid_cells[row][col], fill='green')
        elif self.tool_var.get() == 'Fim':
            if self.fim_pos:
                self.labirinto[self.fim_pos[0]][self.fim_pos[1]] = ' '
                self.canvas.itemconfig(self.grid_cells[self.fim_pos[0]][self.fim_pos[1]], fill='white')

            self.fim_pos = (row, col)
            self.labirinto[row][col] = 'E'
            self.canvas.itemconfig(self.grid_cells[row][col], fill='red')

    def iniciar_busca(self):
        if not self.inicio_pos or not self.fim_pos:
            return
        self.desabilitar_edicao()
        self.fila.clear()
        self.visitados.clear()
        self.predecessores = {}
        self.fila.append(self.inicio_pos)
        self.visitados.add(self.inicio_pos)

        self.processar_passo_bfs()

    def processar_passo_bfs(self):
        if not self.fila:
            print("Caminho não encontrado")
            return

        current_pos = self.fila.popleft()
        row, col = current_pos

        if current_pos == self.fim_pos:
            self.reconstruir_caminho()
            return

        self.canvas.itemconfig(self.grid_cells[row][col], fill='blue')

        vizinhos = self.obter_vizinhos(row, col)
        for vizinho in vizinhos:
            if vizinho not in self.visitados:
                self.visitados.add(vizinho)
                self.predecessores[vizinho] = current_pos
                self.fila.append(vizinho)
                r, c = vizinho
                self.canvas.itemconfig(self.grid_cells[r][c], fill='yellow')

        self.job_after = self.root.after(100, self.processar_passo_bfs)

    def obter_vizinhos(self, row, col):
        vizinhos = []
        if row > 0 and self.labirinto[row - 1][col] != '#':  # Cima
            vizinhos.append((row - 1, col))
        if row < 19 and self.labirinto[row + 1][col] != '#':  # Baixo
            vizinhos.append((row + 1, col))
        if col > 0 and self.labirinto[row][col - 1] != '#':  # Esquerda
            vizinhos.append((row, col - 1))
        if col < 29 and self.labirinto[row][col + 1] != '#':  # Direita
            vizinhos.append((row, col + 1))
        return vizinhos

    def reconstruir_caminho(self):
        path = []
        current_pos = self.fim_pos
        while current_pos != self.inicio_pos:
            path.append(current_pos)
            current_pos = self.predecessores[current_pos]
        path.append(self.inicio_pos)
        path.reverse()

        for pos in path:
            row, col = pos
            self.canvas.itemconfig(self.grid_cells[row][col], fill='gold')

    def resetar_busca(self):
        for i in range(20):
            for j in range(30):
                if self.labirinto[i][j] == ' ':
                    self.canvas.itemconfig(self.grid_cells[i][j], fill='white')
                elif self.labirinto[i][j] == 'S':
                    self.canvas.itemconfig(self.grid_cells[i][j], fill='green')
                elif self.labirinto[i][j] == 'E':
                    self.canvas.itemconfig(self.grid_cells[i][j], fill='red')