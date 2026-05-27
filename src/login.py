import json
servers = {}

# fungsi login sederhana menggunakan dictionary
def login_user():
    with open('data/dalam-json/akun.json', 'r') as f:
        servers = json.load(f)
    
    akun = [item['credential'] for item in servers['servers']]
    
    username = input('Username: ')
    password = input('Password: ')
    
    for i in akun:
        if username == i['username']:
            print ('\nLogin Berhasil!') if password == i['password'] else print('\nPassword Salah!')
            break
    else:
        print('\nUsername Tidak Ditemukan!')