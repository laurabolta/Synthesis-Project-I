import csv
from collections import defaultdict

# Ruta del archivo CSV
csv_path = '/mnt/c/Users/sonia/OneDrive/Documents/UAB/Segon/2 semestre/Synthesis Project/Estudiants_èxit_accés_anònim.csv'

# Campos del CSV
campos = [
    "Estudi",
    "Curs acadèmic",
    #"Id Anonim", #not necessary to print
    "Sexe",
    "Curs acadèmic accés estudi",
    "Via Accés Estudi",
    "Nota d'accés (preinscripció)",
    "Dedicació de l'estudiant",
    "S/N Discapacitat",
    "Beca Concedida?",
    "Estudis Mare",
    "Estudis Pare",
    "Taxa èxit"
]

# Rangos para notas de acceso
rangos_notas = [
    (0, 3, "0-3"),
    (3, 6, "3-6"),
    (6, 9, "6-9"),
    (9, 10, "9-10"),
    (10, 12, "10-12"),
    (12, 14, "12-14"),
    (14, 16, "14-16"),
    (16, float('inf'), "16+")
]

# Rangos para Taxa èxit
rangos_taxa = [
    (0, 20, "0-20%"),
    (20, 40, "20-40%"),
    (40, 60, "40-60%"),
    (60, 80, "60-80%"),
    (80, 100, "80-100%"),
    (100, 101, "100%")
]

def procesar_porcentaje(porcentaje_str):
    """Convierte string de porcentaje a valor numérico"""
    if not porcentaje_str:
        return None
    try:
        return float(porcentaje_str.replace('%', '').strip())
    except ValueError:
        return None

# Diccionario principal para almacenar los conteos
conteos = {campo: defaultdict(int) for campo in campos}

with open(csv_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    
    # Procesar cada fila
    for row in csv_reader:
        for campo in campos:
            if campo == "Nota d'accés (preinscripció)":
                # Procesamiento especial para notas
                try:
                    nota_str = row[campo].replace(',', '.').strip()
                    nota = float(nota_str) if nota_str else 0
                    
                    # Asignar al rango correspondiente
                    for rango_min, rango_max, etiqueta in rangos_notas:
                        if rango_min <= nota < rango_max:
                            conteos[campo][etiqueta] += 1
                            break
                except (ValueError, KeyError):
                    conteos[campo]["Datos no válidos"] += 1
            
            elif campo == "Taxa èxit":
                # Procesamiento especial para taxa èxit
                taxa_val = procesar_porcentaje(row.get(campo, ''))
                
                if taxa_val is not None:
                    if taxa_val == 100:
                        conteos[campo]["100%"] += 1
                    else:
                        for rango_min, rango_max, etiqueta in rangos_taxa:
                            if rango_min <= taxa_val < rango_max:
                                conteos[campo][etiqueta] += 1
                                break
                else:
                    conteos[campo]["Datos no válidos"] += 1
            
            else:
                # Procesamiento normal para otros campos
                valor = row[campo].strip() if campo in row else ''
                if valor:
                    conteos[campo][valor] += 1

# Función para mostrar resultados ordenados
def mostrar_resultados(conteos):
    for campo, valores in conteos.items():
        print(f"\n--- {campo} ---")
        if campo == "Nota d'accés (preinscripció)":
            # Orden especial para notas
            for rango in rangos_notas:
                etiqueta = rango[2]
                print(f"{etiqueta}: {valores.get(etiqueta, 0)}")
            if "Datos no válidos" in valores:
                print(f"Datos no válidos: {valores['Datos no válidos']}")
        
        elif campo == "Taxa èxit":
            # Orden especial para taxa èxit
            for rango in rangos_taxa:
                etiqueta = rango[2]
                print(f"{etiqueta}: {valores.get(etiqueta, 0)}")
            if "Datos no válidos" in valores:
                print(f"Datos no válidos: {valores['Datos no válidos']}")
        
        else:
            # Orden alfabético para otros campos
            for valor, cantidad in sorted(valores.items()):
                print(f"{valor}: {cantidad}")

# Mostrar resultados
mostrar_resultados(conteos)


#si volem guardar el resultat en un fitxer
"""
with open('resultados_agrupados_completos.txt', 'w', encoding='utf-8') as out_file:
    for campo, valores in conteos.items():
        out_file.write(f"\n--- {campo} ---\n")
        if campo == "Nota d'accés (preinscripció)":
            for rango in rangos_notas:
                etiqueta = rango[2]
                out_file.write(f"{etiqueta}: {valores.get(etiqueta, 0)}\n")
            if "Datos no válidos" in valores:
                out_file.write(f"Datos no válidos: {valores['Datos no válidos']}\n")
        
        elif campo == "Taxa èxit":
            for rango in rangos_taxa:
                etiqueta = rango[2]
                out_file.write(f"{etiqueta}: {valores.get(etiqueta, 0)}\n")
            if "Datos no válidos" in valores:
                out_file.write(f"Datos no válidos: {valores['Datos no válidos']}\n")
        
        else:
            for valor, cantidad in sorted(valores.items()):
                out_file.write(f"{valor}: {cantidad}\n")
print("Resultados guardados en 'resultados_agrupados_completos.txt'")"
"""
