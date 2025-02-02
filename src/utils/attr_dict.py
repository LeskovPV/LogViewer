# coding=utf-8

class AttrDict(dict):
    """
    Справочник атрибутов
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.update(kwargs)

    def add_self_attributes(self, **new_self_attributes):
        for key, value in new_self_attributes.items():
            super().__setattr__(key, value)

    @property
    def self_attributes(self) -> dict:
        """
        Список собственных атрибутов (не входит в словарь и не де/сериализуется)
        """
        return self.__dict__

    def __getattr__(self, key):  # self.key
        if key in self.keys():  # если ключ среди атрибутов,
            return super().__getitem__(key)  # то возвращаем значение атрибут,
        elif key in self.self_attributes:
            return getattr(self, key)
        else:
            return None

    def __getitem__(self, key):  # self[key]
        return self.__getattr__(key)

    def __setattr__(self, key, value):  # self.key = _value
        if key in self.self_attributes or key[0] == '_':  # если ключ среди атрибутов,
            super().__setattr__(key, value)  # то изменяем атрибут,
        else:  # иначе ключ либо уже в словаре, либо его нужно добавить в словарь
            super().__setitem__(key, value)  # изменяем словарь

    def __setitem__(self, key, value):  # self[key] = _value
        self.__setattr__(key, value)

