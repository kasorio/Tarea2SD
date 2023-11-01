import csv
import base64

def corregir_padding(data):
    # Calcula cuántos caracteres de relleno '=' se necesitan
    padding = (4 - (len(data) % 4)) % 4
    corrected_data = data + '=' * padding
    return corrected_data

# Abre el archivo CSV en modo lectura
with open('respuestas.csv', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    # Itera sobre las filas del archivo
    for row in reader:
        data = corregir_padding(row[1])
        try:
            decoded_data = base64.b64decode(data)
            decoded_string = decoded_data.decode('utf-8')  # Decodificar a cadena de texto
            print(decoded_string)
        except base64.binascii.Error as e:
            print(f"Error en fila {reader.line_num}: {e}")
