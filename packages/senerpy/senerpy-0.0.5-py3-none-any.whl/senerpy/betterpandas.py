"""
Title: 
Author: Julio Rodriguez
Organization: SENER
"""

# BLK: Imports

# Standard Libraries
import cProfile
import pstats

# 3rd Party
# import pandas as pd


# Local Libraries


# Global variables
class Cstruct:
    pass


# Code

# Clases

# Funciones
def describe(dataframe):
    """
    Soluciona el problema con PyCharm al utilizar la función describe() que pone % en los índices
    :param dataframe: Pandas DataFrame a aplicar la función describe
    :return: Función describe aplicada sin % en los índices
    """
    df_describe = dataframe.describe().rename(index={'25%': '25', '50%': '50', '75%': 75})
    return df_describe
