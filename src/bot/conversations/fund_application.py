# Логика "Заявка на вступление в фонд" без хендлеров
from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from ..constans import fund_app_callbacks as fund_callbacks
from ..constans import fund_app_constans as constans
from ..constans import fund_app_states as fund_states
from ..templates import HTML_TEMPLATE_JOIN_FUND
from ..validators import fund_app_validators as validators
from .menu import start
from bot import keys, states
from core.email import bot_send_email_to_curator
from core.logger import logger


END = ConversationHandler.END


# Подпрограммы
def clean_dictionary(context: dict, save_values=[None]) -> None:
    """Очистка словаря."""
    for key in context:
        if key not in save_values:
            context[key] = ""


# Здесь начинаются обработчики кнопок и ответов на вопросы
async def application_to_the_fund(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вывод кнопок программ фонда."""

    buttons = [
        [
            InlineKeyboardButton(
                text=constans.PROGRAM_FUND[fund_callbacks.LOOK_WORLD_PROGRAM][
                    0
                ],
                callback_data=fund_callbacks.LOOK_WORLD_PROGRAM,
            ),
            InlineKeyboardButton(
                text=constans.PROGRAM_FUND[
                    fund_callbacks.REABILITATION_PROGRAM
                ][0],
                callback_data=fund_callbacks.REABILITATION_PROGRAM,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constans.PROGRAM_FUND[fund_callbacks.PSIHO_PROGRAM][0],
                callback_data=fund_callbacks.PSIHO_PROGRAM,
            ),
            InlineKeyboardButton(
                text=constans.PROGRAM_FUND[
                    fund_callbacks.KIND_LESSONS_PROGRAM
                ][0],
                callback_data=fund_callbacks.KIND_LESSONS_PROGRAM,
            ),
        ],
        [
            InlineKeyboardButton(
                text="Главное меню", callback_data=fund_callbacks.MAIN_MENU
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.first_start:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.MSG_FIRST_MENU, reply_markup=keyboard
        )

    else:
        await update.message.reply_text(
            text=constans.MSG_FIRST_MENU, reply_markup=keyboard
        )
        flags_obj.changing_first_start(False)

    return fund_states.JOIN_PROGRAM


async def join_or_not_to_program(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """
    Вывод информации о фонде, а также кнопок:
    Вступить, назад, в главное меню.
    """
    query = update.callback_query
    await query.answer()
    message_about_fund_and_documents = ""
    flags_obj = context.user_data[keys.FLAGS]

    if not flags_obj.edit_mode_first_flag:
        data = update.callback_query.data
        if data in constans.PROGRAM_FUND:
            message_about_fund_and_documents = (
                f"{constans.PROGRAM_FUND[data][0]}\n"
                + f"{constans.PROGRAM_FUND[data][1]}\n"
                + f"{constans.PROGRAM_FUND[data][2]}\n"
            )
            context.user_data["Программа фонда"] = constans.PROGRAM_FUND[data][
                0
            ]
        else:
            context.user_data["Программа фонда"] = constans.ANSWERS_DICT[
                "bad_answer"
            ]

        context.user_data["Programm"] = data

    else:
        dates_about_fund = constans.PROGRAM_FUND[context.user_data["Programm"]]
        message_about_fund_and_documents = (
            f"{dates_about_fund[0]}\n"
            + f"{dates_about_fund[1]}\n"
            + f"{dates_about_fund[2]}\n"
        )

        flags_obj.changing_edit_mode_first(False)

    buttons = [
        [
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["join"],
                callback_data=fund_callbacks.JOIN_BUTTON,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["back"], callback_data=str(END)
            ),
        ],
        [
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["main_menu"],
                callback_data=fund_callbacks.MAIN_MENU,
            ),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(
        text=message_about_fund_and_documents + constans.MSG_SECOND_MENU,
        reply_markup=keyboard,
    )

    return fund_states.JOIN_PROGRAM


async def asking_fio_mother(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение фамилии мамы."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(
            text=constans.QUESTIONS_DICT["fio_mother"]
        )
        flags_obj.changing_bad_request(False)
        return fund_states.FIO_MOTHER

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.QUESTIONS_DICT["fio_mother"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.FIO_MOTHER

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=constans.QUESTIONS_DICT["fio_mother"])

    return fund_states.FIO_MOTHER


async def asking_phone_mother(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение телефона мамы."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(
            text=constans.QUESTIONS_DICT["phone_number"]
        )
        flags_obj.changing_bad_request(False)
        return fund_states.PHONE

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.QUESTIONS_DICT["phone_number"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.PHONE

    fio = update.message.text

    if not validators.checking_not_digits(fio):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_fio_mother"],
            reply_markup=constans.MARKUP_FIX,
        )
        flags_obj.changing_bad_request(True)

        return fund_states.RETURN_MOTHER_FIO

    context.user_data["ФИО мамы"] = fio.title()
    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constans.QUESTIONS_DICT["phone_number"]
    )

    return fund_states.PHONE


async def asking_email_mother(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение email мамы."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(text=constans.QUESTIONS_DICT["email"])
        flags_obj.changing_bad_request(False)
        return fund_states.EMAIL

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=constans.QUESTIONS_DICT["email"])
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.EMAIL

    phone_number = update.message.text

    if not validators.checking_phone_number(phone_number):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_phone_number"],
            reply_markup=constans.MARKUP_FIX,
        )
        flags_obj.changing_bad_request(True)
        return fund_states.FIO_MOTHER

    context.user_data["Телефон"] = phone_number
    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constans.QUESTIONS_DICT["email"])

    return fund_states.EMAIL


async def asking_fio_child(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение ФИО ребёнка."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(
            text=constans.QUESTIONS_DICT["fio_child"]
        )
        flags_obj.changing_bad_request(False)

        return fund_states.FIO_CHILD

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.QUESTIONS_DICT["fio_child"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.FIO_CHILD

    email_mother = update.message.text
    if not validators.checking_email(email_mother):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_email"],
            reply_markup=constans.MARKUP_FIX,
        )
        flags_obj.changing_bad_request(True)

        return fund_states.PHONE

    context.user_data["Email"] = email_mother

    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constans.QUESTIONS_DICT["fio_child"])

    return fund_states.FIO_CHILD


async def asking_how_many_people_in_family(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение количества членов семьи."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(
            text=constans.QUESTIONS_DICT["how_many_people"]
        )
        flags_obj.changing_bad_request(False)
        return fund_states.HOW_MANY_PEOPLE

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.QUESTIONS_DICT["how_many_people"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.HOW_MANY_PEOPLE

    fio_child = update.message.text

    if not validators.checking_not_digits(fio_child):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_child_fio"],
            reply_markup=constans.MARKUP_FIX
        )
        flags_obj.changing_bad_request(True)
        return fund_states.EMAIL

    context.user_data["ФИО ребёнка"] = fio_child.title()

    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constans.QUESTIONS_DICT["how_many_people"]
    )

    return fund_states.HOW_MANY_PEOPLE


async def asking_city(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение города проживания."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(text=constans.QUESTIONS_DICT["city"])
        flags_obj.changing_bad_request(False)
        return fund_states.CITY

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=constans.QUESTIONS_DICT["city"])
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.CITY

    how_many_people = update.message.text

    if not validators.checking_count_people_in_family(how_many_people):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_people_in_family"],
            reply_markup=constans.MARKUP_FIX,
        )
        flags_obj.changing_bad_request(True)
        return fund_states.FIO_CHILD

    context.user_data["Сколько членов семьи"] = how_many_people
    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constans.QUESTIONS_DICT["city"])

    return fund_states.CITY


async def asking_address(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение адреса проживания."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(
            text=constans.QUESTIONS_DICT["address"]
        )
        flags_obj.changing_bad_request(False)
        return fund_states.ADDRESS

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.QUESTIONS_DICT["address"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.ADDRESS

    city = update.message.text

    if not validators.checking_not_digits(city):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_city"],
            reply_markup=constans.MARKUP_FIX,
        )
        flags_obj.changing_bad_request(True)
        return fund_states.HOW_MANY_PEOPLE

    context.user_data["Город"] = city.title()
    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constans.QUESTIONS_DICT["address"]
    )

    return fund_states.ADDRESS


async def asking_child_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение дня рождения ребенка."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(
            text=constans.QUESTIONS_DICT["birthday"]
        )
        flags_obj.changing_bad_request(False)
        return fund_states.BIRTHDAY

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.QUESTIONS_DICT["birthday"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.BIRTHDAY

    address = update.message.text

    context.user_data["Адрес"] = address.title()
    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constans.QUESTIONS_DICT["birthday"]
    )

    return fund_states.BIRTHDAY


async def asking_place_birthday(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение места рождения ребенка."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.QUESTIONS_DICT["place_birth"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.PLACE_BIRTH

    child_birthday = update.message.text

    if not validators.checking_birthday(child_birthday):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_birthday"],
            reply_markup=constans.MARKUP_FIX,
        )
        flags_obj.changing_bad_request(True)
        return fund_states.ADDRESS

    context.user_data["Дата рождения ребёнка"] = child_birthday

    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constans.QUESTIONS_DICT["place_birth"]
    )

    return fund_states.PLACE_BIRTH


async def asking_birth_date(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение срока рождения ребёнка."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(
            text=constans.QUESTIONS_DICT["birth_date"]
        )
        flags_obj.changing_bad_request(False)
        return fund_states.BIRTH_DATE

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.QUESTIONS_DICT["birth_date"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.BIRTH_DATE

    place_birth = update.message.text

    context.user_data["Место рождения ребёнка"] = place_birth.title()

    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constans.QUESTIONS_DICT["birth_date"]
    )

    return fund_states.BIRTH_DATE


async def asking_child_weight(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение веса ребёнка."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(text=constans.QUESTIONS_DICT["weight"])
        flags_obj.changing_bad_request(False)
        return fund_states.WEIGHT

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=constans.QUESTIONS_DICT["weight"])
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.WEIGHT

    birth_date = update.message.text

    if not validators.checking_count_people_in_family(birth_date):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_birth_date"],
            reply_markup=constans.MARKUP_FIX,
        )
        flags_obj.changing_bad_request(True)
        return fund_states.PLACE_BIRTH

    context.user_data["Срок рождения ребёнка"] = birth_date

    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constans.QUESTIONS_DICT["weight"])

    return fund_states.WEIGHT


async def asking_child_height(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение роста ребёнка."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(text=constans.QUESTIONS_DICT["height"])
        flags_obj.changing_bad_request(False)
        return fund_states.HEIGHT

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=constans.QUESTIONS_DICT["height"])
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.HEIGHT

    child_weight = update.message.text

    if not validators.checking_weight_and_height(child_weight):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_weight"],
            reply_markup=constans.MARKUP_FIX,
        )
        flags_obj.changing_bad_request(True)
        return fund_states.BIRTH_DATE

    context.user_data["Вес"] = child_weight

    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constans.QUESTIONS_DICT["height"])

    return fund_states.HEIGHT


async def asking_child_diagnosis(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение диагнозов ребёнка."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.bad_request:
        await update.message.reply_text(
            text=constans.QUESTIONS_DICT["diagnosis"]
        )
        flags_obj.changing_bad_request(False)
        return fund_states.DIAGNOSIS

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.QUESTIONS_DICT["diagnosis"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.DIAGNOSIS

    child_height = update.message.text

    if not validators.checking_weight_and_height(child_height):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_height"],
            reply_markup=constans.MARKUP_FIX,
        )
        flags_obj.changing_bad_request(True)
        return fund_states.WEIGHT

    context.user_data["Рост"] = child_height

    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constans.QUESTIONS_DICT["diagnosis"])

    return fund_states.DIAGNOSIS


async def asking_how_found_us(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение информации о том, как нашли фонд."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            constans.QUESTIONS_DICT["how_found_fund"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.HOW_FOUND

    diagnosis = update.message.text
    if not validators.checking_not_digits(diagnosis):
        await update.message.reply_text(
            text=constans.ANSWERS_DICT["bad_diagnosis"],
            reply_markup=constans.MARKUP_FIX,
        )
        flags_obj.changing_bad_request(True)
        return fund_states.HEIGHT

    context.user_data["Диагнозы"] = diagnosis.title()

    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constans.QUESTIONS_DICT["how_found_fund"]
    )

    return fund_states.HOW_FOUND


async def asking_which_fund_now(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """
    Получение информации о том, состоят ли ещё в
    каком-либо фонде в данный момент.
    """
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.QUESTIONS_DICT["fund_now"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.WHICH_FUND

    how_found_us = update.message.text

    context.user_data["Как узнали о нас"] = how_found_us.title()

    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(text=constans.QUESTIONS_DICT["fund_now"])

    return fund_states.WHICH_FUND


async def asking_which_funds_helped(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Получение информации о том, какие фонды помогали раньше."""
    flags_obj = context.user_data[keys.FLAGS]

    if flags_obj.edit_mode_first_flag:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            text=constans.QUESTIONS_DICT["which_fund"]
        )
        flags_obj.changing_edit_mode_first(False)
        flags_obj.changing_edit_mode_second(True)
        return fund_states.WHICH_FUND_WAS_PREVIOUSLY

    which_fund_now = update.message.text

    context.user_data["В фонде сейчас"] = which_fund_now.title()

    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    await update.message.reply_text(
        text=constans.QUESTIONS_DICT["which_fund"]
    )

    return fund_states.WHICH_FUND_WAS_PREVIOUSLY


async def show_user_information(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение пользователю полученной информации."""
    flags_obj = context.user_data[keys.FLAGS]

    which_funds_helped = update.message.text

    context.user_data["Фонды помогали"] = which_funds_helped.title()

    if flags_obj.edit_mode_second_flag:
        flags_obj.changing_edit_mode_second(False)
        return await show_user_edit_information(update, context)

    for key, data in context.user_data.items():
        if key not in constans.SECRET_KEY:
            await update.message.reply_text(text=f"{key}: {data}")

    return await send_or_change_data(update, context)


async def show_user_edit_information(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Отображение пользователю обновленной
    информации после редактирования."""

    for key, data in context.user_data.items():
        if key not in constans.SECRET_KEY:
            await update.message.reply_text(text=f"{key}: {data}")

    return await send_or_change_data(update, context)


async def send_or_change_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Меню с выбором дальнейших действий:
    - Отправить данные куратору
    - Изменить данные
    - Назад
    """

    buttons = [
        [
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["confirm_and_send"],
                callback_data=fund_callbacks.CONFIRM_AND_SEND,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["change_data"],
                callback_data=fund_callbacks.CHANGE_DATA,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["back"],
                callback_data=fund_callbacks.END_SECOND_LEVEL,
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        text=constans.MSG_THIRD_MENU, reply_markup=keyboard
    )

    return fund_states.EDIT_USER_DATА


async def send_message_to_curator(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Отправка сообщения куратору с данными.
    Пока без фотографии/сканов."""
    query = update.callback_query
    await query.answer()
    date_now = date.today()
    date_of_application = f"{date_now.day}.{date_now.month}.{date_now.year}"
    context.user_data["Дата обращения"] = date_of_application

    try:
        html_from_user = HTML_TEMPLATE_JOIN_FUND.substitute(
            mother_fio=context.user_data["ФИО мамы"],
            programm=context.user_data["Программа фонда"],
            mother_phone=context.user_data["Телефон"],
            mother_email=context.user_data["Email"],
            child_fio=context.user_data["ФИО ребёнка"],
            how_many_people=context.user_data["Сколько членов семьи"],
            city=context.user_data["Город"],
            adress=context.user_data["Адрес"],
            child_birthday=context.user_data["Дата рождения ребёнка"],
            place_birth=context.user_data["Место рождения ребёнка"],
            birth_date=context.user_data["Срок рождения ребёнка"],
            weight=context.user_data["Вес"],
            height=context.user_data["Рост"],
            dizgnozes=context.user_data["Диагнозы"],
            date_aplication=context.user_data["Дата обращения"],
            how_about_us=context.user_data["Как узнали о нас"],
            fund_now=context.user_data["В фонде сейчас"],
            fund_early=context.user_data["Фонды помогали"],
        )

        bot_send_email_to_curator(constans.SUBJECT, html_from_user)
    except Exception as ex:
        logger.error(ex)
        html_from_user = HTML_TEMPLATE_JOIN_FUND.substitute(error=ex)
        bot_send_email_to_curator(constans.SUBJECT_ERROR, html_from_user)
        logger.info("Ошибка отправлена куратору!")

    documents = "Вам сообщит куратор."

    if context.user_data["Programm"] in constans.PROGRAM_FUND:
        documents = constans.PROGRAM_FUND[context.user_data["Programm"]][2]

    button = [
        [
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["back_to_menu"],
                callback_data=str(END),
            ),
        ],
    ]

    keyboard = InlineKeyboardMarkup(button)

    await query.edit_message_text(
        text=constans.MESSAGE_SUCCESSFUL_DEPARTURE_TO_CURATOR + documents,
        reply_markup=keyboard,
    )

    return fund_states.END_FIRST_LEVEL


async def change_data(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Изменение данных пользователя через кнопки."""
    flags_obj = context.user_data[keys.FLAGS]

    query = update.callback_query

    await query.answer()

    buttons = [
        [
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["fio_mother"],
                callback_data=fund_callbacks.FIO_MOTHER,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["phone_number"],
                callback_data=fund_callbacks.PHONE,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["email"],
                callback_data=fund_callbacks.EMAIL,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["fio_child"],
                callback_data=fund_callbacks.FIO_CHILD,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["how_many_people"],
                callback_data=fund_callbacks.HOW_MANY_PEOPLE,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["city"],
                callback_data=fund_callbacks.CITY,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["address"],
                callback_data=fund_callbacks.ADDRESS,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["birthday"],
                callback_data=fund_callbacks.BIRTHDAY,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["place_birth"],
                callback_data=fund_callbacks.PLACE_BIRTH,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["birth_date"],
                callback_data=fund_callbacks.BIRTH_DATE,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["weight"],
                callback_data=fund_callbacks.WEIGHT,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["height"],
                callback_data=fund_callbacks.HEIGHT,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["diagnosis"],
                callback_data=fund_callbacks.DIAGNOSIS,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["how_found_fund"],
                callback_data=fund_callbacks.HOW_FOUND,
            ),
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["which_fund"],
                callback_data=fund_callbacks.WHICH_FUND,
            ),
        ],
        [
            InlineKeyboardButton(
                text=constans.BUTTONS_TEXT["fund_now"],
                callback_data=fund_callbacks.WHICH_FUND_WAS_PREVIOUSLY,
            ),
        ],
    ]

    flags_obj.changing_edit_mode_first(True)
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text(text=constans.MSG_EDIT, reply_markup=keyboard)

    return fund_states.EDIT_USER_DATА


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возврат в меню выбора программ."""
    await update.callback_query.answer()
    clean_dictionary(context=context.user_data)
    await application_to_the_fund(update, context)


async def end_second_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возврат в меню вступления в программу."""
    flags_obj = context.user_data[keys.FLAGS]

    query = update.callback_query

    await query.answer()
    # Очистка словаря пользователя с сохранением выбранной программы
    save_values = ["Programm", "Программа фонда"]
    clean_dictionary(context=context.user_data, save_values=save_values)

    # Нужно для корректировки вывода в join_or_not_to_programm
    flags_obj.changing_edit_mode_first(True)

    await join_or_not_to_program(update, context)
    return fund_states.END_FIRST_LEVEL


async def return_main_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Возврат в главное меню."""
    flags_obj = context.user_data[keys.FLAGS]

    query = update.callback_query

    await query.answer()
    # Очистка словаря пользователя
    clean_dictionary(context=context.user_data)

    context.user_data[keys.START_OVER] = True
    flags_obj.changing_first_start(True)

    await start(update, context)
    return fund_states.END_MAIN_MENU


async def stop_nested(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Завершение работы по команде /stop из вложенного разговора."""
    clean_dictionary(context=context.user_data)

    await update.message.reply_text(
        text=constans.MSG_GOODBYE
    )
    return states.STOPPING
