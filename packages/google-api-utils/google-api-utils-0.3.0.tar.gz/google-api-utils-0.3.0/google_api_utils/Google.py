from oauth2client import crypt, service_account, GOOGLE_TOKEN_URI, GOOGLE_REVOKE_URI
from googleapiclient.discovery import build
from typing import Dict, List
import pandas as pd

class Drive:
    def __init__(self, project_id: str, client_id:str, client_email:str, client_x509_cert_url:str, private_key_id: str, private_key: str) -> None:
        """Construtor de Autentificação na Service Account do Google Drive

        Args:
            private_key_id (str): private key id da API do Google
            private_key (str): private key da API do Google

        Returns:
            [Object]: Instância autenticada do DriveUtils
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

        # Instância do Serviço Google criada
        self.service = build("drive", "v3", credentials=credentials)

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
    
    def list_files(self, folder_id: str)-> List:
        """Lista os metadados dos arquivos dentro de uma pasta no Google Drive

        Args:
            folder_id [str]: ID da pasta onde estão os arquivos de interesse.

        Returns:
            [list]: Lista com dicionários contendo os metadados dos arquivos listados
        """
        
        # Montando a Query de Listagem
        query = f"parents = '{folder_id}'"

        response = self.service.files().list(q=query).execute()
        files = response.get("files")

        # Coletando todos os arquivos da pasta
        nextPageToken = response.get("nextPageToken")
        while nextPageToken:
            response = self.service.files().list(q=query).execute()
            files.extend(response.get("files"))
            nextPageToken = response.get("nextPageToken")

        return files

    def create_folder(self, parent_id:str, folder_name:str)->str:
        """Cria uma pasta no drive, caso ela não exista.

        Args:
            parent_id (str): ID da pasta onde a nova pasta será criada.
            folder_name (str): Nome da nova pasta criada.

        Returns:
            [str]: ID da nova pasta criada.
        """
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and parents='{parent_id}'"

        folders = (self.service.files().list(q=query, spaces="drive").execute().get("files"))

        if not folders:
            # Caso a pasta não exista, cria a pasta
            file_metadata = {
                "name": folder_name,
                "parents": [parent_id],
                "mimeType": "application/vnd.google-apps.folder",
            }
            new_id = (
                self.service.files()
                .create(body=file_metadata, fields="id")
                .execute()["id"]
            )
        else:
            new_id = folders[0]["id"]
        return new_id

    def download_file(self, file_id: str, file_path: str) -> str:
        """Função para baixar localmente um arquivo do Drive

        Args:
            file_id (str): ID do arquivo de interesse.
            file_path (str): Caminho local onde o arquivo será baixado.

        Returns:
            str: Caminho local onde o arquivo pode ser encontrado.
        """

        # Iniciando Download do arquivo
        file = self.service.files().get(fileId=file_id).execute()
        file_path = os.path.join(file_path, file['name'])
        
        requestDownload = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=requestDownload)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Progresso do Download: {0}".format(status.progress() *100))
        
        fh.seek(0)

        with open(file_path, 'wb') as f:
            f.write(fh.read())
            f.close()
        
        return file_path
        
    def read_file(self, file_id: str) -> io.BytesIO:
        """Função para ler um arquivo do Drive em memória.

        Args:
            file_id (str): ID do arquivo que se deseja baixar.

        Returns:
            io.BytesIO: Bytes do arquivo
        """

        requestDownload = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=requestDownload)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            print("Progresso do Download: {0}".format(status.progress() * 100))

        fh.seek(0)
        
        return fh

    def move_file(self, file_id: str, folder_id: str) -> None:
        """Função para mover arquivo isoladamente entre pastas do Drive

        Args:
            source_id (str, optional): ID da pasta fonte. Defaults to '1fqphePhddaDIbrjmexkCbEXjJQOsLeU5' (Pasta Input de ContratosSupply).
            target_id (str, optional): ID da pasta destino. Defaults to '1_44_GgXaWfeReQFMaCb9l8RSkzGitF8k' (Pasta Processados de ContratosSupply).
            mimeType (str, optional): Tipo dos arquivos manipulados. Defaults to 'application/pdf'.
        """
        # Removendo arquivo da pasta de origem
        file = self.service.files().get(fileId=file_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents"))

        # Transferindo arquivo para nova pasta
        file = (
            self.service.files()
            .update(
                fileId=file_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields="id, parents",
            )
            .execute()
        )

    def delete_file(self, file_id: str) -> None:
        """Deleta o arquivo do Drive

        Args:
            file_id (str): ID do arquivo que se deseja deletar.
        """
        file = self.service.files().get(fileId=file_id, fields="parents").execute()
        previous_parents = ",".join(file.get("parents"))
        
        file = (
            self.service.files()
            .update(
                fileId=file_id,
                removeParents=previous_parents,
                fields="id, parents",
            )
            .execute()
        )
    

class Sheets:
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











