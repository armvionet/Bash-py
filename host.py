
import requests
import sys
import time
from requests.exceptions import RequestException

# Función para testear un dominio individual
def test_domain(domain):
    # Asegurar que el dominio tiene el formato correcto
    if not domain.startswith('http'):
        domain = f'https://{domain}'
    
    try:
        # Realizar petición GET con timeout de 8 segundos y sin verificar SSL
        response = requests.get(
            domain, 
            timeout=8, 
            verify=False, 
            allow_redirects=False,
            headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0'}
        )
        
        status_code = response.status_code
        server = response.headers.get('Server', 'No especificado')
        content_type = response.headers.get('Content-Type', 'No especificado')
        
        # Comprobar si hay redirección
        if 300 <= status_code < 400:
            redirect_url = response.headers.get('Location', 'No especificado')
            result = f"{domain}\n  Estado: {status_code}\n  Redirección: {redirect_url}\n  Servidor: {server}"
        else:
            result = f"{domain}\n  Estado: {status_code}\n  Tipo: {content_type[:50]}\n  Servidor: {server}"
        
        return result
        
    except RequestException as e:
        return f"{domain}\n  Error: {str(e)}"

def main():
    # Deshabilitar advertencias SSL
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except ImportError:
        pass
    
    # Comprobar si se proporcionó un archivo como argumento
    if len(sys.argv) != 2:
        print("Uso: python test_domains.py archivo_dominios.txt")
        sys.exit(1)
    
    # Leer dominios del archivo
    try:
        with open(sys.argv[1], 'r') as file:
            domains = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {sys.argv[1]}")
        sys.exit(1)
    
    total = len(domains)
    print(f"Testeando {total} dominios...")
    
    # Procesar dominios uno por uno (evitamos multithreading para mejor compatibilidad con Termux)
    results = []
    for i, domain in enumerate(domains):
        print(f"[{i+1}/{total}] Testeando: {domain}")
        result = test_domain(domain)
        results.append(result)
        print("✓")
        # Pequeña pausa para no sobrecargar recursos
        time.sleep(0.5)
    
    # Guardar resultados en un archivo
    output_file = "resultados_dominios.txt"
    with open(output_file, 'w') as file:
        for result in results:
            file.write(result + "\n\n")
    
    print(f"\nTesteo completado. Resultados guardados en {output_file}")
    
    # Mostrar resumen en pantalla
    print("\n--- RESUMEN DE RESULTADOS ---")
    for result in results:
        print("\n" + result)

if __name__ == "__main__":
    main()
