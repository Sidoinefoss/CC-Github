"""
import os
import csv
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Chemin vers le fichier dans Microsoft Fabric
fabric_file_path = 'abfss://inno_sidoine_test@onelake.dfs.fabric.microsoft.com/DemoLakeHouse.Lakehouse/Files/bitcoin_data.csv'

# Fonction pour charger les données depuis un fichier dans Microsoft Fabric
def load_fabric_data_from_file(file_path):
    fabric_data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            fabric_data.append(row)
    return fabric_data

@app.get('export/https://onelake.dfs.fabric.microsoft.com/')
def export_microsoft_fabric():
    # Vérifier si le fichier existe dans Microsoft Fabric
    if not os.path.exists(fabric_file_path):
        raise HTTPException(status_code=404, detail="Le fichier n'existe pas dans Microsoft Fabric")

    # Charger les données depuis le fichier
    fabric_data = load_fabric_data_from_file(fabric_file_path)
    return fabric_data
"""
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()
# Informations d'authentification pour Microsoft Fabric
client_id = '8925603d-3d89-4c1e-bd76-45244e2f7002'
#client_secret = 'YOUR_CLIENT_SECRET'
#tenant_id = 'YOUR_TENANT_ID'
fabric_url = 'https://fabric.microsoft.com'

# Fonction pour obtenir un jeton d'accès auprès de Microsoft Fabric
def get_access_token():
    token_url = f'{fabric_url}/oauth2/token'
    payload = {
        'client_id': client_id,
        #'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'resource': fabric_url
    }
    response = requests.post(token_url, data=payload)
    access_token = response.json().get('access_token')
    return access_token

# Route protégée nécessitant une authentification avec Microsoft Fabric
@app.route('/protected-route')
def protected_route():
    access_token = get_access_token()
    if access_token:
        # Utilisez l'access_token pour effectuer des opérations protégées avec les API Fabric
        # Exemple : obtenir des données depuis Microsoft Fabric
        fabric_data = requests.get(fabric_url + '/api/data', headers={'Authorization': 'Bearer ' + access_token}).json()
        return {fabric_data}
    else:
        raise HTTPException(status_code=404, detail="Le fichier n'existe pas dans Microsoft Fabric")

if __name__ == '__main__':
    app.run(debug=True)
