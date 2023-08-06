from oauth2client import crypt, service_account, GOOGLE_TOKEN_URI, GOOGLE_REVOKE_URI
from googleapiclient.discovery import build
from typing import Dict, List
import pandas as pd

class SheetsUtils:
    def __init__(self, project_id: str, client_id:str, client_email:str, client_x509_cert_url:str, private_key_id: str, private_key: str) -> None:
        """Construtor de Autentificação na Service Account do Google Drive

        Args:
            project_id (str)
            client_id (str)
            client_email (str)
            client_x509_cert_url (str)
            private_key_id (str)
            private_key (str)
        """
        
        # Iniciando autentificacao na API do Google Drive
        drive_credentials = self.__get_drive_credentials(project_id, client_id, client_email, client_x509_cert_url, private_key_id, private_key)
        service_account_email = drive_credentials["client_email"]
        private_key_pkcs8_pem = drive_credentials["private_key"]
        client_id = drive_credentials["client_id"]
        token_uri = drive_credentials.get("token_uri", GOOGLE_TOKEN_URI)
        revoke_uri = drive_credentials.get("revoke_uri", GOOGLE_REVOKE_URI)

        signer = crypt.Signer.from_string(private_key_pkcs8_pem)
        credentials = service_account.ServiceAccountCredentials(
            service_account_email,
            signer,
            scopes="",
            private_key_id=private_key_id,
            client_id=client_id,
            token_uri=token_uri,
            revoke_uri=revoke_uri,
        )
        credentials._private_key_pkcs8_pem = private_key_pkcs8_pem

        self.service = build("sheets", "v4", credentials=credentials)
    
    def __get_drive_credentials(self, project_id: str, client_id:str, client_email:str, client_x509_cert_url:str, private_key_id: str, private_key: str) -> Dict[str, str]:
        """Função para organizar as credenciais do serviço Google

        Args:
            project_id (str)
            client_id (str)
            client_email (str)
            client_x509_cert_url (str)
            private_key_id (str)
            private_key (str)

        Returns:
            Dict[str, str]: Credenciais do serviço Google organizadas no formato de dicionário
        """
        drive_credentials = {
            "type": "service_account",
            "project_id": project_id,
            "client_id": client_id,
            "client_email": client_email,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": client_x509_cert_url,
            "private_key_id": private_key_id,
            "private_key": private_key,
        }

        return drive_credentials
    
    def read_spreadsheet(self, spreadsheet_id : str, spreadsheet_range: str) -> pd.DataFrame:
        """Função para ler um spreadsheet do Google e transformá-lo em um Dataframe

        Args:
            spreadsheet_id (str): ID do spreadsheet do Google Drive.
            spreadsheet_range (str): Range desejado para a leitura (A1:Z).

        Returns:
            DataFrame: Dataframe referente ao range selecionado do spreadsheet correspondente
        """
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId= spreadsheet_id, range=spreadsheet_range).execute()
        data = result.get('values')
        df = pd.DataFrame(data)
        df.columns = df.iloc[0]
        df = df[1:]
        df = df.apply(lambda x: x.str.strip())

        return df   

    def write_spreadhseet(self, spreadsheet_id: str, spreadsheet_range:str, values: List) -> Dict:
        """Função para sobrescrever em um spreadsheet do Google

        Args:
            spreadsheet_id (str): ID do spreadsheet do Google Drive.
            spreadsheet_range (str): Range desejado para escrita (A1).
            values (List): Lista contendo os valores a serem escritas nas Linhas e Células correspondentes

        Returns:
            Dict: Resposta da requisição de escrita.
        """
        body = {'values': values}
        request = self.service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=spreadsheet_range, valueInputOption='USER_ENTERED', body=body).execute()
        return request











