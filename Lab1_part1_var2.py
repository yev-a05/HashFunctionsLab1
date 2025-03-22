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


# Функція для випадкової модифікації повідомлення
def modify_message_randomly(message):
    # Вибираємо випадкову позицію в повідомленні і змінюємо її
    position = random.randint(0, len(message) - 1)
    random_char = random.choice(string.ascii_letters + string.digits)
    modified_message = message[:position] + random_char + message[position + 1:]
    return modified_message

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
attempts = 0

while not found_preimage:
    attempts += 1
    # Вносимо випадкову модифікацію в повідомлення
    modified_message = modify_message_randomly(random_message)

    # Обчислюємо хеш для модифікованого повідомлення
    current_hash = hashlib.blake2b(modified_message.encode('utf-8')).hexdigest()

    # Обрізаємо хеш до останніх 16 бітів (4 шістнадцяткові символи)
    current_hash_16bit = current_hash[-4:]

    # Додаємо обрізаний хеш до списку
    hashes.append(int(current_hash_16bit, 16))

    # Виводимо інформацію про поточний хеш на кожній ітерації
    print(f"Ітерація {attempts}: Обрізаний хеш: {current_hash_16bit}")

    # Перевіряємо, чи збігається обрізаний хеш
    if current_hash_16bit == original_hash_16bit:
        print(f"Знайдено прообраз на ітерації {attempts}: {modified_message}")
        found_preimage = True
        break

    # Виводимо кількість спроб
    if attempts % 100 == 0:
        print(f"Кількість спроб: {attempts}")

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