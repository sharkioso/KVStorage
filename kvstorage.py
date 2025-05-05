class Storage():
    def __init__(self, size=2):
        """
        происходит инициализация
        param size:размер таблицы
        """
        self.size = size
        self.table = [[] for _ in range(size)]

    def __str__(self):
        """
        возвращет хранилище в виде строки
        """
        output = ""
        for i in range(self.size):
            if (self.table[i]):
                output += f"{self.table[i]}"
        return output

    def list_values(self):
        output = "значения в хранилище "
        for i in self.table:
            if i:
                for j in i:
                    output += f"{j[1] } "
        print(output)

    def hashing(self, key):
        """
        хэширование ключа для этой таблицы
        param key: ключ
        return: захэшированное значение ключа(индекс в таблице)
        """
        try:
            hash(key)
            return hash(key) % self.size
        except TypeError as e:
            print(f"Этот тип данных не поддерживает хэширование: {e}")

    def add_key_value(self, key, value):
        """
        Вставляет пару ключ-значение в хэш-таблицу.
        :param key: Ключ.
        :param value: Значение.
        """
        if key is None:
            print("не поддерживает хэширование")
            return
        index = self.hashing(key)
        for i in self.table[index]:
            if i[0] == key:
                i[1] = value
                print(F'Ошибка: Ключ "{key}" уже существует.')
                return
        self.table[index].append([key, value])
        print(F'Пара ключ-значение "{key}: {value}" добавлена.')

    def get_value(self, key):
        """
        получаем значение по ключу
        param key: ключ
        """
        index = self.hashing(key)
        for i in self.table[index]:
            if i[0] == key:
                print(F'значение для ключа"{key}": {i[1]}')
                return
        print(F'Ошибка: Ключ "{key}" не найден.')

    def __getitem__(self, key):
        return self.get_value(key)

    def __setitem__(self, key, value):
        self.add_key_value(key, value)

    def delete_key(self, key):
        """
        удаляет пару ключ значение
        param key: ключ
        """
        index = self.hashing(key)
        for ind, i in enumerate(self.table[index]):
            if i[0] == key:
                del self.table[index][ind]
                print(f'Пара ключ-значение с ключом "{key}" удалена.')
                return
        print(f'Ошибка: Ключ "{key}" не найден.')

    def clean_storage(self):
        """
        чистит все хранилище
        """
        for i in range(self.size):
            if (self.table[i]):
                self.table[i] = []
