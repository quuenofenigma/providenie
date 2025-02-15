import logging
from datetime import date

from pydantic.error_wrappers import ValidationError
from telegram import BotCommandScopeChat, Update
from telegram import InlineKeyboardButton as Button
from telegram import InlineKeyboardMarkup as Keyboard
from telegram.ext import ContextTypes
from validate_email.exceptions import Error as EmailValidationError

from bot.constants import button, key, state
from bot.constants.info import text
from bot.constants.info.question import ALL_QUESTIONS
from bot.core.settings import settings
from bot.utils import send_email_message, send_message


async def start_form(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """Init the user's form data and asks for input."""
    user_data = context.user_data
    await context.bot.set_my_commands(
        [button.MENU_CMD, button.CANCEL_CMD, button.START_CMD],
        scope=BotCommandScopeChat(update.effective_chat.id),
    )
    option = user_data.get(key.OPTION, {})
    model = option.get(key.CUSTOM_MODEL)
    if not model:
        model = user_data[key.MENU][key.MODEL]

    user_data[key.FORM] = {
        key.DATA: model(),
        key.FIELDS: list(model().dict()),
        key.FIELD_INDEX: 0,
        key.FIELD_EDIT: False,
    }

    return await ask_input(update, context)


async def ask_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for input related to the current form field."""
    callback = update.callback_query
    user_data = context.user_data
    form = user_data[key.FORM]
    fields = form[key.FIELDS]

    if callback and callback.data.startswith(key.ASK):
        form[key.FIELD_EDIT] = callback.data.replace(f'{key.ASK}_', '').lower()

    field = form.get(key.FIELD_EDIT)
    if not field:
        field = fields[form[key.FIELD_INDEX]]

    question = ALL_QUESTIONS[field.upper()]
    await send_message(update, question[key.TEXT])

    return state.FORM_INPUT


async def save_input(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:
    """Save the user's input for the current form field."""
    user_data = context.user_data
    form = user_data[key.FORM]
    fields = form[key.FIELDS]
    input_text = update.message.text.strip()

    field = form.get(key.FIELD_EDIT)
    if not field:
        field = fields[form[key.FIELD_INDEX]]
    try:
        setattr(form[key.DATA], field, input_text)
    except (ValidationError, EmailValidationError) as error:
        error_message = (
            text.VALIDATION_ERROR.format(
                field=field,
                form=user_data[key.FORM][key.DATA].__class__.__name__,
                error=error.errors()[0]['msg'],
            )
            if type(error) is ValidationError
            else error
        )
        logging.info(error_message)
        question_hint = ALL_QUESTIONS[field.upper()][key.HINT]
        error_message = text.INPUT_ERROR_TEMPLATE.format(hint=question_hint)
        await send_message(update, error_message)
        return await ask_input(update, context)

    if (form[key.FIELD_INDEX] + 1) >= len(fields):
        return await show_data(update, context)

    form[key.FIELD_INDEX] = form[key.FIELD_INDEX] + 1

    return await ask_input(update, context)


async def show_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show the completed form data to the user."""
    user_data = context.user_data
    info = user_data[key.MENU]
    form = user_data[key.FORM]

    message = text.SHOW_DATA_TEMPLATE.format(
        title=text.FORM,
        value=info.get(key.NAME),
    )
    if menu_option := user_data.get(key.OPTION):
        message += text.SHOW_DATA_TEMPLATE.format(
            title=info.get(key.FORM_HEADER),
            value=menu_option[key.BUTTON_TEXT],
        )
    message += text.SHOW_DATA_TEMPLATE.format(
        title=text.APPLICATION_DATE,
        value=date.today().strftime(text.DATE_TEMPLATE),
    )
    for name, value in form[key.DATA]:
        question = ALL_QUESTIONS[name.upper()]
        message += text.SHOW_DATA_TEMPLATE.format(
            title=question[key.TITLE],
            value=value,
        )
    form[key.SHOW_DATA] = message

    keyboard = Keyboard(
        [[button.SEND_DATA], [button.EDIT_MENU, button.MAIN_MENU]],
    )
    await send_message(update, message, keyboard=keyboard)
    logging.info(
        f'User filled out the form for "{user_data[key.MENU][key.NAME]}".',
    )

    return state.FORM_SUBMISSION


async def edit_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the edit menu to the user."""
    user_data = context.user_data
    fields = user_data[key.FORM][key.FIELDS]

    edit_buttons = []
    for field in fields:
        question = ALL_QUESTIONS[field.upper()]
        callback = f'{key.ASK}_{field.upper()}'
        edit_buttons.append(
            [Button(text=question[key.TITLE], callback_data=callback)],
        )
    edit_buttons.append([button.SHOW_DATA])

    await send_message(
        update,
        text.SELECT_EDIT,
        keyboard=Keyboard(edit_buttons),
    )

    return state.FORM_INPUT


async def send_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send form data to the specified curator email-address."""
    user_data = context.user_data
    form = user_data[key.FORM]
    info = user_data[key.MENU]
    message = form[key.SHOW_DATA].replace('\n', '<br>')
    choice = user_data.get(key.OPTION)

    if choice:
        subject = f'Анкета_{choice.get(key.BUTTON_TEXT)}_{info.get(key.NAME)}'
    else:
        subject = f'Анкета_{info.get(key.NAME)}'

    logging.info(
        f'Form for "{user_data[key.MENU][key.NAME]}" is completed and sent.',
    )
    curators = settings.email_curator.split(',')
    if all(
        send_email_message(message, subject, curator) for curator in curators
    ):
        response_message = info.get(key.RESPONSE, text.MAIL_SEND_OK_MESSAGE)
    else:
        response_message = text.MAIL_SEND_ERROR_MESSAGE

    await send_message(
        update,
        response_message,
        keyboard=Keyboard([[button.MAIN_MENU]]),
    )

    return state.MAIN_MENU
