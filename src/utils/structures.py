# coding=utf-8
from typing import Any

from utils.attr_dict import AttrDict


class TreeItem(AttrDict):

    def __init__(self,
                 title: str,
                 parent: Any = None,  # TreeGroup
                 **kwargs):
        """
        :param title:
        """
        super().__init__(title=title, **kwargs)
        self.add_self_attributes(_parent=parent)

    def get_parent(self):
        return self._parent


class TreeGroup(TreeItem):

    NONE_GROUP_NAME: str = 'неопределённый'
    """
    Имя группы для значений None и для других случаев, когда невозможно установить значение
    - например, отсутствие запрашиваемого атрибута
    """

    def __init__(self,
                 items: list[TreeItem],
                 props: list[str] = None,
                 title: str = None,
                 parent: Any = None):
        """
        Дерево: группы первого уровня создаются из множества значений свойства props[0],
        при этом список items делится на соответствующее множество списков;
        аналогично формируются группы последующих уровней вплоть до len(props)
        Таким образом, каждая группа уровня len(props) содержит один или более элементов из items,
        отсутствуют пустые группы и все элементы items содержаться в дереве, причём единожды

        :param items: Список дочерних элементов в составе генерируемого дерева
        :param props: Список имён атрибутов - первый используется для группировки, остальные передаются в рекурсию
        :param parent: Родительский узел дерева
        :param title: Наименование узел дерева
        :return: Дерево
        """
        super().__init__(title=title, parent=parent)
        self.add_self_attributes(
            _children=None,
            _items=items,
            _props=props)
        # self.get_children()  # Формирование дерева во время инициализации без ожидания запроса "развернуть"

    def get_children(self):
        if isinstance(self._children, list):
            return self._children
        self._children = []
        if len(self._props) == 0:
            for item in self._items:
                self._children.append(TreeItem(parent=self, **item))
            # self._children.extend(self._items)
        else:
            # Формируем список групп первого уровня из множества значений свойства props[0]
            prop = self._props[0]
            groups = dict()
            for item in self._items:
                group = f'{self.NONE_GROUP_NAME} {prop}' if item.get(prop, None) is None else item[prop]
                if group not in groups.keys():
                    groups[group] = []
                groups[group].append(item)

            for group, group_items in groups.items():
                self._children.append(TreeGroup(
                    items=group_items,
                    props=self._props[1:],
                    title=group,
                    parent=self
                ))  # list[TreeGroup | TreeItem]
        return self._children