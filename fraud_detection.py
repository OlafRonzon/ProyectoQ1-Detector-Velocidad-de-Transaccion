
import math
import datetime
import csv

def ingerir_datos_reales(ruta_archivo):
    print("⏳ Ingestando datos crudos desde Kaggle...")
    dicc_limpio = {"Kaggle_Data": []} 
    

    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        
        contador = 0
        for fila in lector:
            transaccion = {
                "id_usuario": fila["cc_num"],
                "hora": fila["trans_date_trans_time"]
            }
            dicc_limpio["Kaggle_Data"].append(transaccion)
            
            contador += 1
            if contador == 1000000:
                break
                
    print(f"Se cargaron {contador} transacciones exitosamente.")
    return dicc_limpio

def recibir_datos(datos_crudos: list) -> list:
    datos_aprobados = []
    for i in datos_crudos:
        if "id_usuario" in i and "monto" in i and "hora" in i:       
            monto_texto = str(i["monto"])

            if "$" in monto_texto:
                monto_texto = monto_texto.replace("$","")
                try:
                    i["monto"] = float(monto_texto)
                except ValueError:
                    continue
            else:
                try:
                    i["monto"] = float(monto_texto)
                    
                except  ValueError:
                    continue
                
            if i["monto"] <= 0:
                continue
            
            if ":" in str(i["hora"]):
                datos_aprobados.append(i)
            else:
                continue
    
    return datos_aprobados


def agrupador_ids(datos_limpios:list) -> dict:
    dicc_limpio = {}   
    for i in datos_limpios:
        id_actual = i["id_usuario"]
        if id_actual in dicc_limpio:
            dicc_limpio[id_actual].append(i)
        else:
            dicc_limpio[id_actual] = [i]
            
    return dicc_limpio  
    

def registro_velocidad(dicc_limpio:dict) -> dict:
    id_tiempo = {}

    for k,v in dicc_limpio.items():
        for i in v:
            id_actual = i["id_usuario"]
            if id_actual in id_tiempo:
                id_tiempo[id_actual].append(i["hora"])
            else:
                id_tiempo[id_actual] = [i["hora"]] 


    id_tiempo_transformado = {}
    for k,v in id_tiempo.items():
        for i in v:
            fecha_texto = i  
            tiempo_entero = datetime.datetime.strptime(fecha_texto, "%Y-%m-%d %H:%M:%S").timestamp()
            
            if k in id_tiempo_transformado:
                id_tiempo_transformado[k].append(tiempo_entero)
            else:
                id_tiempo_transformado[k] = [tiempo_entero]
            
    for lista_tiempo in id_tiempo_transformado.values():
        lista_tiempo.sort()

    cuentas_bloqueadas = {}
    revision_manual = {}
    for id_usuario,lista in id_tiempo_transformado.items():

        indice_ancla = 0

        for indice_actual in range(len(lista)):

            tiempo_actual = lista[indice_actual]
            tiempo_ancla = lista[indice_ancla]

            while (tiempo_actual - tiempo_ancla) > 300:
                indice_ancla += 1
                tiempo_ancla = lista[indice_ancla]
                  
            transacciones = (indice_actual - indice_ancla) + 1

            if transacciones >= 3:
                lista_antes_evento = lista[: indice_actual]
                suma = sum(lista_antes_evento)
                longitud = len(lista_antes_evento)
                promedio = suma/longitud
                sumatoria = 0
                for i in lista_antes_evento:
                    cuadrado = (i - promedio)**2
                    sumatoria += cuadrado
                varianza = sumatoria/(longitud-1)
                desviacion_estandar = math.sqrt(varianza)
                if desviacion_estandar == 0:
                    desviacion_estandar = 0.0001
                z_score = (tiempo_actual - promedio)/desviacion_estandar

                if z_score > 2 or z_score < -2:
                    cuentas_bloqueadas[id_usuario] = "Bloqueada"
                    break
                else:
                    if id_usuario in revision_manual:
                        revision_manual[id_usuario] += 1
                    else:
                        revision_manual[id_usuario] = 1
                    continue

    return cuentas_bloqueadas, revision_manual
    


    # --- PIPELINE PRINCIPAL ---
# --- EJECUCIÓN DEL PROGRAMA ---
if __name__ == "__main__":
    datos_Kaggle = ingerir_datos_reales("fraude_basedatos.csv")
    bloqueadas, revision = registro_velocidad(datos_Kaggle)
    print(f"🚨 Tarjetas Bloqueadas (Fraude Detectado): {len(bloqueadas)}")
    print(f"⚠️ Tarjetas en Revisión Manual: {len(revision)}")
              
