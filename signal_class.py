import numpy as np
import matplotlib.pyplot as plt
from functools import lru_cache
class Signal:

    amostras_por_bit = 8
    bits_no_grafico = 20
    show_amostras = bits_no_grafico*amostras_por_bit

    def __init__(self, n_bits:int,encoding_dict:dict={0:0,1:1}):
        """_summary_

        Args:
            n_bits (int): length of the signal
            encoding_dict ([ int,int|list ], optional): Dict to convert the default signal to encoded. maps int keys(source signal) to list or int. Defaults to {0:0,1:1}.
        """
        self.encoding_dict = encoding_dict
        self.n_bits = n_bits

    @staticmethod
    def potencia(x) -> float:
        if not isinstance(x, np.ndarray):
            x = np.array(x)
        return np.sum(np.abs(x)**2)/len(x)

    @classmethod
    def snr(cls,sinal, ruido) -> float:
        return 10*np.log10(cls.potencia(sinal)/cls.potencia(ruido))

    @lru_cache(maxsize=None)
    def amplitude_para_snr(self,snr_dB,start=0.9,step=0.05):
        amplitude = start  # Tentativa inicial para a amplitude

        # Loop para ajustar a amplitude
        while True:  # Fazemos um número fixo de iterações para convergir
            gt, rt, xt = self.cria_vetores(amplitude)
            snr_calculado = self.snr(gt, rt)
            if snr_calculado >= snr_dB:
                break

            # Atualiza a amplitude para atingir o SNR desejado
            amplitude += step

        return amplitude
    
    def cria_vetores(self,amplitude=1,bits_per_symbol=1):
        np.random.seed(10)  # semente para gerar os mesmos números aleatórios
        # gera um vetor de N bits aleatórios
        gt = np.random.randint(0, 2**bits_per_symbol, self.n_bits)
        # gt = np.repeat(gt,amostras_por_bit) # repete cada bit pela quantidade de amostras
        gt = np.array([self.encoding_dict[b] for b in gt]).flatten()*amplitude

        # gera um vetor de números aleatórios com distribuição normal
        rt = np.random.normal(0, 1, len(gt))
        xt = gt + rt  # gera o sinal
        return gt, rt, xt