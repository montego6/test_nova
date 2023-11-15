from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class CreateFileInDriveAPIView(APIView):
    def post(self, request):
        name = request.data["name"]
        content = request.data["data"]

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        file_metadata = {
            "name": name + ".txt",
            "parents": "root",
            "mimeType": "application/vnd.google-apps.file'",
        }

        with open(name + ".txt", "w") as file:
            file.write(content)

        media = MediaFileUpload(name + ".txt", mimetype="text/plain", resumable=True)

        service = build("drive", "v3", credentials=creds)
        file = service.files().create(body=file_metadata, media_body=media).execute()

        return Response({"result": file.get("id")}, status=status.HTTP_200_OK)
