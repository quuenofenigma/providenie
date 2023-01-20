"""Templates for emails."""
from string import Template


HTML_TEMPLATE_JOIN_FOND = Template(
    """
    <html>
        <body>
            <h1>Тестовое письмо от пользователя: $mother_fio</h1>
            <h2>Данные пользователя:</h2>
            <p><b>Программа фонда:</b> $programm</p>
            <p><b>ФИО мамы:</b> $mother_fio</p>
            <p><b>Телефон мамы:</b> $mother_phone</p>
            <p><b>Email мамы:</b> $mother_email</p>
            <p><b>ФИО ребёнка:</b> $child_fio</p>
            <p><b>Членов семьи:</b> $how_many_people</p>
            <p><b>Город:</b> $city</p>
            <p><b>Адрес:</b> $adress</p>
            <p><b>Дата рождения ребёнка:</b> $child_birthday</p>
            <p><b>Место рождения ребёнка:</b> $place_birth</p>
            <p><b>Срок рождения:</b> $birth_date</p>
            <p><b>Вес ребёнка:</b> $weight</p>
            <p><b>Рост ребёнка:</b> $height</p>
            <p><b>Диагнозы:</b> $dizgnozes</p>
            <p><b>Дата обращения:</b> $date_aplication</p>
            <p><b>Как узнали о нас:</b> $how_about_us</p>
            <p><b>В каких фондах оформлены:</b> $fond_now</p>
            <p><b>Какие фонды помогали ранее:</b> $fond_early</p>
        </body>
    </html>"""
)

HTML_TEMPLATE_JOIN_FOND_ERROR = Template(
    """
    <html>
        <body>
            <h1>Ошибка</h1>
            <p><b>$error</b></p>
        </body>
    </html>"""
)

VOLUNTEER_DATA_SUBJECT = "Новый волонтёр"
HTML_VOLUNTEER_DATA = """
    <html>
        <body>
            <h1>{}</h1>
            <p>
                ФИО: <b>{}</b><br/>
                Дата рождения: <b>{}</b><br/>
                Город проживания: <b>{}</b><br/>
                Телефон: <b>{}</b><br/>
                Почта: <b>{}</b><br/>
                Вариант помощи: <b>{}</b>
            </p>
        </body>
    </html>
"""


"""Templates for messages."""

MSG_VOLUNTEER_DATA = (
    "Ф.И.О. - <b><i>{}</i></b>\n"
    "Дата рождения - <b><i>{}</i></b>\n"
    "Город - <b><i>{}</i></b>\n"
    "Телефон - <b><i>{}</i></b>\n"
    "Email - <b><i>{}</i></b>\n"
    "Сообщение - <b><i>{}</i></b>\n"
)
MSG_QUESTION_DATA = (
    "Ваше имя - <b><i>{}</i></b>\n"
    "Тема вопроса - <b><i>{}</i></b>\n"
    "Вопрос - <b><i>{}</i></b>\n"
)
MSG_QUESTION_TO_CURATOR = (
    "От пользователя <b><i>{}</i></b> \n"
    "поступил вопрос на тему <b><i>{}</i></b>.\n"
    "{}\n"
)
