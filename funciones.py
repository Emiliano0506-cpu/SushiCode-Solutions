import os
import mysql.connector
from mysql.connector import Error

HOST = "127.0.0.1"
USUARIO = "root"
PASSWORD = ""
BASE_DATOS = "bd_sushicode"

def borrarPantalla():
    os.system("cls" if os.name == "nt" else "clear")

def espereTecla():
    input("\nPresiona ENTER para continuar...")

def conectar():
    try:
        return mysql.connector.connect(host=HOST, user=USUARIO, password=PASSWORD, database=BASE_DATOS)
    except Error as e:
        print(f"No se pudo conectar: {e}")
        print("Primero ejecuta sql/schema.sql y revisa las credenciales en funciones.py.")
        return None

def leer_entero(mensaje, minimo=None):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                raise ValueError
            return valor
        except ValueError:
            print("Ingresa un número entero válido.")

def leer_decimal(mensaje, minimo=0):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < minimo:
                raise ValueError
            return valor
        except ValueError:
            print("Ingresa una cantidad válida.")

def si_no(mensaje):
    return input(mensaje + " (s/n): ").strip().lower() in ("s", "si", "sí")
