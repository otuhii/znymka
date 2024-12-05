# Class to handle Google Drive operations for photo storage
# Requires:
# 1. credentials.json - OAuth client configuration from Google Cloud Console for now its my email there but in future it would be good to just create 
# new email for this site or actually on production buy decent db just to not to be broke boys(olegtyhii81079@gmail.com)
# 2. token.json - Generated after first user authentication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import io
import os

class GoogleDriveStorage:
    # Define access scope - 'drive.file' allows access only to files created by the app
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    


    ##################                        so it is just authentication                         ####################
    def __init__(self, credentials_path='static/credentials.json', token_path='token.json'):
        """Initialize Drive service with credentials"""
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._get_drive_service()
    

    
    def _get_drive_service(self):
        """Set up authentication and create Drive service
        1. Check for existing token
        2. If no token/invalid, start OAuth flow
        3. Save new token for future use"""
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        if not creds or not creds.valid:
            # Start OAuth flow if no valid credentials
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
            creds = flow.run_local_server(port=0)
            # Save token for future runs
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        return build('drive', 'v3', credentials=creds)
    
    ##################################################################################################





    def upload_photo(self, file_path, filename=None):
        """Upload photo to Drive and return file ID for database storage
        Args:
            file_path: Path to local file
            filename: Optional custom filename in Drive"""
        if not filename:
            filename = os.path.basename(file_path)
            
        file_metadata = {'name': filename}
        media = MediaFileUpload(file_path, mimetype='image/jpeg', resumable=True)
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        return file.get('id')
    
    def get_photo(self, file_id):
        """Download photo from Drive using file ID
        Returns binary file data"""
        request = self.service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        
        return file.getvalue()
    
    def delete_photo(self, file_id):
        """Remove photo from Drive using file ID"""
        self.service.files().delete(fileId=file_id).execute()