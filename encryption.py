#!/etc/usr/bin python3
def public_encryption():
    from random import randint
    prime_a = 41
    prime_b = 37

    n = prime_a * prime_b
    totient_n = (prime_a - 1)*(prime_b - 1)

    aux_totient = totient_n
    factors_totient = []
    while aux_totient != 1:
        divide_by = 1
        if factors_totient is not []:
            for i in factors_totient:
                divide_by *= i
        i = 2
        while i <= int(totient_n/divide_by):
            if aux_totient % i == 0:
                factors_totient.append(i)
                aux_totient /= i
                i = totient_n
            else:
                i += 1

    list_coprimes = []
    for temp_e in range(2, totient_n):
        factors_temp_e = []
        aux_temp_e = temp_e
        while aux_temp_e != 1:
            divide_by = 1
            if factors_temp_e is not []:
                for i in factors_temp_e:
                    divide_by *= i
            i = 2
            while i <= int(temp_e/divide_by):
                if aux_temp_e % i == 0:
                    factors_temp_e.append(i)
                    aux_temp_e /= i
                    i = temp_e
                else:
                    i += 1
        for check_factor in factors_temp_e:
            if check_factor not in factors_totient and check_factor not in list_coprimes:
                list_coprimes.append(check_factor)

    e = list_coprimes[randint(0,len(list_coprimes))]
    #print("Public keys: \nn = {}, \ne = {}\n".format(n, e))

    d = 0
    while True:
        d += 1
        if (e*d)%totient_n == 1:
            break
    #print("Decrypting keys: \nn = {}, \nd = {}".format(n, d))

    public_keys = [n, e]
    private_keys = [n, d]
    return public_keys, private_keys

public_keys, private_keys = public_encryption()

def encrypt_string(raw_text="Hello, world!", keys=public_keys):
    encrypted_text = ""
    for i in range(0,len(raw_text)):
        print(keys)
        encrypted_char = (ord(raw_text[i])**keys[1])%keys[0]
        encrypted_text = encrypted_text + chr(encrypted_char)

    return encrypted_text

def decrypt_string(encrypted_text, keys=private_keys):
    raw_text = ""
    for i in range(0,len(encrypted_text)):
        print(keys)
        raw_char = (ord(encrypted_text[i])**keys[1])%keys[0]
        raw_text = raw_text + chr(raw_char)

    return raw_text


def vigenere_encrypt(raw_text="Hello, world!", password="asdf"):
    full_password=""
    for i in range(0,len(raw_text)):
        full_password = full_password + password[i%len(password)]

    encrypted_text = ""
    for i in range(0, len(raw_text)):
        encrypt_digit = ord(raw_text[i]) + ord(full_password[i])
        encrypted_text = encrypted_text + chr(encrypt_digit)

    return encrypted_text


def vigenere_decrypt(encrypted_string, password="asdf"):
    full_password=""
    for i in range(0, len(encrypted_string)):
        full_password = full_password + password[i%len(password)]

    raw_text = ""
    for i in range(0, len(encrypted_string)):
        raw_digit = ord(encrypted_string[i]) - ord(full_password[i])
        raw_text = raw_text + chr(raw_digit)

    return raw_text



if __name__ == "__main__":
    enc_str = encrypt_string()
    print(enc_str)
    dec_str = decrypt_string(enc_str)
    print(dec_str)
