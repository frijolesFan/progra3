class KakuroCell:
    def __init__(self, cell_str):
        self.raw = cell_str
        self.is_black = cell_str.startswith('#')
        self.right_sum = None
        self.down_sum = None
        self.is_variable = cell_str == '.'
        if 'RD' in cell_str:
            parts = cell_str[2:].split('-')
            self.right_sum = int(parts[0]) if parts[0] != '0' else None
            self.down_sum = int(parts[1]) if parts[1] != '0' else None
        elif cell_str.startswith('R'):
            self.right_sum = int(cell_str[1:])
        elif cell_str.startswith('D'):
            self.down_sum = int(cell_str[1:])
        self.value = None

class KakuroBoard:
    def __init__(self, filename):
        self.grid = []
        with open(filename, 'r') as f:
            for line in f:
                row = [KakuroCell(cell.strip()) for cell in line.strip().split()]
                self.grid.append(row)
    
    def get_cell_str(self, cell):
        if cell.is_black:
            if cell.right_sum is None and cell.down_sum is None:
                return ' █ '
        if cell.is_variable:
            return f' {cell.value if cell.value else " "} '
        if cell.down_sum is not None and cell.right_sum is not None:
            return f' M '
        if cell.down_sum is not None:
            return f' ▼ '
        else:
            return f' ▶ '
    
    def print_pretty_board(self):
        # Imprimir números de columna
        print('   ' + ' '.join(f' {j+1}  ' for j in range(len(self.grid[0]))))
        print('  ┌' + '─' * (4 * len(self.grid[0])) + '┐')
        
        for i, row in enumerate(self.grid):
            print(f'{i+1} │', end='')
            for cell in row:
                print(self.get_cell_str(cell), end='')
                print('│', end='')
            print()
            
            if i < len(self.grid) - 1:
                print('  ├' + '─' * (4 * len(row)) + '┤')
            else:
                print('  └' + '─' * (4 * len(row)) + '┘')

# Ejemplo de uso
board = KakuroBoard('kakuro/tablerofacil.txt')
print("\nImpresión mejorada:")
board.print_pretty_board()