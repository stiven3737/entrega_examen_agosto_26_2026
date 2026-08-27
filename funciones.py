# funciones.py

def registrar_ingreso(vehiculos):
    """
    1. registrar_ingreso(vehiculos)
    Registra vehículos uno a uno hasta completar 15 ingresos o hasta que el usuario decida terminar.
    No se permite repetir una placa que esté activa. Retorna la lista actualizada.
    """
    print("\n--- REGISTRO DE INGRESOS ---")
    
    # Validar si ya se alcanzó el límite máximo de registros totales permitidos (15)
    if len(vehiculos) >= 15:
        print("Se ha alcanzado el límite máximo de 15 registros para la jornada.")
        return vehiculos

    while len(vehiculos) < 15:
        # Validar cupo simultáneo antes de dejar ingresar uno nuevo (Capacidad máxima: 10)
        if not validar_cupo(vehiculos, 10):
            print("¡Atención! El parqueadero ha alcanzado su capacidad máxima simultánea (10 vehículos activos). No se pueden registrar más ingresos hasta que se libere espacio.")
            break

        placa = input("Ingrese la placa del vehículo (o presione Enter para terminar): ").strip().upper()
        if placa == "":
            break

        # Verificar si la placa ya está registrada y activa
        placa_repetida = False
        for v in vehiculos:
            if v["placa"] == placa and v["activo"]:
                placa_repetida = True
                break

        if placa_repetida:
            print(f"Error: El vehículo con placa {placa} ya se encuentra activo en el parqueadero.")
            continue

        # Solicitar tipo de vehículo con validación
        tipo = ""
        while tipo not in ["Moto", "Carro", "Camioneta"]:
            t_input = input("Ingrese el tipo (Moto, Carro, Camioneta): ").strip().capitalize()
            if t_input in ["Moto", "Carro", "Camioneta"]:
                tipo = t_input
            else:
                print("Tipo inválido. Intente nuevamente.")

        # Solicitar categoría con validación
        categoria = ""
        while categoria not in ["Asistente", "Proveedor", "Personal"]:
            c_input = input("Ingrese la categoría (Asistente, Proveedor, Personal): ").strip().capitalize()
            if c_input in ["Asistente", "Proveedor", "Personal"]:
                categoria = c_input
            else:
                print("Categoría inválida. Intente nuevamente.")

        # Solicitar hora de entrada (entera entre 6 y 20)
        hora_entrada = -1
        while hora_entrada < 6 or hora_entrada > 20:
            try:
                hora_entrada = int(input("Ingrese la hora de entrada (entera entre 6 y 20): "))
                if hora_entrada < 6 or hora_entrada > 20:
                    print("La hora debe estar entre 6 y 20.")
            except ValueError:
                print("Por favor, ingrese un número entero válido.")

        # Crear el diccionario del vehículo dentro del ciclo de n iteraciones
        nuevo_vehiculo = {
            "placa": placa,
            "tipo": tipo,
            "categoria": categoria,
            "hora_entrada": hora_entrada,
            "hora_salida": 0,
            "valor_pagado": 0,
            "activo": True
        }

        # Agregar el vehículo a la lista general
        vehiculos.append(nuevo_vehiculo)
        print(f"Vehículo con placa {placa} registrado exitosamente.\n")

        if len(vehiculos) >= 15:
            print("Se ha alcanzado el límite total de 15 ingresos.")
            break
        
        continuar = input("¿Desea registrar otro vehículo? (s/n): ").strip().lower()
        if continuar != 's':
            break

    return vehiculos


def validar_cupo(vehiculos, capacidad):
    """
    2. validar_cupo(vehiculos, capacidad)
    Contar cuántos vehículos tienen activo=True y determinar si aún existe espacio.
    La capacidad máxima será de 10 vehículos simultáneos.
    Retorna True si existe cupo y False en caso contrario.
    """
    activos_count = 0
    for v in vehiculos:
        if v["activo"]:
            activos_count += 1
            
    return activos_count < capacidad


def calcular_horas(hora_entrada, hora_salida):
    """
    3. calcular_horas(hora_entrada, hora_salida)
    Calcular las horas de permanencia. Si la diferencia es menor que 1, se cobra 1 hora.
    La salida debe ser mayor que la entrada. Retorna la cantidad de horas o -1 si los datos son inválidos.
    """
    if hora_salida <= hora_entrada:
        return -1
    
    diferencia = hora_salida - hora_entrada
    if diferencia < 1:
        return 1
    
    return diferencia


def calcular_tarifa(tipo, categoria, horas):
    """
    4. calcular_tarifa(tipo, categoria, horas)
    Aplicar tarifa por hora: Moto $2.000, Carro $3.500, Camioneta $5.000.
    El personal tiene 100% de descuento y los proveedores 20% de descuento. Retorna el valor final.
    """
    tarifa_base_por_hora = 0
    if tipo == "Moto":
        tarifa_base_por_hora = 2000
    elif tipo == "Carro":
        tarifa_base_por_hora = 3500
    elif tipo == "Camioneta":
        tarifa_base_por_hora = 5000

    subtotal = tarifa_base_por_hora * horas

    # Aplicar condiciones múltiples para obtener la tarifa pagada según categoría
    if categoria == "Personal":
        valor_final = 0.0
    elif categoria == "Proveedor":
        valor_final = subtotal * 0.80  # 20% de descuento (pagan el 80%)
    else:  # Asistente
        valor_final = float(subtotal)

    return valor_final


def registrar_salida(vehiculos, placa):
    """
    5. registrar_salida(vehiculos, placa)
    Buscar la placa activa, solicitar hora de salida, calcular permanencia y tarifa,
    actualizar hora_salida, valor_pagado y activo=False.
    Retorna True si la salida fue registrada y False si la placa no existe o los datos son inválidos.
    """
    vehiculo_encontrado = None
    for v in vehiculos:
        if v["placa"] == placa and v["activo"]:
            vehiculo_encontrado = v
            break

    if not vehiculo_encontrado:
        print(f"La placa {placa} no se encuentra activa en el parqueadero.")
        return False

    try:
        hora_salida = int(input(f"Ingrese la hora de salida para la placa {placa} (Entrada fue a las {vehiculo_encontrado['hora_entrada']}h): "))
    except ValueError:
        print("Hora inválida.")
        return False

    horas = calcular_horas(vehiculo_encontrado["hora_entrada"], hora_salida)
    if horas == -1:
        print("Error: La hora de salida debe ser estrictamente mayor que la hora de entrada.")
        return False

    valor = calcular_tarifa(vehiculo_encontrado["tipo"], vehiculo_encontrado["categoria"], horas)

    # Actualizar los campos del diccionario
    vehiculo_encontrado["hora_salida"] = hora_salida
    vehiculo_encontrado["valor_pagado"] = valor
    vehiculo_encontrado["activo"] = False

    print(f"Salida registrada con éxito. Tiempo cobrado: {horas} hora(s). Total a pagar: ${valor:,.0f}")
    return True


def generar_cierre(vehiculos):
    """
    6. generar_cierre(vehiculos)
    Mostrar total de vehículos registrados, vehículos aún activos, ingresos recaudados,
    promedio de horas de los vehículos que ya salieron y tipo de vehículo que más ingresó.
    Utiliza contadores, ciclos y condicionales (sin librerías externas ni max con key).
    """
    print("\n==========================================")
    print("         REPORTE DE CIERRE DE JORNADA     ")
    print("==========================================")

    total_registrados = len(vehiculos)
    vehiculos_activos = 0
    ingresos_recaudados = 0.0
    
    # Variables para el cálculo del promedio de horas (Suma y conteo usando ciclos)
    suma_horas = 0
    contador_salidos = 0

    # Contadores independientes para los tipos de vehículos
    cont_motos = 0
    cont_carros = 0
    cont_camionetas = 0

    for v in vehiculos:
        if v["activo"]:
            vehiculos_activos += 1
        else:
            ingresos_recaudados += v["valor_pagado"]
            h = calcular_horas(v["hora_entrada"], v["hora_salida"])
            if h != -1:
                suma_horas += h
                contador_salidos += 1

        # Acumular conteos por tipo de vehículo
        if v["tipo"] == "Moto":
            cont_motos += 1
        elif v["tipo"] == "Carro":
            cont_carros += 1
        elif v["tipo"] == "Camioneta":
            cont_camionetas += 1

    # Calcular promedio de horas (Suma total / Cantidad de elementos)
    promedio_horas = 0.0
    if contador_salidos > 0:
        promedio_horas = suma_horas / contador_salidos

    # Determinar el tipo más frecuente mediante condicionales estrictos (sin max ni Counter)
    tipo_frecuente = "Ninguno"
    if total_registrados > 0:
        if cont_motos >= cont_carros and cont_motos >= cont_camionetas:
            tipo_frecuente = "Moto"
        if cont_carros >= cont_motos and cont_carros >= cont_camionetas:
            tipo_frecuente = "Carro"
        if cont_camionetas >= cont_motos and cont_camionetas >= cont_carros:
            tipo_frecuente = "Camioneta"
        
        if cont_motos == cont_carros == cont_camionetas:
            tipo_frecuente = "Empate entre tipos"

    # Salidas en consola claras para interpretar el resultado del reporte
    print(f"* Total de vehículos registrados : {total_registrados}")
    print(f"* Vehículos aún activos          : {vehiculos_activos}")
    print(f"* Ingresos totales recaudados    : ${ingresos_recaudados:,.0f}")
    print(f"* Promedio de horas (salidos)    : {promedio_horas:.1f} horas")
    print(f"* Tipo de vehículo más frecuente : {tipo_frecuente} (Motos: {cont_motos}, Carros: {cont_carros}, Camionetas: {cont_camionetas})")
    print("==========================================")
    print("Finaliza programa y nos genera reporte que tuvimos en la feria.")