import pandas as pd
import numpy as np
import csv


with open("Tabela.csv", "r", encoding="utf-8") as arquivo:
    arquivo_csv = csv.reader(arquivo, delimiter=";")
    for i, linha in enumerate(arquivo_csv):
        if i == 0:
            print("Cabeçalho: " + str(linha))
        else:
            print("Valor: " + str(linha))
