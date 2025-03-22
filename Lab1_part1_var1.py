import hashlib
import random
import string
import numpy as np
import scipy.stats as stats

pib = "Фурутіна Євгенія Віталіївна"

# Створюємо випадкове повідомлення, яке містить ПІБ
def generate_random_message(pib):
    # Генеруємо випадкові символи перед і після ПІБ
    random_prefix = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    message = random_prefix + pib + random_suffix
    return message


# Формуємо випадкове повідомлення з ПІБ
random_message = generate_random_message(pib)

# Обчислюємо хеш для випадкового повідомлення з ПІБ
original_hash = hashlib.blake2b(random_message.encode('utf-8')).hexdigest()

# Обрізаємо хеш до останніх 16 бітів (це останні 4 шістнадцяткових символи)
original_hash_16bit = original_hash[-4:]  # 16 біт = останні 4 шістнадцяткові символи
print(f"Випадкове повідомлення: {random_message}")
print(f"Обрізаний хеш (останнi 16 бітів): {original_hash_16bit}")
print(f"Повний хеш: {original_hash}")

# Створимо список для збереження обрізаних хешів для аналізу
hashes = []

found_preimage = False
for i in range(1, 1001):  # 1000 ітерацій
    # Генеруємо нове випадкове повідомлення з числом
    message_with_number = random_message + str(i)
    current_hash = hashlib.blake2b(message_with_number.encode('utf-8')).hexdigest()

    # Обрізаємо хеш до останніх 16 бітів (4 шістнадцяткові символи)
    current_hash_16bit = current_hash[-4:]

    # Додаємо обрізаний хеш до списку
    hashes.append(int(current_hash_16bit, 16))

    # Виводимо інформацію про поточний хеш на кожній ітерації
    print(f"Ітерація {i}: Обрізаний хеш: {current_hash_16bit}")

    # Перевіряємо, чи збігається обрізаний хеш
    if current_hash_16bit == original_hash_16bit:
        print(f"Знайдено прообраз на числі {i}: {message_with_number}")
        found_preimage = True
        break

if not found_preimage:
    print("Не вдалося знайти прообраз.")

# Обчислюємо математичне очікування (середнє значення)
mean = np.mean(hashes)

# Обчислюємо дисперсію
variance = np.var(hashes)

# Обчислюємо стандартне відхилення
std_dev = np.std(hashes)

# Обчислюємо довірчий інтервал для середнього з рівнем довіри 95%
confidence_interval = stats.t.interval(0.95, len(hashes)-1, loc=mean, scale=std_dev/np.sqrt(len(hashes)))

# Виводимо результати
print(f"Математичне очікування (середнє): {mean}")
print(f"Дисперсія: {variance}")
print(f"Стандартне відхилення: {std_dev}")
print(f"Довірчий інтервал (95%): ({confidence_interval[0].item()}, {confidence_interval[1].item()})")