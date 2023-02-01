from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import subprocess
import datetime
import os
import dateutil.parser
import sys

MAX_NB_BACKUP=3

backupFileName = datetime.datetime.now().strftime('%Y-%m-%d') + \
    '_previsionix.archive'
res = subprocess.call(['mongodump', '--db', 'previsionix',
                       '--gzip', '--archive'+'='+backupFileName])
if res != 0:
    print('Error while MongoDump', file=sys.stderr)
    exit(res)


gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)


backup = drive.CreateFile()
backup.SetContentFile(backupFileName)
backup.Upload()

file_list = drive.ListFile(
    {'q': "'root' in parents and trashed=false"}).GetList()
previous_dump = []
for file1 in file_list:
    if file1['title'].endswith('_previsionix.archive'):
        file1.FetchMetadata(fields='createdDate')
        previous_dump.append(file1)
if len(previous_dump) < 3:
    print('Less than 3 backup in drive')
    exit(0)
for i,dump in enumerate(sorted(previous_dump, key=lambda x: dateutil.parser.parse(x['createdDate']))):
    if i < len(previous_dump) - MAX_NB_BACKUP:
        print(f'deleting: {dump["title"]}')
        dump.Delete()



os.remove(backupFileName)
