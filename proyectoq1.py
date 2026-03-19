# Archivo: detector_main.py


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
    

def identificador_anomalias(datos_ordenados:dict) -> dict:
    #TODO: Logica booleana para separar clientes normales de clientes sospechosos
    #TODO: productir una lista simple con los clientes a investigar
    #TODO: a partir de la lista, sumar el número de anomalías y el monto total de las transacciones ocurridas durante la ventana
    #TODO: producir un diccionario con ID, monto total y número de transacciones ocurridas dentro de la ventana deslizante

    pass


    # --- PIPELINE PRINCIPAL ---
if __name__ == "__main__":
    # Datos de prueba con basura (monto con $, hora mal, llaves faltantes)
    transacciones_sucias = [
        {"id_usuario": "User1", "monto": "$100.50", "hora": "10:30"},
        {"id_usuario": "User2", "monto": "50.00", "hora": "1115"}, # Mal: sin ":"
        {"monto": "20.0"}, # Mal: sin "ids" ni "hora"
        {"id_usuario": "User3", "monto": "Gratis", "hora": "12:00"} # Mal: no es número
    ]
    
    resultado = recibir_datos(transacciones_sucias)
    print(f"Transacciones aprobadas: {len(resultado)}")
    print(resultado)
    agrupados = agrupador_ids(resultado)
    print(f"Agrupados: {agrupados}")
    
              
