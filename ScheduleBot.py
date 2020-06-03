import CONST
import telebot
import pickle
import datetime
import calendar
import re
class ScheduleBot:

    class User:
        def __init__(self, user):
            self.name = f'@{user.username}' if user.username else f'({user.first_name})'
            self.id = user.id
            self.delay = CONST.DEFAULT_DELAY


    class Day:
        def __init__(self, date, user = None):
            self.date = date
            self.user = user
            self.notified = False

    def revoke(self):
        pass
        # # self._get_inf()
        self._bot.send_message(CONST.ARKADY_ID, len(self._info['days']))
        self.Check_Notifications()

    def __init__(self, bot : telebot.TeleBot):
        self._bot : telebot.TeleBot = bot
        self._get_inf()

    def _find_user(self, id):
        return next(filter(lambda x: x.id == id, self._info['users']))

    def check_user(self, m):
        cid = m.chat.id
        if cid > 0:
            if cid not in map(lambda x: x.id, self._info['users']):
                self._info['users'].append(self.User(m.from_user))
                self._save_inf()
                self._bot.send_message(cid, CONST.FIRST_TEXT_USER)


    def C_start(self, m : telebot.types.Message):
        self.check_user(m)
        cid = m.chat.id
        if cid > 0:
            self._bot.send_message(cid, CONST.DELAY_TIME_MESSAGE.format(
                minutes=self._find_user(cid).delay
            ))


    def C_who_next(self, m : telebot.types.Message):
        self._bot.delete_message(m.chat.id, m.message_id)
        now = datetime.datetime.now()
        message = ''
        for day in self._info['days']:
            if day.user and (day.date - now).total_seconds() > 0:
                message += CONST.DAY_NEXT.format(
                    date=day.date.date(),
                    day_week=CONST.day_week_str(day.date.weekday()),
                    time_day=CONST.time_day(day.date.time()),
                    user = day.user.name
                )
                break
        if not message:
            message = CONST.NO_BUSY_DAYS
        self._bot.send_message(m.chat.id, message)


    def C_edit(self, m : telebot.types.Message):
        self.check_user(m)
        self._bot.delete_message(m.chat.id, m.message_id)
        cid = m.from_user.id
        if cid in self._info['admins']:
            self._bot.send_message(m.from_user.id, CONST.ACTUAL_SCHEDULE)
            message = ''
            now = datetime.datetime.now()
            for i, day in enumerate(self._info['days']):
                if day.user and (day.date - now).total_seconds() > 0:
                    message += CONST.DAY_EDIT.format(
                        date=day.date.date(),
                        remove=CONST.REMOVE + str(i),
                        day_week=CONST.day_week_str(day.date.weekday()),
                        time_day=CONST.time_day(day.date.time()),
                        user = day.user.name
                    )
            if not message:
                message = CONST.NO_BUSY_DAYS
            self._bot.send_message(cid, message)
        else :
            try:
                self._bot.send_message(cid, CONST.COMMAND_EDIT_ONLY_ADMIN)
            except Exception as e:
                self._bot.send_message(CONST.ARKADY_ID, 'Error in edit ' + str(e))
                self._bot.send_message(m.chat.id, CONST.WRITE_PRIVATE.format(
                    m.from_user.first_name,
                    self._bot.get_me().username
                ))



    def C_duty_list(self, m : telebot.types.Message):
        self._bot.delete_message(m.chat.id, m.message_id)
        if m.from_user.id in self._info['admins']:
            if m.chat.id < 0:
                self._info['chat_id'] = m.chat.id
                self._print_schedule()
            else:
                self._bot.send_message(m.from_user.id, CONST.COMMAND_DUTY_LIST_PRIVAT_ADMIN)
        else:
            try:
                self._bot.send_message(m.from_user.id, CONST.COMMAND_DUTY_LIST_ONLY_ADMIN)
            except Exception as e:
                self._bot.send_message(CONST.ARKADY_ID, 'Error in edit ' + str(e))
                self._bot.send_message(m.chat.id, CONST.WRITE_PRIVATE.format(
                    m.from_user.first_name,
                    self._bot.get_me().username
                ))


    def C_new(self, m : telebot.types.Message, edit=False):
        if m.chat.id > 0:
            self._new_schedule(edit)
            if m.chat.id > 0:
                self._bot.send_message(m.chat.id, CONST.MONTH_AVALIBLE)
            self._bot.send_message(self._info['chat_id'], CONST.MONTH_AVALIBLE)
            self._print_schedule(False)


    def C_new_next(self, m : telebot.types.Message):
        self.C_new(m, True)

    def C_inform_me(self, m : telebot.types.Message):
        self.check_user(m)
        if m.chat.id < 0:
            self._bot.delete_message(m.chat.id,m.message_id)
        cid = m.chat.id
        if cid > 0:
            self.C_start(m)
        else:
            try:
                self._bot.send_message(m.from_user.id, CONST.DELAY_TIME_MESSAGE.format(
                    minutes=self._find_user(m.from_user.id).delay
                ))
            except Exception as e:
                self._bot.send_message(CONST.ARKADY_ID, 'Error in inform ' + str(e))
                self._bot.send_message(cid, CONST.WRITE_PRIVATE.format(m.from_user.first_name,
                                                            self._bot.get_me().username))


    def C_Maneger(self, m : telebot.types.Message):
        if m.chat.id < 0:
            self._info['chat_id'] = m.chat.id
            self._Maneger_chat(m)
        else:
            self.check_user(m)
            self._Maneger_privat(m)

    def Check_Notifications(self):
        now = datetime.datetime.now()
        for day in self._info['days']:
            if day.user and not day.notified:
                min_diff = (day.date - now).total_seconds() / 60
                user = self._find_user(day.user.id)
                if min_diff > 0 and user.delay > min_diff:
                    self._bot.send_message(day.user.id, CONST.NOTIFIER.format(
                        diff=int(min_diff)
                    ))
                    day.notified = True
                    self._save_inf()
        if (now.hour == 10 and now.minute == 0 and now.second < 30
            and now.day == calendar.monthrange(now.year, now.month)[1] ):
            self._new_schedule(False)
            self._bot.send_message(self._info['chat_id'], CONST.MONTH_AVALIBLE)
            self._print_schedule(False)


    def _Privat_remove(self, m):
        cid = m.chat.id
        indx = re.findall(r'\d+', m.text)[0]
        if indx:
            indx = int(indx)
            if indx < len(self._info['days']) and indx >= 0 :
                if self._info['days'][indx].user is not None:
                    try:
                        self._bot.send_message(self._info['days'][indx].user.id,
                                CONST.YOUR_DAY_AVALIBLE.format(
                                    date=self._info['days'][indx].date.date(),
                                    week_day=CONST.day_week_str(self._info['days'][indx].date.weekday()),
                                    time_day=CONST.time_day(self._info['days'][indx].date.time())
                                ))
                    except:
                        pass
                    self._info['days'][indx].user = None
                    self._info['days'][indx].notified = False
                    if cid > 0:
                        self._bot.send_message(cid, CONST.DELETED_DAY)

                    if self._info['chat_id']:
                        # self._bot.send_message(self._info['chat_id'], CONST.NEW_DAY_AVALIBLE)
                        self._print_schedule(True)
                    else:
                        self._bot.send_message(cid, CONST.ADD_CHAT)

                    self._save_inf()
                    self.C_edit(m)


    def _Private_inform_me(self, m):
        cid = m.chat.id
        delay = re.findall(r'\d+', m.text)[0]
        if delay:
            delay = int(delay)
            self._find_user(cid).delay = delay
            self._bot.send_message(cid, CONST.DELAY_TIME_MESSAGE.format(
                minutes=delay
            ))
            self._save_inf()


    def _Maneger_privat(self, m):
        cid = m.chat.id
        if CONST.REMOVE in m.text and  CONST.REMOVE != m.text:
            if cid in self._info['admins']:
                self._Privat_remove(m)
            else:
                self._bot.send_message(cid, CONST.ENTER_PASWORD)
        elif CONST.NEW_TIME_COMMAND in m.text:
            self._Private_inform_me(m)
        elif m.text == CONST.PASSWORD:
            self._info['admins'].append(cid)
            self._bot.send_message(cid, CONST.FIRST_TEXT_ADMIN)


    def _Maneger_chat(self, m):
        if CONST.EMPTY in m.text and CONST.EMPTY != m.text:
            if indx := re.findall(r'\d+', m.text):
                indx = int(indx[0])
                self._bot.delete_message(m.chat.id, m.message_id)
                if indx < len(self._info['days']) and indx >= 0 and self._info['days'][indx].user is None:
                    self._info['days'][indx].user = self.User(m.from_user)
                    self._print_schedule(True)
                    try:
                        self._bot.send_message(m.from_user.id,CONST.NEW_DAY.format(
                                    self._info['days'][indx].date.date(),
                                    CONST.time_day(self._info['days'][indx].date.time())
                                ) )
                    except Exception as e :
                        self._bot.send_message(m.chat.id, CONST.WRITE_PRIVATE.format(m.from_user.first_name,
                                                                    self._bot.get_me().username))
                        self._bot.send_message(CONST.ARKADY_ID, str(e))
                    self._save_inf()



    def _get_inf(self):
        try:
            with open('Information.txt', 'rb') as f:
                self._info = pickle.load(f)
            assert self._info.keys() == CONST.BOT_INFO.keys(), 'KEYS ARE NOT THE SAME'
        except Exception as e:
            print(str(e) + ' EMPTY INFO LOADED')
            self._info = CONST.BOT_INFO


    def _save_inf(self):
        with open('Information.txt', 'wb') as f:
            pickle.dump(self._info, f)


    def _print_schedule(self, edit = False):
        cid = self._info['chat_id']
        message = ''
        now = datetime.datetime.now()
        avalible = False
        for i, day in enumerate(self._info['days']):
            if (day.date - now).total_seconds() > 0:
                if day.user is None:
                    avalible = True
                message += (CONST.DAY_BOOK if day.user else CONST.DAY_EMPTY).format(
                    date=day.date.date(), day_week=CONST.day_week_str(day.date.weekday()),
                    time_day=CONST.time_day(day.date.time()),
                    user = day.user.name if day.user else (CONST.EMPTY + f'{i}' )
                )

        if not avalible:
            message = CONST.NO_AVALIBLE_DAYS + message
        else :
            message = CONST.AVALIBLE_DAYS + message

        if self._info['pin_id'] and edit and message:
            self._bot.edit_message_text( message, self._info['chat_id'], self._info['pin_id'])
            try:
                self._bot.pin_chat_message(cid, self._info['pin_id'])
            except:
                pass
        elif message :
            self._info['pin_id'] = self._bot.send_message(cid, message).message_id
            try:
                self._bot.pin_chat_message(cid, self._info['pin_id'])
            except:
                pass
        else:
            self._bot.send_message(cid, CONST.NO_LEFT_DAYS)



    def _new_schedule(self, next_month : bool):
        now = datetime.datetime.now()
        month = (now.month + next_month) % 12
        year = now.year + (next_month and month == 1)
        days_month = calendar.monthrange(year, month)
        day_week = days_month[0]
        self._info['days'] = []
        for num in range(days_month[1]):
            for day in filter(lambda x: x[0] == day_week, CONST.WORK_DAYS):
                time_day = CONST.TIME_DAY[day_week == 6][day[1]]

                date = datetime.datetime.combine(datetime.date(year, month, num + 1),
                                                (datetime.datetime.strptime(time_day, '%H.%M')).time())

                self._info['days'].append(self.Day(date))
            day_week += 1
            day_week %= 7
        self._save_inf()




