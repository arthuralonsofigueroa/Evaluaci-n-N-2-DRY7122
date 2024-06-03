import requests

def calcular_ruta(ciudad_origen, ciudad_destino):
    url_geocode = "https://graphhopper.com/api/1/geocode"
    url_ruta = "https://graphhopper.com/api/1/route"
    api_key = "a5bfd8b7-c183-42e4-bbe4-5cd51468f3b0"  # Reemplaza con tu propia clave API
   
    # Obtener coordenadas de las ciudades
    params = {"q": ciudad_origen, "limit": "1", "key": api_key}
    respuesta = requests.get(url_geocode, params=params)
    coordenadas_origen = respuesta.json()["hits"][0]["point"] if respuesta.status_code == 200 else None
   
    params["q"] = ciudad_destino
    respuesta = requests.get(url_geocode, params=params)
    coordenadas_destino = respuesta.json()["hits"][0]["point"] if respuesta.status_code == 200 else None
   
    # Calcular la ruta si se obtuvieron las coordenadas
    if coordenadas_origen and coordenadas_destino:
        params = {
            "point": [f"{coordenadas_origen['lat']},{coordenadas_origen['lng']}", f"{coordenadas_destino['lat']},{coordenadas_destino['lng']}"],
            "key": api_key
        }
        respuesta = requests.get(url_ruta, params=params)
        if respuesta.status_code == 200:
            datos_ruta = respuesta.json()["paths"][0]
            distancia_km = datos_ruta["distance"] / 1000
            duracion_segundos = datos_ruta["time"]
            combustible_litros = distancia_km / 10  # Suponiendo consumo de 10 km por litro
            return distancia_km, duracion_segundos, combustible_litros
        else:
            print(f"No se pudo calcular la ruta entre {ciudad_origen} y {ciudad_destino}.")
    else:
        print(f"No se pudieron obtener las coordenadas para una o ambas ciudades.")

# Ejemplo de uso
ciudad_origen = "Santiago"
ciudad_destino = "Puerto Varas"
distancia, duracion, combustible = calcular_ruta(ciudad_origen, ciudad_destino)
if distancia is not None:
    print(f"Distancia entre {ciudad_origen} y {ciudad_destino}: {distancia:.2f} km")
    horas = duracion // 3600
    minutos = (duracion % 3600) // 60
    segundos = duracion % 60
    print(f"Duración del viaje: {horas:.0f} horas {minutos:.0f} minutos {segundos:.0f} segundos")
    print(f"Combustible requerido para el viaje: {combustible:.2f} litros")
