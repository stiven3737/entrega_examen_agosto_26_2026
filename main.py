# main.py
from funciones import registrar_ingreso, registrar_salida, generar_cierre

def main():
    # Lista principal donde se almacenarán los diccionarios de vehículos
    vehiculos = []
    
    while True:
        print("\n=== SISTEMA DE CONTROL DE ESTACIONAMIENTO ===")
        print("1. Registrar Ingreso de Vehículo")
        print("2. Registrar Salida de Vehículo")
        print("3. Generar Cierre de Jornada y Reporte")
        print("4. Salir del Sistema")
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            vehiculos = registrar_ingreso(vehiculos)
        elif opcion == "2":
            if not vehiculos:
                print("No hay vehículos registrados en el sistema todavía.")
                continue
            placa_buscar = input("Ingrese la placa del vehículo a retirar: ").strip().upper()
            registrar_salida(vehiculos, placa_buscar)
        elif opcion == "3":
            generar_cierre(vehiculos)
        elif opcion == "4":
            print("Saliendo del sistema. ¡Mucho éxito con tu examen!")
            break
        else:
            print("Opción inválida. Por favor, elija un número entre 1 y 4.")

if __name__ == "__main__":
    main()