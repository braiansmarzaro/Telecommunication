import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np
class FiltroCasado:
    def __init__(self,symbols):
        self.symbols:np.ndarray[list[int]] = np.array(symbols) # lista de simbolos
        self.filters = np.array([s[::-1] for s in symbols]) # lista de filtros
        self.T = len(symbols[0])-1 # Posição do ultimo elemento do simbolo
        for s1,s2 in combinations(self.filters,2):
            if s1@s2 != 0:
                raise ValueError(f"Símbolos {s1} e {s2} não são ortogonais")
            if len(s1) != len(s2):
                raise ValueError(f"Símbolos {s1} e {s2} não possuem o mesmo tamanho")
            
    def get_plot(self,figsize=(12, 5)):
        fig, axes = plt.subplots(figsize=figsize, nrows=(self.T+1)//2, ncols=(self.T+1)//2)
        fig.suptitle('Convolução entre entradas e filtros')

        for i in range(len(self.symbols)):
            for j in range(len(self.filters)):
                convolve = np.convolve(self.symbols[i], self.filters[j], mode='full')
                axes[i, j].plot(convolve)
                axes[i, j].set_title(f'Entrada {i+1} x Filtro {j+1}')
                axes[i, j].set_xlim(-1, len(convolve))
                axes[i, j].set_xticks(np.arange(0, len(convolve)+1))
                axes[i, j].set_yticks(np.arange(min(convolve)-1, max(convolve)+1))
                axes[i, j].grid()

        fig.tight_layout()
        return fig, axes
    
    def get_output(self, input_signal:np.ndarray):
        """Return the symbols that match the input signal based on filter convolutions

        Args:
            input_signal (np.ndarray): _description_
        """        

        output = []
        for symbol in input_signal:
            step = []
            for filter in self.filters:
                convolve = np.convolve(symbol, filter, mode='full')
                step.append(convolve[self.T])
            argmax = np.argmax(step)
            output.append(self.symbols[argmax])
if __name__=='__main__':
    symbols = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1,-1, 1,-1, 1,-1, 1,-1],
        [1, 1,-1,-1, 1, 1,-1,-1],
        [1,-1,-1, 1, 1,-1,-1, 1]
    ]
    fc = FiltroCasado(symbols)
    fc.get_plot()