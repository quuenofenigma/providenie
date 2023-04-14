from datetime import datetime as dt

from bot.constants import key
from . import option


COMMON_QUESTIONS = {
    'FULL_NAME': {
        key.TITLE: 'ФИО',
        key.TEXT: 'Введите фамилию, имя и отчество',
        key.HINT: (
            'Пожалуйста, введите ФИО, например: Иванова Мария '
            'или Иванова Мария Петровна.'
        )
    },
    'PHONE': {
        key.TITLE: 'Номер телефона',
        key.TEXT: 'Введите контактный номер телефона',
        key.HINT: (
            'Пожалуйста, введите номер телефона, например: +7ххххххххх.'
        ),
    },
    'EMAIL': {
        key.TITLE: 'Электронная почта',
        key.TEXT: 'Введите электронную почту',
        key.HINT: (
            'Пожалуйста, введите электронную почту, '
            'например: my_address@mail.ru'
        ),
    },
    'CITY': {
        key.TITLE: 'Город',
        key.TEXT: 'Введите город проживания',
        key.HINT: (
            'Пожалуйста, введите город проживания, например: Ростов'
        ),
    },
    'FAMILY_MEMBERS': {
        key.TITLE: 'Тип семьи',
        key.TEXT: 'Укажите тип семьи (полная/неполная)',
        key.HINT: (
            'Пожалуйста, укажите тип семьи, например: полная'
        ),
    },
    'WHERE_GOT_INFO': {
        key.TITLE: 'Как узнали о Фонде',
        key.TEXT: 'Как Вы узнали о нашем Фонде?',
        key.HINT: (
            'Пожалуйста, укажите как Вы узнали о нашем Фонде, '
            'например: увидел информационный пост на Яндекс Дзен'
        ),
    },
    'ADDITIONAL_CHATS': {
        key.TITLE: 'Дополнительные чаты',
        key.TEXT: (
            'В какие ещё чаты Вы хотели бы вступить?'
            '\nСписок возможных чатов для вступления:\n- ' +
            '\n- '.join([chat.get(key.BUTTON_TEXT) for chat in option.CHAT.values()])
        ),
        key.HINT: (
            'Пожалуйста, укажите, В какие ещё чаты Вы хотели бы вступить, '
            'например: Да, хочу вступить в "Смотри на мир", "Дети с гидроцефалией"'
        ),
    }
}

VOLUNTEER_QUESTIONS = {
    'BIRTHDAY': {
        key.TITLE: 'Дата рождения',
        key.TEXT: 'Введите дату рождения',
        key.HINT: 'Пожалуйста, введите дату рождения, например: '
        f'{dt.now().strftime("%d.%m")}.{dt.now().year - 16}',
    },
    'VOLUNTEER_HELP': {
        key.TITLE: 'Предлагаемая помощь',
        key.TEXT: (
            'Вы можете предложить свой вариант помощи'
            '\n\nВозможные варианты помощи: '
            '\n— творческие мастер-классы с детьми; '
            '\n— фото и видеосъемка мероприятий; '
            '\n— автоволонтерство; '
            '\n— занятия с детьми по школьной программе; '
            '\n— помощь с документами; '
            '\n— курьерские услуги; '
            '\n— Ваш вариант.'
        ),
        key.HINT: (
            'Пожалуйста, укажите, какую помощь Вы можете предложить?'
            '\nПример: могу оказать помощь в транспортировке, '
            'есть машина легкового типа'
        ),
    },
    'VOLUNTEER_TIME': {
        key.TITLE: 'Количество уделяемого времени',
        key.TEXT: 'Как часто Вы сможете уделять время волонтерству?',
        key.HINT: (
            'Пожалуйста, укажите сколько времени Вы сможете уделять '
            'волонтерству.'
            '\nПример: 5 часов в неделю.'
        )
    }
}

ASK_QUESTIONS = {
    'QUESTION': {
        key.TITLE: 'Вопрос',
        key.TEXT: 'Введите Ваш вопрос',
        key.HINT: (
            'Пожалуйста, введите Ваш вопрос, '
            'например: в какой фонд я могу обратиться, '
            'если моему ребенку нужна консультация офтальмолога?'
        ),
    },
}

LONG_QUESTIONS = {
    'PARENT_FULL_NAME': {
        key.TITLE: 'ФИО родителя',
        key.TEXT: 'Введите фамилию, имя и отчество родителя или опекуна',
        key.HINT: (
            'Пожалуйста, введите ФИО, например: Иванова Мария или '
            'Иванова Мария Петровна.'
        ),
    },
    'CHILD_FULL_NAME': {
        key.TITLE: 'ФИО ребенка',
        key.TEXT: 'Введите фамилию, имя и отчество ребенка',
        key.HINT: (
            'Пожалуйста, введите ФИО, например: Иванова Мария или '
            'Иванова Мария Петровна.'
        ),
    },
    'CHILD_BIRTHDAY': {
        key.TITLE: 'Дата рождения ребенка',
        key.TEXT: 'Введите дату рождения ребенка',
        key.HINT: (
            'Пожалуйста, введите дату рождения, например: 09.03.2023'
        ),
    },
    'CHILD_BIRTH_PLACE': {
        key.TITLE: 'Место рождения ребенка',
        key.TEXT: 'Введите место рождения ребенка',
        key.HINT: (
            'Пожалуйста, введите место рождения ребенка, '
            'например: Челябинск',
        )
    },
    'CHILD_BIRTH_DATE': {
        key.TITLE: 'Срок беременности при рождении ребенка',
        key.TEXT: 'На каком сроке родился ребёнок (полных недель)?',
        key.HINT: (
            'Пожалуйста, введите срок рождения ребенка в неделях, например 35'
        ),
    },
    'CHILD_BIRTH_WEIGHT': {
        key.TITLE: 'Вес ребенка при рождении',
        key.TEXT: 'Введите в граммах вес ребенка при рождении',
        key.HINT: (
            'Пожалуйста, введите вес ребенка в граммах, например: 3000'
        ),
    },
    'CHILD_BIRTH_HEIGHT': {
        key.TITLE: 'Рост ребенка при рождении',
        key.TEXT: 'Введите рост ребенка при рождении',
        key.HINT: (
            'Пожалуйста, введите рост ребенка в см, например: 40'
        ),
    },
    'CHILD_DIAGNOSIS': {
        key.TITLE: 'Диагнозы ребенка',
        key.TEXT: (
            'Введите диагнозы ребенка на момент обращения'
        ),
        key.HINT: (
            'Пожалуйста, введите диагнозы ребенка, например, '
            'тугоухость 2ой степени, косоглазие, нистагм'
        ),
    },
}

FUND_QUESTIONS = {
    'ADDRESS': {
        key.TITLE: 'Адрес',
        key.TEXT: 'Введите адрес проживания',
        key.HINT: (
            'Пожалуйста, введите адрес проживания, '
            'например: Ростов, ул. Моравского, д.6, кв. 1'
        ),
    },
    'REQUIRED_THERAPY': {
        key.TITLE: 'Требуемое лечение',
        key.TEXT: (
            'Какое лечение требуется и какая стоимость лечения?'
            '\nТакже можно указать ссылку '
            'на техническое средство реабилитации, '
            'которое необходимо приобрести'
        ),
        key.HINT: (
            'Пожалуйста, укажите требуемое лечение, '
            'например: Шунтирование'
        ),
    },
    'REQUEST_GOAL': {
        key.TITLE: 'Цель обращения',
        key.TEXT: 'Опишите кратко Вашу ситуацию с указанием цели обращения',
        key.HINT: (
            'Пожалуйста, укажите цель обращения, '
            'например: Обратился, потому что ...'
        ),
    },
    'SOCIAL_NETWORKS': {
        key.TITLE: 'Cоциальные сети',
        key.TEXT: 'Введите ссылку на Вашу страницу в социальных сетях',
        key.HINT: (
            'Пожалуйста, введите ссылку на Вашу страницу в социальных сетях, '
            'например: vk.com/fond_providenie"'
        ),
    },
    'PARENTS_WORK_PLACE': {
        key.TITLE: 'Место работы родителей',
        key.TEXT: 'Введите место работы родителей',
        key.HINT: (
            'Пожалуйста, введите место работы родителей, '
            'например: ОАО "Корпорация"'
        ),
    },
    'ANOTHER_FUND_MEMBER': {
        key.TITLE: 'Состоите ли в другом фонде',
        key.TEXT: (
            'Оформлены ли Вы в данный момент в каком-либо другом фонде? '
            '\nКакие фонды помогали Вам ранее?'
        ),
        key.HINT: (
            'Пожалуйста, укажите, оформлены ли Вы в данный момент в '
            'каком-либо другом фонде и какие фонды помогали Вам ранее, '
            'например: Да, Фонд «Название Фонда»'
        ),
    },
}

ALL_QUESTIONS = {
    **COMMON_QUESTIONS,
    **VOLUNTEER_QUESTIONS,
    **ASK_QUESTIONS,
    **LONG_QUESTIONS,
    **FUND_QUESTIONS,
}
