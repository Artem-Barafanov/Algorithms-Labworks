import os
import pandas as pd
import hashlib

# Глобальные переменные
file_path = None
phones = None
numbers = None

def compute_salt(phones, numbers):
    for phone in phones:
        salt = int(phone) - int(numbers[0])
        if salt < 0:
            continue
        i = 1
        while (str(int(numbers[i]) + salt)) in phones:
            i += 1 
            if i == 5:
                return salt 
    return 0


def sha1(phones):
    phones_sha1 = [hashlib.sha1(phone.encode()).hexdigest() for phone in phones]
    with open('sha1.txt', 'w') as f:
        for phone in phones_sha1:
            f.write(phone + '\n')

    os.remove('hashcat.potfile')
    os.system("hashcat -a 3 -m 100 -o decrypt_sha1.txt sha1.txt ?d?d?d?d?d?d?d?d?d?d?d -O")

def sha256(phones):
    phones_sha256 = [hashlib.sha256(phone.encode()).hexdigest() for phone in phones]
    with open('sha256.txt', 'w') as f:
        for phone in phones_sha256:
            f.write(phone + '\n')

    os.remove('hashcat.potfile')
    os.system("hashcat -a 3 -m 1400 -o decrypt_sha256.txt sha256.txt ?d?d?d?d?d?d?d?d?d?d?d -O")

def sha512(phones):
    phones_sha512 = [hashlib.sha512(phone.encode()).hexdigest() for phone in phones]
    with open('sha512.txt', 'w') as f:
        for phone in phones_sha512:
            f.write(phone + '\n')

    os.remove('hashcat.potfile')
    os.system("hashcat -a 3 -m 1700 -o decrypt_sha512.txt sha512.txt ?d?d?d?d?d?d?d?d?d?d?d -O")


def decrypt_without_salt(file_path):
    global phones, numbers 
    df = pd.read_excel(file_path)
    hashes = df["Номер телефона"]
    numbers = [number[:-2] for number in df["Unnamed: 2"].astype(str).tolist()][:5]
    
    with open('hashes.txt', 'w') as f:
        for HASH in hashes:
            f.write(HASH + "\n")
    os.system("hashcat -a 3 -m 0 -o output.txt hashes.txt ?d?d?d?d?d?d?d?d?d?d?d -O")

    with open('output.txt') as r:
        phones = [line.strip()[33:] for line in r.readlines()]

    with open('phones.txt', 'w') as file:
        for phone in phones:
            file.write(phone + '\n')
    print("Таблица успешно расшифрована. Данные сохранены в файле 'phones.txt'.")


def find_salt():
    global phones, numbers 
    if phones is None:
        print("Данные о телефонах не загружены. Сначала выполните деобезличивание.")
        return
    salt = compute_salt(phones, numbers)
    print(f"Значение соли: {salt}")

    # Обновление списка phones с использованием найденной соли
    if salt > 0:
        phones = [str(int(phone) - salt) for phone in phones]
        with open('phones.txt', 'w') as file:
            for phone in phones:
                file.write(phone + '\n')
        print("Список телефонов обновлен с использованием найденной соли.")


def encrypt_alg(algorithm):
    global phones 
    if phones is None:
        print("Данные о телефонах не загружены. Сначала выполните деобезличивание.")
        return
    if algorithm == "sha1":
        sha1(phones)
        print("Результат сохранен в файле output_sha1.")
    elif algorithm == "sha256":
        sha256(phones)
        print("Результат сохранен в файле output_sha256.")
    else:
        sha512(phones)
        print("Результат сохранен в файле output_sha512.")


# Основная функция
def main():
    global file_path
    file_path = input("Введите путь к файлу Excel: ")
    if not os.path.exists(file_path):
        print("Файл не найден.")
        return

    decrypt_without_salt(file_path)
    find_salt()
    encrypt_alg("sha1")
    encrypt_alg("sha256")
    encrypt_alg("sha512")

if __name__ == "__main__":
    main()