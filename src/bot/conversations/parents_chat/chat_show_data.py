from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot import states


async def chat_show_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение всех введённых данных для вступления в чат"""
    user_data = context.user_data
    data = user_data.get(states.FEATURES)
    if not data:
        text = "\nДанных нет.\n"
    else:
        text = (
            f'ФИО родителя (опекуна)\n {data.get(states.CHAT_PARENTS_NAME, "-")}\n'
            f'Номер телефона родителя(опекуна)\n {data.get(states.CHAT_PARENTS_PHONE, "-")}\n'
            f'ФИО ребенка\n {data.get(states.CHAT_CHILD_NAME, "-")}\n'
            f'Дата рождения ребенка\n {data.get(states.CHAT_CHILD_BIRTHDAY, "-")}\n'
            f'Место рождения ребенка\n {data.get(states.CHAT_CHILD_PLACE_BIRTHDAY, "-")}\n'
            f'Срок беременности рождения ребенка\n {data.get(states.CHAT_CHILD_TERM, "-")}\n'
            f'Вес при рождении\n {data.get(states.CHAT_CHILD_WEIGHT, "-")}\n'
            f'Рост при рождении\n {data.get(states.CHAT_CHILD_HEIGHT, "-")}\n'
            f'Диагнозы\n {data.get(states.CHAT_CHILD_DIAGNOSE, "-")}\n'
            f'Операции\n {data.get(states.CHAT_CHILD_OPERATION, "-")}\n'
            f'Дата обращения\n {data.get(states.CHAT_DATE_ADDRESS, "-")}\n'
            f'Как узнали о фонде\n {data.get(states.CHAT_ABOUT_FOND, "-")}\n'
        )

    buttons = [
        [
            InlineKeyboardButton(
                text="Редактировать", callback_data=str(states.CHAT_DATA_EDIT)
            )
        ],
        [
            InlineKeyboardButton(
                text="Отправить", callback_data=str(states.CHAT_SEND)
            )
        ],
        [
            InlineKeyboardButton(
                text="Список чатов", callback_data=str(states.END)
            )
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    state = context.user_data.get(states.START_OVER)
    if state:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        await update.message.reply_text(text=text, reply_markup=keyboard)
    user_data[states.START_OVER] = False
    return states.CHAT_SHOWING
