"""Templates for emails."""

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
