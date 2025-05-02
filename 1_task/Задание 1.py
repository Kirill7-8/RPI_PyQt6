import hashlib
file = open("data.txt", "r+", encoding="utf-8")
data = list(map(lambda x: x.strip(), file.readlines()))


def hashpas(x):
    return hashlib.sha256(x.encode()).hexdigest()


print('Добро пожаловать:)')
while True:
    ch = input('Для входа в систему напишите "1"\nЕсли вы новый пользователь, то зарегистрируйтесь в системе, для этого напишите "2"\n')
    if ch == "2":
        while True:
            log = input("Придумайте логин: ")
            if len(log) < 5:
                print("Логин слишком короткий! Логин состоит не менее чем из 5 символов")
            elif not all('a' <= a <= 'z' or a.isdigit() for a in log.lower()):
                print("Логин должен состоять из символов из набора латинских букв и цифр!")
            elif log in data[0::7]:
                print("Пользователь с таким логином уже зарегистрирован")
            else:
                break
        file.write(log + "\n")

        while True:
            pas1 = input("Придумайте пароль: ")
            if len(pas1) < 8:
                print("Пароль слишком короткий! Пароль должен состоять не менее чем из 8 символов!")
            elif not any(b.isdigit() for b in pas1):
                print("Пароль должен содержать хотя бы одну цифру!")
            elif not any(c in "|?/.,<>';:[]{}!@#$%^&*()_=+~`" for c in pas1):
                print("Пароль должен содержать хотя бы один специальный символ")
            elif not (any("a" <= d <= "z" for d in pas1) and any("A" <= z <= "Z" for z in pas1)):
                print("Пароль должен содержать как минимум одну строчную и одну прописную букву")
            else:
                pas1 = hashpas(pas1)
                break

        while True:
            pas2 = hashpas(input("Введите пароль повторно: "))
            if pas1 != pas2:
                print("Пароли не совпадают!")
            else:
                break
        file.write(pas2 + "\n")

        while True:
            email = input("Введите адрес электронной почты: ")
            if email[0] == "@" or email[-1] == "@" or email.count("@") != 1:
                print("Некорректный адрес электронной почты!\nАдрес электронной почты должен содержать ровно один символ @, но не начинаться с него и не заканчиваться им.")
            elif email in data[2::7]:
                print("Пользователь с таким адресом электронной почты уже зарегистрирован")
            else:
                break
        file.write(email + "\n")

        print("Введите номер телефона")
        while True:
            nu = input("Номер телефона должен содержать только код страны и цифры! (Например +7 123 456 78 90 или 8 123 456 78 90)\n").split()
            num = "".join(nu)
            if "+7" == num[:2] and num[2:].isdigit() and len(num[2:]) == 10:
                file.write(num[2:] + "\n")
                break
            elif "8" == num[0] and num[1:].isdigit() and len(num[1:]) == 10:
                file.write("7" + num[1:] + "\n")
                break
            elif num[1:] in data[3::7]:
                print("Пользователь с таким номером телефона уже зарегистрирован")
            else:
                print("Неверно!")

        print("Вы хотите указать свое ФИО?")
        while True:
            fio = input("Напишите: Да/нет\n")
            if fio.lower() == "да":
                fio = input("Укажите своё ФИО:\n")
                break
            elif fio.lower() == "нет":
                fio = "None"
                break
        file.write(fio + "\n")

        print("Вы хотите указать свой город")
        while True:
            city = input("Напишите: Да/нет\n")
            if city.lower() == "да":
                city = input("Укажите свой город\n")
                break
            elif city.lower() == "нет":
                city = "None"
                break
        file.write(city + "\n")

        print("Вы хотите указать информацию о себе")
        while True:
            mine = input("Напишите: Да/нет\n")
            if mine.lower() == "да":
                mine = input("Расскажите о себе:\n")
                break
            elif mine.lower() == "нет":
                mine = "None"
                break
        file.write(mine + "\n")
        print("Вы успешно зарегистрировались в системе!")
        break
    elif ch == "1":
        while True:
            log = input("Введите свой логин или номер телефона или почту: ")
            if log in data[0::7]:
                break
            elif log in data[2::7]:
                break
            elif log[1:] in data[3::7]:
                break
            elif log[2:] in data[3::7]:
                break
            else:
                print("Пользователь не найден!")

        while True:
            pas = hashpas(input("Введите пароль: "))
            if pas in data[1::7]:
                break
            else:
                print("Неверный пароль! Попробуйте еще раз")
        print("Добро пожаловать в систему!")
        break