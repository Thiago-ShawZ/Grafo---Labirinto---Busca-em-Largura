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

    