from telegram.ext import ConversationHandler


"""Константы ConversationHandler"""
(
    SELECTING_ACTION,
    CHATS,
    REQUEST,
    ADD_VOLUNTEER,
    TALK,
    DONATION,
    EVENTS,
    ASK_QUESTION,
    ABOUT,
    ENDING,
) = map(chr, range(10))

(
    VOLUNTEER,
    ADDING_VOLUNTEER,
    ADDING_NAME,
    ADDING_BIRTHDAY,
    ADDING_CITY,
    ADDING_PHONE,
    ADDING_EMAIL,
    ADDING_MESSAGE,
    SHOWING_VOLUNTEER,
    EDIT_VOLUNTEER,
    VOLUNTEER_FEATURE,
    TYPING_VOLUNTEER,
    SEND_VOLUNTEER,
    VOLUNTEER_SENT,
    SENT,
) = map(chr, range(10, 25))

(STOPPING,) = map(chr, range(30, 31))

(
    START_OVER,
    CURRENT_FEATURE,
    LEVEL,
    FEATURES,
    NAME,
    BIRTHDAY,
    CITY,
    PHONE,
    EMAIL,
    MESSAGE,
    THEME,
) = map(chr, range(100, 111))

END = ConversationHandler.END

(
    ASKING_QUESTION,
    QUESTION,
    ADDING_THEME,
    ADDING_QUESTION,
    EDIT_QUESTION,
    SEND_QUESTION,
    SHOWING_QUESTION,
    QUESTION_FEATURE,
    TYPING_QUESTION,
    QUESTION_SENT,
) = map(chr, range(200, 210))
