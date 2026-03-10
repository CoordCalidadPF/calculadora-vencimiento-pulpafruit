import pandas as pd
import json
import re

archivo = "datos/productos.xlsx"

df = pd.read_excel(archivo)

def limpiar(texto):
    t = str(texto if pd.notna(texto) else "").strip()
    t = t.replace("\n"," ").replace("\r"," ")
    t = re.sub(r"\s+"," ",t)
    t = t.replace('"','\\"')
    return t

def interpretar_vida_util(texto):
    texto = limpiar(texto).upper()

    if "MES" in texto:
        n = re.search(r"\d+",texto)
        return int(n.group()),"meses"

    if "AÑO" in texto or "ANO" in texto:
        n = re.search(r"\d+",texto)
        return int(n.group())*12,"meses"

    if "DIA" in texto:
        n = re.search(r"\d+",texto)
        return int(n.group()),"dias"

    return None,None

materiales = {}

for _,row in df.iterrows():

    codigo = limpiar(row["CODIGO"])
    nombre = limpiar(row["NOMBRE"])
    vida,unidad = interpretar_vida_util(row["VIDA_UTIL"])

    if codigo and nombre and vida:
        materiales[codigo] = {
            "nombre": nombre,
            "vidaUtil": vida,
            "unidadVidaUtil": unidad
        }

with open("materiales.json","w",encoding="utf8") as f:
    json.dump(materiales,f,ensure_ascii=False,indent=2)

with open("materiales.js","w",encoding="utf8") as f:
    f.write("window.MATERIALES = ")
    json.dump(materiales,f,ensure_ascii=False,indent=2)
    f.write(";\nwindow.materiales = window.MATERIALES;\n")

print("Archivos generados correctamente")
