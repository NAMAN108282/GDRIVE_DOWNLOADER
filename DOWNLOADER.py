import requests, pandas as pd

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id , 'confirm': 1 }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

if __name__ == "__main__":
    sheet_url = "DRIVE EXCEL SHEET LINK"
    url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(url, usecols = ['Recording Link'])

    arr = df.values.tolist()
    c = 0
    for i in arr:
        c += 1
        if str(i).split('/')[0]:
            print(c, str(i)[34:67])

            file_id = str(i)[34:67]
            destination = f"E:\SCRATCH\{file_id}.mp4"
            try:
                download_file_from_google_drive(file_id, destination)
            except PermissionError:
                print(f'permission error copying {file_id} to {destination}')
                
