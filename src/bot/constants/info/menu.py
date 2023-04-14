from bot.constants import key
from bot.constants.info import option, text
from bot.conversations.models import (
    AskQuestionForm,
    ChatForm,
    FundForm,
    VolunteerForm,
)


ALL_MENU = {
    f"{key.MENU}_CHAT": {
        key.NAME: "Вступление в чат",
        key.BUTTON_TEXT: "Хочу попасть в родительский чат",
        key.DESCRIPTION: "Выберите чат для вступления:",
        key.MODEL: ChatForm,
        key.OPTIONS: option.CHAT,
        key.RESPONSE: (
            "Спасибо за ваши ответы!"
            "\nВаша заявка отправлена. Координатор Фонда свяжется "
            "с Вами в течение 3 рабочих дней после рассмотрения заявки."

        ),
    },
    f"{key.MENU}_FOND": {
        key.NAME: "Заявка на помощь",
        key.BUTTON_TEXT: "Подать заявку в Фонд",
        key.DESCRIPTION: "Выберите программу Фонда:",
        key.MODEL: FundForm,
        key.OPTIONS: option.FUND,
        key.RESPONSE: (
            "Спасибо за ваши ответы!"
            "\nВаша заявка отправлена. Координатор Фонда свяжется "
            "с Вами в течение 7 рабочих дней."
            f"\n{text.REQUIRED_DOCUMENTS}"
        ),
    },
    f"{key.MENU}_VOLONTEER": {
        key.NAME: "Заявка на волонтёрство",
        key.BUTTON_TEXT: "Хочу стать волонтёром",
        key.DESCRIPTION: (
            "Далее необходимо предоставить "
            "информацию для координатора"
        ),
        key.MODEL: VolunteerForm,
        key.RESPONSE: (
            "Спасибо за ваши ответы!"
            "\nВаша заявка отправлена."
            "\nТелефон для связи с координатором Фонда +79169814619 (Юлия)"
        ),
    },
    f"{key.MENU}_ASK_QUESTION": {
        key.NAME: "Вопрос пользователя",
        key.BUTTON_TEXT: "Задать вопрос",
        key.DESCRIPTION: "Чтобы задать вопрос, заполните, пожалуйста, нашу анкету",
        key.MODEL: AskQuestionForm,
        key.RESPONSE: (
            "Ваш вопрос успешно отправлен!"
            "\nНаш координатор свяжется с Вами в течение 3 рабочих дней."
        ),
    },
    f"{key.MENU}_SHARE": {
        key.BUTTON_TEXT: "Рассказать о Фонде своим друзьям",
        key.DESCRIPTION: text.SHARE
    },
    f"{key.MENU}_DONATION": {
        key.BUTTON_TEXT: "Отчёты и пожертвования",
        key.DESCRIPTION: "Сделать пожертвование",
        key.OPTIONS: option.DONATION,
    },
    f"{key.MENU}_EVENT": {
        key.BUTTON_TEXT: "Наши события",
        key.DESCRIPTION: (
            "Вы можете ознакомиться с ключевыми событиями "
            "Фонда, перейдя по ссылке ниже"
            "\n<a href='https://fond-providenie.ru/news/'>"
            "Ссылка на страницу с ключевыми событиями фонда</a>"
        ),
    },
    f"{key.MENU}_ABOUT": {
        key.BUTTON_TEXT: "О Фонде",
        key.DESCRIPTION: (
            "Благотворительный Фонд \"Провидение\" был создан в "
            "2018 году родителями недоношенного ребенка и стал "
            "первым оперативно и комплексно помогать при угрозе "
            "отслойки сетчатки глаз при ретинопатии недоношенных, "
            "когда лечения по ОМС недостаточно."
            "\nСегодня Фонд помогает всем детям с нарушениями "
            "зрения независимо от места рождения, а также поддерживает"
            " семьи, где растут дети, рожденные раньше срока."
            "\nНаша миссия – спасти зрение детей, помочь им "
            "избежать инвалидности и улучшить качество жизни их семей."
            "\nПодробнее ознакомиться с деятельностью Фонда можно, "
            "перейдя по ссылке:"
            "\n<a href='https://fond-providenie.ru/about/'>"
            "Ссылка на раздел \"О нас\"</a>"
            "\n\nКонтакты для связи:"
            "\nE-mail: info@fond-providenie.ru"
            "\nТелефон: +7 985 431 56 76, +7 927 120 33 75"
            "\n\n<a href='https://fond-providenie.ru/'>"
            "Сайт Благотворительного Фонда</a>"
        ),
        key.OPTIONS: option.ABOUT,
    },
    f"{key.MENU}_PARTNER": {
        key.BUTTON_TEXT: "Стать партнером",
        key.DESCRIPTION: (
            "Благотворительный Фонд «Провидение» открыт для сотрудничества! "
            "\n\nЕсли Вы заинтересованы во взаимодействии в рамках любого из "
            "наших проектов или хотите предложить спецпроект – свяжитесь "
            "с нашим сотрудником по работе с партнерами Ириной Пшеничниковой."
            "\n\nКонтакты для связи:"
            "\nE-mail: i.pshenichnikova@fond-providenie.ru"
            "\nТелефон: +79031397876"
        ),
    },
}
