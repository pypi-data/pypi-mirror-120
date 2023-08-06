""" Модуль, содержащий основной класс GCoreQDK, являющийся носителем всех
методов для взаимодействия с Gravity Compound. Используется как графическим
интерфейсом весовщика, так и WServer."""
import threading
from traceback import format_exc
from qdk.main import QDK


class GCoreQDK(QDK):
    """ Главный класс, содержащий все методы для взаимодействия с GCore """

    def __init__(self, host_ip, host_port, host_login='login',
                 host_password='pass', start_resp_operator=False,
                 only_show_response=False,
                 *args, **kwargs):
        """
        Инициация приложения.

        :param host_ip: IP адрес машины с GCore
        :param host_port: Port GCore QPI
        :param host_login: Логин, если требуется
        :param host_password: Пароль, если требуется
        :param start_resp_operator: Запустить или нет встроенный обработчк
            ответов от GCore QPI. Принимает либо False, либо словарь,
            в котором ключом является метод GCore QPI, вернувший ответ,
            а ключом - функция, которая должна этот ответ обрабатывать.
            (значение ключа info, из словаря, который отправляет QPI)
        :param args:
        :param kwargs:
        """
        super().__init__(host_ip, host_port, host_login, host_password,
                         *args, **kwargs)
        self.resp_operator_dict = start_resp_operator
        self.only_show_response = only_show_response

    def set_resp_operator_dict(self, response_operator_dict: dict):
        """
        Установить словарь операторов ответов

        :param response_operator_dict:
        :return:
        """
        self.resp_operator_dict = response_operator_dict

    def start_round(self, car_number: str, course: str, car_choose_mode: str,
                    dlinnomer: bool = False, polomka: bool = False,
                    carrier: int = None, trash_cat: int = None,
                    trash_type: int = None, notes: str = None,
                    operator: int = None, duo_polygon: int = None):
        """
        Отдать команду на начало раунда взвешивания

        :param car_number: гос. номер, в строковом представлении,
            типа "A111AA702"
        :param course: направление, с какой стороны стоит машина
            (external/internal)
        :param car_choose_mode: спсособ инициации заезда (auto/manual),
            если auto - значит система сама увидела машину,
            если manual - значит заезд инициируют вручную
        :param dlinnomer: Спец. проткол "Длинномер" (True/False)
        :param polomka: Спец. протокол "Поломка" (True/False)
        :param carrier: ID перевозчика
        :param trash_cat: ID категории груза
        :param trash_type: ID вида груза
        :param notes: Комментарий весовщика
        :param operator: ID весовщика
        :param duo_polygon: ID объекта, принимающего груз

        :return: В случае успеха:
                {'status': True, 'info': 'Поток выполнения запущен успешно',
                'record_id': *id: int*};

            В случае провала (уже активен заезд):
                {'status': False, 'info': 'GCore занят в данный момент', 'record_id':
                *id: int*}
        """
        self.execute_method('start_weight_round', car_number=car_number,
                            course=course, car_choose_mode=car_choose_mode,
                            spec_protocol_dlinnomer_bool=polomka,
                            spec_protocol_polomka_bool=dlinnomer,
                            carrier=carrier, trash_cat=trash_cat,
                            trash_type=trash_type, notes=notes,
                            operator=operator, duo_polygon=duo_polygon)

    def get_status(self):
        """ Вернуть состояние готовности весовой площадки (есть активные заезды
            или нет)
        :return: False/True"""
        self.execute_method('get_status')

    def add_comment(self, record_id: int, comment: str):
        """
        Добавить комментарий к существующему заезду.

        :param record_id: id записи
        :param comment: добавочный комментарий
        :return:
            В случае успеха:
                {'status': 'success', 'info': [(*id: int*,)]}
            В случае провала:
                {'status': 'failed', 'info': Python Traceback}
        """
        self.execute_method('add_comment', record_id=record_id,
                            comment=comment)

    def change_opened_record(self, record_id: int, car_number: str = None,
                             carrier: int = None, trash_cat_id: int = None,
                             trash_type_id: int = None, comment: str = None,
                             polygon: int = None, auto_id: int = None):
        """
        Изменить запись. Можно менять все основные параметры.

        :param record_id: ID этой записи
        :param car_number: Гос.номер, на который надо поменять (если такой
            машины нет, она будет зарегана, в любом случае,
            в записи будет отображаться только ссылка на это авто.
        :param carrier: ID перевозчика
        :param trash_cat_id: ID категории груза
        :param trash_type_id: ID вида груза
        :param comment: комментарий, который нужно поменять
        :param polygon: Полигон
        :param auto_id: Можно указать ID авто напямую (но, как правило, через
            графический интерфейс поступает гос.номер в виде строки
            (см. car_number))
        :return:
            В случае успеха:
                {'status': 'success', 'info': {'status': 'success',
                    'info': 'Данные успешно изменены'}}
            В случае провала:
                {'status': 'failed', 'info': Python Traceback}
            Либо:
                None - если не найден заезд с таким ID

        """
        self.execute_method('change_opened_record', record_id=record_id,
                            car_number=car_number, carrier=carrier,
                            trash_cat_id=trash_cat_id,
                            trash_type_id=trash_type_id, comment=comment,
                            polygon=polygon, auto_id=auto_id)

    def close_opened_record(self, record_id: int):
        """
        Закрыть открытую запись (у которой есть только брутто)

        :param record_id: ID этой записи
        :return:
            В случае успеха:
                id: int
            В случае провала:
                None
        """
        self.execute_method('close_opened_record', record_id=record_id)

    def get_unfinished_records(self):
        """
        Вернуть список, содержащий словари, каждый из которых описывает заезд,
            который еще не завершен (без тары)

        :return:
            Если есть незакрытые заезды:
                Вернет список словарь, где ключом
                является поле из wdb.records, а значением - содержимое поля
            Если незакрытых заездов нет:
                None

        """
        self.execute_method('get_unfinished_records')

    def get_history(self, time_start=None, time_end=None, trash_cat=None,
                    trash_type=None, carrier=None, auto_id=None, polygon=None,
                    alerts=None, what_time='time_in'):
        """
        Получить историю заездов. Если ни один аргумент не указан, то вернется
        история за сегодняшний день, без каких либо фильтров. Указанные же
        аргументы - это фильтры, они суммируются в любом порядке и количестве.

        :param time_start: с какой даты учитывать
        :param time_end: по какую дату учитывать
        :param trash_cat: фильтрация по категории груза
        :param trash_type: фильтрация по виду груза
        :param carrier: фильтрация по перевозчику
        :param auto_id: фильтрация по авто
        :param polygon: фильтрация по объекту-приемщику
        :param alerts: фильтрация по наличию алертов
        :param what_time: какую дату брать за учетную (time_in|time_out).
            То есть, time_start и time_end могут быть как время въезда, так и
            время выезда (по умолчанию, это время въезда)
        :return:
            Если есть заезды по указанным фильтрам:
                Вернет список словарь, где ключом
                является поле из wdb.records, а значением - содержимое поля
            Если по указанным фильтрам заездов нет:
                None
        """
        self.execute_method('get_history', time_start=time_start,
                            time_end=time_end, trash_cat=trash_cat,
                            trash_type=trash_type, carrier=carrier,
                            auto_id=auto_id, polygon=polygon,
                            alerts=alerts, what_time=what_time)

    def get_table_info(self, table_name: str, only_active=True):
        """
        Вернуть данные о таблице из wdb.
            Внимание! Не все таблицы доступны, как и не все поля, доступ по
            таблице происходит из белого списка, а по полям, не отправляются те
            поля, которые отмечены в черном списке (например, поле users.password).
            Механизм допуска прописан в модуле gravity_data_worker.

        :param table_name: Название нужной таблицы
        :param only_active: Возвращать ли только те поля, у которых поле active
            положительно?
        :return:
            В случае успеха:
                {'status': 'success', info: [*список заездов*]}
            В случае, когда к данным таблицы доступ запрещен:
                {'status': 'failed', 'info': 'У вас нет доступа к просмотру
                    информации с данной таблицы!', 'tablename': *tablename*}
        """
        self.execute_method('get_table_info', tablename=table_name,
                            only_active=only_active)

    def get_last_event(self, auto_id: int):
        """
        Получить данные о последнем заезде авто с ID (auto_id)

        :param auto_id: ID авто, по котором нужна информация
        :return:
            Если машина найдена:
                Возвращает словарь с данными о перевозчике, виде груза,
                категории груза и времени с последнего заезда
            Если же заезда с такой машины не обнаружено:
                None
        """
        self.execute_method('get_last_event', auto_id=auto_id)

    def open_external_barrier(self):
        """
        Открыть внешний шлагбаум

        :return: {'operation': 'open', 'barrier_name': 'EXTERNAL_GATE'}
        """
        self.operate_barrier(barrier_name='EXTERNAL_GATE', operation='open')

    def close_external_barrier(self):
        """
        Закрыть внешний шлагбаум

        :return: {'operation': 'close', 'barrier_name': 'EXTERNAL_GATE'}
        """
        self.operate_barrier(barrier_name='EXTERNAL_GATE', operation='close')

    def open_internal_barrier(self):
        """
        Открыть внешний шлагбаум

        :return: {'operation': 'open', 'barrier_name': 'INTERNAL_GATE'}
        """
        self.operate_barrier(barrier_name='INTERNAL_GATE', operation='open')

    def close_internal_barrier(self):
        """
        Закрыть внешний шлагбаум

        :return: {'operation': 'close', 'barrier_name': 'INTERNAL_GATE'}
        """
        self.operate_barrier(barrier_name='INTERNAL_GATE', operation='close')

    def operate_barrier(self, barrier_name: str, operation: str):
        """
        Произвести работу со шлагбаумами (открыть или закрыть)

        :param barrier_name: Название шлагбаума. Обычно он носит вид,
            типа "НАПРАВЛЕНИЕ_ИМЯ" (EXTERNAL_BARRIER)
        :param operation: (close|open) Открыть или закрыть шлагбаум
        :return:
        """
        self.execute_method('operate_gate_manual_control',
                            barrier_name=barrier_name,
                            operation=operation)

    def try_auth_user(self, username: str, password: str):
        """ Попытка аутентификации весовщика через графический интерфейс

        :param username: Логин пользователя
        :param password: Пароль пользователя
        :return:
            В случае успешной аутентификации юзера:
                {'status': True, 'info': id: int}
            В случае, если логин или пароль не верные:
                {'status': False, 'info': None}
        """
        self.execute_method('try_auth_user', username=username,
                            password=password)

    def capture_gui_launched(self):
        """ Зафиксировать запуск графического интерфейса в логе
        :return: [(id)] (id записи из cm_events_log)"""

        self.execute_method('capture_cm_launched')

    def capture_gui_terminated(self):
        """ Зафиксировать отключение графического интерфейса в логе
        :return: [(id)] (id записи из cm_events_log)"""

        self.execute_method('capture_cm_terminated')

    def restart_core(self):
        """ Перезапустить Gravity Core Compound """

        self.execute_method('restart_core')

    def add_carrier(self, name, inn=None, kpp=None, ex_id=None, status=None,
                    wserver_id=None):
        """
        Добавить нового перевозчика

        :param name: Название перевозчика
        :param inn: ИНН перевозчика
        :param kpp: КПП перевозчика
        :param ex_id: ID перевозчика из внешней системы (например, 1С)
        :param status: Статус (действующий/недействующий)
        :param wserver_id: ID перевозчика в базе GDB
        :return:
            В случае успеха:
                {'status': 'success', 'info': [(*id: int*,)]}
            В случае провала:
                {'status': 'failed', 'info': Python Traceback}
        """
        self.execute_method('add_new_carrier', name=name, inn=inn, kpp=kpp,
                            ex_id=ex_id, status=status, wserver_id=wserver_id)

    def upd_carrier(self, client_id, name=None, active=None,
                    wserver_id=None, status=None, inn=None,
                    kpp=None, ex_id=None):
        """
        Обновить компанию-перевозчика.

        :param client_id: ID компании.
        :param name: Изменить имя.
        :param active: Изменить активность.
        :param wserver_id: Изменить WServer ID.
        :param status: Изменить статус компании.
        :param inn: Изменить ИНН.
        :param kpp: Изменить КПП.
        :param ex_id: Изменить ID внешней системы.
        :return:
        """
        self.execute_method('upd_carrier', client_id=client_id, name=name,
                            active=active, wserver_id=wserver_id,
                            status=status, inn=inn, kpp=kpp, ex_id=ex_id)

    def add_auto(self, car_number, wserver_id, model, rfid, id_type,
                 rg_weight, rfid_id=None, **kwargs):
        """
        Добавить новое авто

        :param rfid_id: ID RFID (необязательно.)
        :param car_number: Гос.номер авто
        :param wserver_id: ID авто из базы GDB
        :param model: Модель авто
        :param rfid: RFID номер авто
        :param id_type: Протокол авто
        :param rg_weight: Справочный вес тары авто
        :return:
            В случае успеха:
                {'status': 'success', 'info': [(*id: int*,)]}
            В случае провала:
                {'status': 'failed', 'info': Python Traceback}
        """
        self.execute_method('add_auto', car_number=car_number, model=model,
                            rfid=rfid, id_type=id_type, rg_weight=rg_weight,
                            wserver_id=wserver_id, rfid_id=rfid_id)

    def upd_auto(self, auto_id, car_number=None, rfid=None, id_type=None,
                 rg_weight=None, wserver_id=None, auto_model=None,
                 active=None, *args, **kwargs):
        """
        Обновить авто.

        :param auto_id: ID авто.
        :param car_number: Изменить гос. номер.
        :param rfid: Изменить RFID номер.
        :param id_type: Изменить вид протокола.
        :param rg_weight: Изменить справочный вес.
        :param wserver_id: Изменить WServer ID.
        :param auto_model: Изменить модель авто.
        :param active: Изменить активность записи.
        :param args:
        :param kwargs:
        :return:
        """
        self.execute_method('upd_auto', car_number=car_number, rfid=rfid,
                            id_type=id_type, rg_weight=rg_weight,
                            wserver_id=wserver_id, auto_model=auto_model,
                            active=active)

    def add_trash_cat(self, cat_name, wserver_id):
        """
        Добавить новую категорию груза

        :param cat_name: Название категории груза
        :param wserver_id: ID из базы GDB
        :return:
            В случае успеха:
                {'status': 'success', 'info': [(*id: int*,)]}
            В случае провала:
                {'status': 'failed', 'info': Python Traceback}
        """
        self.execute_method('add_trash_cat', cat_name=cat_name,
                            wserver_id=wserver_id)

    def upd_trash_cat(self, cat_id, name=None, active=None,
                      wserver_id=None):
        """
        Обновить категорию груза.

        :param cat_id: ID категории.
        :param name: Изменить имя.
        :param active: Изменить активность.
        :param wserver_id: Изменить WServer ID.
        :return:
        """
        self.execute_method('upd_trash_cat', cat_id=cat_id, name=name,
                            active=active, wserver_id=wserver_id)

    def add_trash_type(self, type_name, wserver_id, wserver_cat_id):
        """
        Добавить новый вид груза

        :param type_name: Название вида груза
        :param wserver_id: ID вида груза из GDB
        :param wserver_cat_id: ID категории груза из GDB, за которым закреплен
        вид груза
        :return:
            В случае успеха:
                {'status': 'success', 'info': [(*id: int*,)]}
            В случае провала:
                {'status': 'failed', 'info': Python Traceback}
        """
        self.execute_method('add_trash_type', type_name=type_name,
                            wserver_cat_id=wserver_cat_id,
                            wserver_id=wserver_id)

    def upd_trash_type(self, type_id, name=None, category=None, active=None,
                       wserver_id=None):
        """
        Обновить вид груза.

        :param type_id: ID вида груза.
        :param name: Изменить имя.
        :param category: Изменить категорию.
        :param active: Изменить активность.
        :param wserver_id: Изменить WServer ID.
        :return:
        """
        return self.execute_method('upd_trash_type', type_id=type_id,
                                   name=name, category=category, active=active,
                                   wserver_id=wserver_id)

    def add_operator(self, full_name, username, password, wserver_id):
        """
        Добавить нового пользователя (весовщика)

        :param full_name: Полное имя (ФИО)
        :param username: Логин пользователя
        :param password: Пароль пользователя
        :param wserver_id: его ID из базы GDB
        :return:
            В случае успеха:
                {'status': 'success', 'info': [(*id: int*,)]}
            В случае провала:
                {'status': 'failed', 'info': Python Traceback}
        """
        self.execute_method('add_operator', full_name=full_name,
                            username=username, password=password,
                            wserver_id=wserver_id)

    def upd_operator(self, user_id, username=None, password=None,
                     full_name=None, wserver_id=None, active=None):
        """
        Изменить данные весовщика (пользователя).

        :param user_id: ID весовщика (пользователя).
        :param username: Изменить логин.
        :param password: Изменить пароль.
        :param full_name: Изменить ФИО.
        :param wserver_id: Изменить wserver_id
        :param active:
        :return:
        """
        self.execute_method('upd_operator', user_id=user_id, username=username,
                            password=password, full_name=full_name,
                            wserver_id=wserver_id, active=active)

    def get_record_info(self, record_id: int):
        """
        Получить информацию о заезде по его ID

        :param record_id: ID записи
        :return:
            Если есть запись с таким ID:
                {ID: int, auto: auto_id, time_in: date, ...}
            Если же нет:
                None
        """
        self.execute_method('get_record_info', record_id=record_id)

    def get_auto_info(self, car_number: str = None, auto_id: int = None):
        """
        Вернуть информацию об авто по его гос.номеру

        :param auto_id: Идентификатор авто
        :param car_number: Гос. номер авто
        :return:
            В случае, если есть данные об авто:
                Возвращает словарь с данными
            В случае, если данных нет:
                Возвращает None
        """
        self.execute_method('get_auto_info', car_number=car_number,
                            auto_id=auto_id)

    def get_record_comments(self, record_id: int):
        """
        Вернуть все комментарии весовщика к данному заезду

        :param record_id: ID заезда
        :return: словарь, где ключ - название комментария,
            значение - его содержимое
        """
        self.execute_method('get_record_comments', record_id=record_id)

    def start_response_operator(self):
        """
        Запустить оператор ответов

        :return:
        """
        threading.Thread(target=self.response_operator,
                         args=(self.resp_operator_dict,)).start()

    def block_external_photocell(self):
        """
        Заблокировать внешний фотоэлемент

        :return:
        """
        self.execute_method('block_external_photocell')

    def unblock_external_photocell(self):
        """
        Разблокировать внешний фотоэлемент

        :return:
        """
        self.execute_method('unblock_external_photocell')

    def block_internal_photocell(self):
        """
        Заблокировать внутренний фотоэлемент

        :return:
        """
        self.execute_method('block_internal_photocell')

    def unblock_internal_photocell(self):
        """
        Разблокировать внутренний фотоэлемент

        :return:
        """
        self.execute_method('unblock_internal_photocell')

    def delete_record(self, record_id: str):
        """
        Удалить заезд

        :param record_id: Идентификатор заезда
        :return:
        """
        self.execute_method('delete_record', record_id=record_id)

    def get_wserver_id(self, table_name, wdb_id):
        """
        Извлечь wserver_id записи по его id.

        :param table_name: Название таблицы.
        :param wdb_id: ID искомых данных.
        :return:
        """
        self.execute_method('get_wserver_id', table_name=table_name,
                            wdb_id=wdb_id)

    def response_operator(self, function_dist):
        """
        Обработчик ответов от GCore. Запускается параллельным потоком.

        :param function_dist: словарь, где ключом является метод,
            который вернул ответ, а значением - какая то функция,
            которая должна такой ответ обработать.
            При этом функции передается весь этот ответ
        :return: возвращает результат выполнения функции в значении ключа
        """
        while self.resp_operator_dict:
            response = self.get_data()
            print("RESPONSE:", response)
            if not response:
                break
            if not isinstance(response, dict):
                continue
            response_method_name = response['core_method']
            if self.only_show_response:
                continue
            try:
                bound_function = function_dist[response_method_name]['method']
                if response['status']:
                    bound_function_result = bound_function(self,
                                                           **response['info'])
                    execution_result = bound_function_result
                else:
                    execution_result = response['info']
            except KeyError:
                error_msg = 'Не найден обработчик для ответов от метода {}.' \
                            '\n({})'
                execution_result = error_msg.format(response_method_name,
                                                    format_exc())
            print('Результат выполненения {}: {}'.format(response_method_name,
                                                         execution_result))
