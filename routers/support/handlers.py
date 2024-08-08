from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config.data import RuTexts
from config.data import SUPPORT_CHAT
from .states import SupportState


router = Router(name=__name__)


@router.message(F.text == RuTexts.support)
async def support_message_handler(message: Message, state: FSMContext):
    await state.set_state(SupportState.question)
    await message.answer(RuTexts.SUPPORT_MESSAGE)


@router.message(SupportState.question, F.text == "ОПЕРАТОР")
async def operator_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("Отправляем ваш(-и) вопрос(-ы) оператору...\nВ течение нескольких минут с вами свяжется поддержка в личных сообщениях")
    username = message.from_user.username
    text = f"<b>Вопрос от {username}</b> [https://t.me/{username}]\n{data['question']}"
    await message.bot.send_message(SUPPORT_CHAT['id'], text=text)  # СДЕЛАТЬ КНОПКУ HIDE КАК У ЛЕГИОН БОТА
    await state.clear()


@router.message(SupportState.question)
async def question_message_handler(message: Message, state: FSMContext):
    question = message.text
    try:
        old_question = (await state.get_data())['question'] + '\n'
    except: # first question
        old_question = ''
    await state.update_data(question=f"{old_question}\n`{question}`")
    keywords = RuTexts.support_keywords
    answer_found = False
    for key in keywords.keys():
        if key in question:
            await message.answer(text=keywords[key])
            answer_found = True
            break
    if not answer_found:
        await message.answer("К сожалению, мы ничего не нашли😕\nЕсли есть еще вопросы, напишите их, и затем пропишите \"ОПЕРАТОР\" для связи с оператором.")
