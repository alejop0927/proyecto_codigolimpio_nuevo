

"""
Script principal para iniciar la aplicación desde consola.
Este archivo importa el menú principal desde src.view.menu y lo ejecuta.
"""

import sys
import os

# Agrega el directorio 'src' al path si no está
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.append(src_path)

from src.view.menu import Menu

if __name__ == "__main__":
    menu = Menu()
    menu.menu_principal()
