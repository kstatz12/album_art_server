"""Upload image to dropbox."""
import dropbox

def __get_dropbox_access_token():
    """Get dropbox access token from env."""
    return os.getenv("DROPBOX_ACCESS")

def upload_to_dropbox(data):
    """Upload data to dropbox."""
    dbx = dropbox.Dropbox(get_dropbox_access_token())
    dbx.files_upload(data, '/current.png', mode=WriteMode('overwrite'))
