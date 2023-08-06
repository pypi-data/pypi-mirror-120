""" Содержит функционал WTAS """


def no_operator(func):
    """
    Декоратор вызова оператора по ключу. Возвращает None, если искомый
    оператор не найден.

    :param func: Функция извлечения WTAS или WTADB.
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return None
    return wrapper


def get_ar_id(gc_qdk, table_name, wserver_id):
    """
    Извлечь из AR id записи по его WServer ID.

    :param gc_qdk: Экземпляр QDK для взаимодействия с GCore.
    :param table_name: Имя таблицы, из которой нужно извлечь данные.
    :param wserver_id: WServer ID.
    :return:
    """
    gc_qdk.get_wserver_id(table_name, wserver_id)
    type_ar_response = gc_qdk.get_data()
    if type_ar_response['status']:
        return type_ar_response['info']
