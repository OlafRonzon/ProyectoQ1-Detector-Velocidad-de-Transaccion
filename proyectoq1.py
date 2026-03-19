# Archivo: detector_main.py


def recibir_datos(datos_crudos: list) -> list:
    #TODO: Crear una lista vacía que se denomiina datos aprobados
    datos_aprobados = []
    #TODO: hacer un bucle para revisar cada diccionario
    for i in datos_crudos:
        if "ids" in i and "monto" in i and "hora" in i:       
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
    #TODO: Asignar numero de transacciones por tiempo a su id
    
    pass

def identificador_anomalias(datos_ordenados:dict) -> dict:
    #TODO: Logica booleana para separar clientes normales de clientes sospechosos
    #TODO: productir una lista simple con los clientes a investigar
    #TODO: a partir de la lista, sumar el número de anomalías y el monto total de las transacciones ocurridas durante la ventana
    #TODO: producir un diccionario con ID, monto total y número de transacciones ocurridas dentro de la ventana deslizante

    pass

if __name__ == "__main__":
    # --- PIPELINE PRINCIPAL ---
    if __name__ == "__main__":
    # Datos de prueba con basura (monto con $, hora mal, llaves faltantes)
        transacciones_sucias = [
            {"ids": "User1", "monto": "$100.50", "hora": "10:30"},
            {"ids": "User2", "monto": "50.00", "hora": "1115"}, # Mal: sin ":"
            {"monto": "20.0"}, # Mal: sin "ids" ni "hora"
            {"ids": "User3", "monto": "Gratis", "hora": "12:00"} # Mal: no es número
        ]
    
        resultado = recibir_datos(transacciones_sucias)
        print(f"Transacciones aprobadas: {len(resultado)}")
        print(resultado)
              
