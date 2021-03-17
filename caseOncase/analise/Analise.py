import numpy as np
import matplotlib as mt
import pandas as pd
import json

class Analise(object):
    def __init__(self):
        self.arquivoDados = 'dados.json'

    def converteToCSV(self):
        jsonDados = json.load(self.arquivoDados)
        print(jsonDados)

