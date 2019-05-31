from random import randint

def generatePasswords(str, length_min, length_max, requirements):
# takes list of keywords and generates 10 random passwords in ascii number form for each password lengths 6 to 10

    output_list = []
    length_min = int(length_min) + 1
    length_max = int(length_max) + 1
    for password_length in range(length_min, length_max):
        password_amount = 0                 # zero out password amount for each length of passwords

        while password_amount < 10:
            storage = list(str)        # make copy of list
            storage.extend(requirements)    # add the special character requirements into possible passwords
            pw = []                         # where individual passwords will be assembled

            while((len(pw) < password_length) and (len(storage) > 0)):
                random_int = randint(0, len(storage)-1)
                temp = storage.pop(random_int)
                pw.append(temp)

            password_amount += 1
            output_list.append(pw)

    return output_list

def storePasswords(str):
    passwords = []
    for pw in str:
        word = ''.join(x for x in pw if x != 32)
        passwords.append(word)






