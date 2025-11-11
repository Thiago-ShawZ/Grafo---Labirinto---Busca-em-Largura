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

   