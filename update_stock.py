import pandas as pd
from woocommerce import API
#import ospip
import logging
from datetime import datetime

# Configuración del logging
log_filename = f"stock_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración de la API de WooCommerce
wcapi = API(
    url="https://midomind.us/",
    consumer_key="ck_consumerkey",
    consumer_secret="cs_consumer",
    version="wc/v3"
)

# Ruta al archivo Excel
excel_path = r"paht in your pc"

# Leer el archivo Excel
df = pd.read_excel(excel_path)

def update_product_stock(sku, new_stock):
    page = 1
    while True:
        products = wcapi.get("products", params={"sku": sku, "page": page, "per_page": 100}).json()
        
        if not products:
            break
        
        for product in products:
            if product['sku'] == sku:
                product_id = product['id']
                data = {"stock_quantity": int(new_stock)}
                
                response = wcapi.put(f"products/{product_id}", data)
                
                if response.status_code == 200:
                    logging.info(f"Stock actualizado para SKU {sku}: {new_stock}")
                    return True
                else:
                    logging.error(f"Error actualizando SKU {sku}: {response.text}")
                    return False
        
        page += 1
    
    logging.warning(f"Producto con SKU {sku} no encontrado")
    return False

# Contador para seguimiento del progreso
total_productos = len(df)
productos_actualizados = 0

# Iterar sobre las filas del DataFrame
for index, row in df.iterrows():
    sku = row['SKU']
    new_stock = row['Initial number in stock']
    
    if update_product_stock(sku, new_stock):
        productos_actualizados += 1
    
    # Mostrar progreso
    if (index + 1) % 10 == 0 or index == total_productos - 1:
        print(f"Progreso: {index + 1}/{total_productos} productos procesados")

print(f"\nActualización de stock completada. {productos_actualizados}/{total_productos} productos actualizados.")
logging.info(f"Actualización de stock completada. {productos_actualizados}/{total_productos} productos actualizados.")