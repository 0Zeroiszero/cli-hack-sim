akun = {
    'admin' : '12345'
}

# fungsi login sederhana menggunakan dictionary
def login_user():
    username = input('Username: ')
    password = input('Password: ')
    
    if username in akun:
        print ('Login Berhasil!') if password == akun[username] else print('Password Salah!')
    else:
        print('Usernamae Tidak Ditemukan!')