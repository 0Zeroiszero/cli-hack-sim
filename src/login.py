import json

# fungsi login sederhana menggunakan dictionary
class Login():
    def __init__(self):
        pass
    
    def login_user(self, servers):
        akun = [item['credential'] for item in servers['servers']]
        
        username = input('Username: ')
        password = input('Password: ')
        
        for i in akun:
            if username == i['username']:
                print ('\nLogin Berhasil!') if password == i['password'] else print('\nPassword Salah!')
                break
        else:
            print('\nUsername Tidak Ditemukan!')

if __name__ == '__main__':
    l = Login()