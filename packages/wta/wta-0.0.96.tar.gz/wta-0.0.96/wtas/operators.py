""" Модуль содержит обработчики для разных видов данных. """
import wsqluse.wsqluse

from wtas.main import WTAS, WTADB
from wtas import functions


class TrashCatsS(WTAS):
    """ Оператор передачи данных в AR. """

    def send(self, name, wserver_id, wtadb, *args, **kwargs):
        self.add_trash_cat(cat_name=name, wserver_id=wserver_id)


class TrashCatsDB(WTADB):
    """ Оператор обработки ответа от AR. """

    def __init__(self, *args, **kwargs):
        super().__init__(table_name='trash_cats_send_reports',
                         column_name='trash_cat', *args, **kwargs)


class TrashCatsUPD(WTAS):
    """ Оператор передачи о обновлении вида груза в AR. """

    def send(self, cat_id, new_name=None, active=None, **kwargs):
        # Запрашиваем wdb.ID из AR для вида груза
        cat_ar_id = functions.get_ar_id(self, 'trash_cats', cat_id)
        if cat_ar_id:
            self.upd_trash_cat(cat_id=cat_ar_id, name=new_name, active=active,
                               wserver_id=cat_id)


class TrashTypesS(WTAS):
    """ Оператор передачи данных в AR. """

    def send(self, name, wserver_id, wtadb, trash_cat_id, *args, **kwargs):
        self.add_trash_type(type_name=name, wserver_id=wserver_id,
                            wserver_cat_id=trash_cat_id)


class TrashTypesUPD(WTAS):
    """ Оператор передачи о обновлении вида груза в AR. """

    def send(self, type_id, new_name=None, new_cat_id=None, active=None,
             *args, **kwargs):
        # Запрашиваем wdb.ID из AR для вида груза
        type_ar_id = functions.get_ar_id(self, 'trash_types', type_id)
        cat_ar_id = functions.get_ar_id(self, 'trash_cats', new_cat_id)
        if type_ar_id and cat_ar_id:
            self.upd_trash_type(type_id=type_ar_id, name=new_name,
                                category=cat_ar_id, active=active)


class TrashTypesDB(WTADB):
    """ Оператор обработки ответа от AR об обновлении вида груза """

    def __init__(self, *args, **kwargs):
        super().__init__(table_name='trash_types_send_reports',
                         column_name='trash_type', *args, **kwargs)


class CompaniesS(WTAS):
    """ Оператор передачи данных в AR. """

    def send(self, name, wtadb, inn=None, kpp=None, ex_id=None, status=None,
             wserver_id=None, *args, **kwargs):
        self.add_carrier(name, inn, kpp, ex_id, status, wserver_id)


class CompaniesUPD(WTAS):
    def send(self, company_id, name=None, inn=None, kpp=None, status=None,
             ex_id=None, active=None, wserver_id=None, **kwargs):
        ar_company_id = functions.get_ar_id(self, 'clients', company_id)
        if ar_company_id:
            self.upd_carrier(client_id=company_id, name=name, active=active,
                             wserver_id=company_id, status=status, inn=inn,
                             kpp=kpp, ex_id=ex_id)


class CompaniesDB(WTADB):
    """ Оператор обработки ответа от AR. """

    def __init__(self, *args, **kwargs):
        super().__init__(table_name='companies_send_reports',
                         column_name='company', *args, **kwargs)


class AutoS(WTAS):
    """ Оператор передачи данных в AR. """

    def send(self, car_number, wserver_id, wtadb, model=None, rfid=None,
             rfid_id=None, id_type=None, rg_weight=None, *args, **kwargs):
        self.add_auto(car_number=car_number, wserver_id=wserver_id,
                      model=model, id_type=id_type, rg_weight=rg_weight,
                      rfid=rfid, rfid_id=rfid_id)


class AutoUPD(WTAS):
    """ Оператор передачи обновления по авто в AR."""

    def send(self, auto_id: int, new_car_number=None,
             new_id_type: str = None, new_rg_weight: int = 0,
             new_model: int = 0, new_rfid_id: int = None, active=True,
             wtadb=None,
             **kwargs):
        if new_rfid_id:
            rfid = wtadb.get_rfid(new_rfid_id)
        ar_auto_id = functions.get_ar_id(self, 'auto', auto_id)
        if ar_auto_id:
            self.upd_auto(auto_id=auto_id, car_number=new_car_number,
                          id_type=new_id_type, rg_weight=new_rg_weight,
                          auto_model=new_model, rfid=rfid, active=active)


class AutoDB(WTADB):
    """ Оператор обработки ответа от AR. """

    def __init__(self, *args, **kwargs):
        super().__init__(table_name='auto_send_reports',
                         column_name='auto', *args, **kwargs)

    @wsqluse.wsqluse.tryExecuteGetStripper
    def get_rfid(self, rfid_id):
        """
        Получить rfid номер из GDB по его ID.

        :param rfid_id: RFID ID.
        :return:
        """
        command = "SELECT rfid FROM rfid_marks WHERE id={}"
        command = command.format(rfid_id)
        return self.try_execute_get(command)


class UserS(WTAS):
    """ Оператор передачи данных в AR. """

    def send(self, full_name, username, password, wserver_id, wtadb):
        self.add_operator(full_name, username, password, wserver_id)


class UserUPD(WTAS):
    """ Оператор передачи обновлений пользователя в AR """

    def send(self, operator_id: int, full_name: str = None,
             login: str = None, password: str = None, active: bool = True,
             **kwargs):
        ar_operator_id = functions.get_ar_id(self, 'users', operator_id)
        if ar_operator_id:
            self.upd_operator(user_id=ar_operator_id, username=login,
                              password=password, full_name=full_name,
                              active=active)


class UserDB(WTADB):
    """ Оператор обработки ответа от AR. """

    def __init__(self, *args, **kwargs):
        super().__init__(table_name='operators_send_reports',
                         column_name='operator', *args, **kwargs)


class GetOperator:
    """ Класс, который возвращает объекты для отправки данных на AR и обработку
    ответов. Главным компонентом является атрибут operators, который содержит
    в форме ключей названия данных (в строковом представлении), имеюющих
    следующую структуру:
        'operation_name': {'wtas': Object, 'wtadb': Object},
    Где значением ключа wtas является подкласс WTAS, предназначенный для
    обмена данными между WServer и AR, а ключом wtadb - подкласс WTADB, который
    отвечает за работу с БД."""

    def __init__(self):
        self.operators = {'trash_cats':
                              {'wtas': TrashCatsS,
                               'wtadb': TrashCatsDB},
                          'trash_cats_upd':
                              {'wtas': TrashCatsUPD,
                               'wtadb': TrashCatsDB},
                          'trash_types':
                              {'wtas': TrashTypesS,
                               'wtadb': TrashTypesDB},
                          'trash_types_upd':
                              {'wtas': TrashTypesUPD,
                               'wtadb': TrashTypesDB},
                          'companies':
                              {'wtas': CompaniesS,
                               'wtadb': CompaniesDB},
                          'companies_upd':
                              {'wtas': CompaniesUPD,
                               'wtadb': CompaniesDB},
                          'auto': {'wtas': AutoS,
                                   'wtadb': AutoDB},
                          'auto_upd': {'wtas': AutoUPD,
                                       'wtadb': AutoDB},
                          'users': {'wtas': UserS,
                                    'wtadb': UserDB},
                          'users_upd': {'wtas': UserUPD,
                                        'wtadb': UserDB},
                          }

    @functions.no_operator
    def get_wtas_class(self, name):
        """
        Вернуть объект класса WTADB.

        :param name: Название данных.
        :return:
        """
        return self.operators[name]['wtas']

    @functions.no_operator
    def get_wtadb_class(self, name):
        """
        Вернуть объект класса WTADB.

        :param name: Название данных.
        :return:
        """
        return self.operators[name]['wtadb']

    def expand_operators(self, new_operator):
        """
        Расширить словарь операторов.

        :param new_operator: Словарь вида:
            {'name': {'wtas': object, 'wtadb': object}}
        :return: Возвращает обновленный список операторов.
        """
        return self.operators.update(new_operator)


class WTA(GetOperator):
    """ Класс, объединяющий классы для работы с БД и с AR. Предоставляет один
    интерфейс (метод deliver),
    который делает всю работу по отправке данных, и фиксации  этого события.
    По сути - god-object (плохо, да, но до жути удобно).
    """

    def __init__(self, name, dbname, user, password, host, polygon_id,
                 *args, **kwargs):
        """
        Инициализация.

        :param name: Название вида данных.
        :param dbname: Имя базы данных (GDB).
        :param user: Имя пользователя БД.
        :param password: Пароль пользователя БД.
        :param host: Адрес машины, на котором хостится БД.
        :param polygon_id: ID полигона, куда отправить данные.
        :param args:
        :param kwargs:
        """
        super(WTA, self).__init__(*args, **kwargs)
        self.wtadb = self.get_wtadb(name, dbname, user, password, host,
                                    polygon_id)
        pol_info = self.wtadb.fetch_polygon_info()
        self.wtas = self.get_wtas(name, pol_info['ip'], pol_info['port'])

    def operate_response(self, ar_response, report_id, wserver_id):
        """ Обработчиков ответа от GCore
        :param wserver_id: ID в GDB.
        :param ar_response: Сам ответ.
        :param report_id: ID отчета об отправке.
        :return: Возвращает словарь со статусом выполнения. """
        response = {}
        response['report_id'] = report_id
        response['wserver_id'] = wserver_id
        if ar_response['info']['status'] == 'success':
            self.wtadb.mark_get(wdb_id=ar_response['info']['info'][0][0],
                                report_id=report_id)
            response['success_save'] = True
        else:
            response['success_save'] = False
            self.wtadb.mark_fail(ar_response['info']['info'], report_id)
        return response

    def get_wtadb(self, name, dbname, user, password, host, polygon_id):
        """
        Вернуть инстанс класса WTADB, предназначенный для работы с данными вида
        name.
        :param name: Название вида данных.
        :param dbname: Имя базы данных (GDB).
        :param user: Имя пользователя БД.
        :param password: Пароль пользователя БД.
        :param host: Адрес машины, на котором хостится БД.
        :param polygon_id: ID полигона, куда отправить данные.
        :return:
        """
        wtadb_class = self.get_wtadb_class(name)
        wtadb = wtadb_class(dbname=dbname, user=user,
                            password=password,
                            host=host,
                            polygon_id=polygon_id)
        return wtadb

    def get_wtas(self, name, polygon_ip, polygon_port):
        """ Получить объекты для работы с БД и с GCore по названию.

        :param name: Название данных.
        :param polygon_ip: IP GCore QDK.
        :param polygon_port: Порт GCore QDK.
        :return: Если объекты предусмотрены - вернет True.
        """
        wtas_class = self.get_wtas_class(name)
        wtas = wtas_class(polygon_ip=polygon_ip,
                          polygon_port=polygon_port)
        return wtas

    def deliver(self, wserver_id, *args, **kwargs):
        """ Доставить данные до GCore. Отметить успешность доставки.
        :param wserver_id: Обязательный аругемент, ID данных в GDB.
        :return: Если все успешно - вернет True """
        self.wtas.send(wserver_id=wserver_id, wtadb=self.wtadb,
                       *args, **kwargs)
        report_id = self.wtadb.mark_send(gdb_id=wserver_id)
        response = self.wtas.get()
        res = self.operate_response(response, report_id, wserver_id)
        return res
