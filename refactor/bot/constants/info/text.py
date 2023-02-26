
"""MAIN MENU"""
START = (
    "Здравствуйте! Добро пожаловать!"
    "\n\nЯ бот - помощник благотворительного фонда «Провидение»."
    "Мы помогаем детям, родившимся раньше срока, лучше видеть, слышать и разговаривать, а также поддерживаем их родителей."
    "\n\nНаша миссия – спасти зрение детей, помочь им избежать инвалидности и улучшить качество жизни их семей."
    "\n\nДля того, чтобы оставаться в курсе последних новостей, рекомендуем Вам подписаться на наши страницы в социальных сетях: "

    "\n\n<a href='https://www.google.com/'>Сайт благотворительного фонда “Провидение”</a>"
    "\n<a href='https://www.facebook.com/fond.providenie/'>Группа в Facebook</a>"
    "\n<a href='https://vk.com/fond_providenie '>Группа Вконтакте</a>"
    "\n<a href='https://zen.yandex.ru/fond_providenie'>Наша страница на Яндекс.Дзен</a>"
    "\n<a href='https://t.me/providenie_fond'>Новостной канал Telegram</a>"
    "\n<a href='https://www.instagram.com/fond_providenie/'>Наша страница в Instagram</a>"
    "\n<a href='https://dobro.mail.ru/funds/blagotvoritelnyij-fond-pomoschi-nedonoshennyim-detyam-i-ih-semyam-providenie-2/'>Наша страница на Mail.ru</a>"
    "\n<a href='https://youtube.com/channel/UC_co5lBatw_pA2DceKCqZfg'>Наш канал на Youtube</a>"
)
STOP = "До скорых встреч!"

MAIN_MENU = (
    "Фонд помогает всем детям с нарушениями зрения "
    "независимо от места рождения и поддерживает семьи, "
    "где растут дети с инвалидностью."
)


"""MENU DESCRIPTIONS"""
SELECT_EDIT = "Выберите для редактирования:"
IN_PROGRESS = "В разработке"
ABOUT = "Информация о фонде"
SELECT_URL = "Выберите интересующую вас соцсеть/страницу"


"""MAIN BUTTONS"""
BACK = "Назад"
OPTION_URL = "Перейти"
START_FILL_FORM = "Начать заполнение анкеты"
SEND_FORM = "Подтвердить и отправить"
EDIT_FORM = "Редактировать"



SHOW_DATA_TEMPLATE = '<b><u>{title}</u></b>:\n{value}\n\n'
INPUT_ERROR_TEMPLATE = '<b>Некорректные введенные данные!</b>\n\n<b>Пример:</b> \n{hint}'
DATE_TEMPLATE = '%d.%m.%Y'


REQUIRED_DOCUMENTS = """\n
Необходимые документы:\n
- Справка о многодетности, малообеспеченности, инвалидности (фото)\n
- Справка 2 НДФЛ родителей или любая форма справки, подтверждающая ДОХОД РОДИТЕЛЕЙ\n
- Выписка с рекомендациями (фото/скан)\n
- Свидетельство о рождении (фото/скан)\n
- Паспорт (фото/скан)\n
- Счёт на лечение (какое лечение требуется, стоимость) или ссылка на то, что необходимо приобрести\n
"""
