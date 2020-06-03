
FIRST_TEXT_USER = 'Привет. Теперь я смогу предупреждать тебя о дежурствах'
NEW_TIME_COMMAND = '/inform_me'
DELAY_TIME_MESSAGE = 'Я тебя предупреждаю за {minutes} минут.\n\n'\
                    f'Напиши мне {NEW_TIME_COMMAND} и количество минут до начала смены для установки нового времени\n '\
                    '\nВот готовые комманды:'\
                    f'\n\n{NEW_TIME_COMMAND}60 - за 1 час'\
                    f'\n\n{NEW_TIME_COMMAND}120 - за 2 часа'\
                    f'\n\n{NEW_TIME_COMMAND}180 - за 3 часа'\
                    f'\n\n{NEW_TIME_COMMAND}240 - за 4 часа'\
                    f'\n\n{NEW_TIME_COMMAND}300 - за 5 часа'\

FIRST_TEXT_ADMIN = ''' Комманды для администратора\n
/edit - удалить учасника со смены'''

NOTIFIER = '‼️‼️‼️‼️‼️‼️‼️\n'\
            'Ваша смена через {diff} минут'

ENTER_PASWORD = 'Введите пароль чтоб стать администратором'

COMMAND_NEW_ONLY_ADMIN = 'Комманда /new только для администраторов'
COMMAND_EDIT_ONLY_ADMIN = 'Комманда /edit только для администраторов'
COMMAND_DUTY_LIST_ONLY_ADMIN = 'Комманда /duty_list только для администраторов'
PASSWORD = '8321'

EMPTY = '/FREE'

REMOVE = '/remove'

DAY_EMPTY = '-----------\n'\
            '‼️{date}🔥\n'\
            '{day_week}({time_day})\n'\
            '👉{user}👈\n'

DAY_BOOK = '-----------\n'\
            '{date}\n'\
            '{day_week}({time_day})\n'\
            '{user}\n'

DAY_EDIT = '-----------\n'\
            '{date} {remove}\n'\
            '{day_week}({time_day})\n'\
            '{user}\n'

DAY_NEXT =  'Следующее дежурство:\n\n'\
            'Дата: {date} \n'\
            '{day_week}({time_day})\n'\
            'Участник: {user}\n'

NO_LEFT_DAYS = 'В этом месяце нет смен'
NO_BUSY_DAYS = 'В этом месяце нет занятых смен'
ACTUAL_SCHEDULE = '‼️Список утверденных дежурств:‼️'
WRITE_PRIVATE = '👇{} напиши мне в личку /start👇\n@{} ✍️'

NEW_DAY = '😀Дежурство на {}({}) закрепил за тобой👍👍'

AVALIBLE_DAYS = '💥Есть свободные смены💥\n'

NO_AVALIBLE_DAYS = '👌Все смены заняты👌\n'

DELETED_DAY = 'Дежурство удалено'

YOUR_DAY_AVALIBLE = 'Ваше дежурство {date} {week_day}({time_day}) отменено.'

NEW_DAY_AVALIBLE = '‼️‼️Освободилось Дежурство‼‼️'

MONTH_AVALIBLE = 'Новый месяц доступен для выбора'

ADD_CHAT = 'Напишите что-то в чате'

DB_NAME = 'Information.json'

SECRET = 'iouasidf'

URL = f'https://scedulebot.pythonanywhere.com/{SECRET}'

TOKEN = '1219221993:AAE8xu81t1YB-0jJV9NFDJ1zcFj_QRyskGw'

ARKADY_ID = 422791122

DEFAULT_DELAY = 120 # minutes

MORNING = 'Утро'

EVENING = 'Вечер'

TIME_DAY =({
    MORNING: '7.00',
    EVENING: '21.00',
}, {
    MORNING: '7.00',
    EVENING: '18.00',
})

WORK_DAYS = (
    (2, EVENING),
    (4, EVENING),
    (6, MORNING),
    (6, EVENING)
)


BOT_INFO = {
            'chat_id' : None,
            'pin_id' : None,
            'new_month': False,
            'days': [],
            'users': [],
            'admins': [],
        }

def time_day(time):
    if time.hour > 15:
        return 'Вечер'
    else :
        return 'Утро'

def day_week_str(day_week) -> str:
    if day_week == 0:
        return 'Понедельник'
    elif day_week == 1:
        return 'Вторник'
    elif day_week == 2:
        return 'Среда'
    elif day_week == 3:
        return 'Четверг'
    elif day_week == 4:
        return 'Пятница'
    elif day_week == 5:
        return 'Суббота'
    elif day_week == 6:
        return 'Воскресенье'
    assert False, 'Day out of range'



