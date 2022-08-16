import os
from sqlite3 import IntegrityError

import aiogram
from aiogram import Bot
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor

import button
import config
import db

storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print('Bot activated')
    db.start_db()


class quest(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()
    q8 = State()
    q9 = State()
    q10 = State()
    q11 = State()
    q12 = State()
    q13 = State()


class MassSend(StatesGroup):
    sendd = State()


@dp.message_handler(commands='start')
async def strt(message: types.Message):
    try:
        db.db_add(message.from_user.id, message.from_user.first_name, message.from_user.username)
    except IntegrityError:
        pass
    await bot.send_message(message.from_user.id, text="Ласкаво просимо!\n"
                                                      "Цей бот допоможе вам зрозуміти наскільки ви обізнані "
                                                      "у темі годування груддю, пройдіть опитування та дізнаєтеся "
                                                      "свій рівень знань у цій темі\n", reply_markup=button.interview())


@dp.message_handler(commands='send', state=None)
async def snd(message: types.Message):


    if message.from_user.id not in config.ADMIN_ID:
        await bot.send_message(message.from_user.id, text="В ДОСТУПІ ВІДМОВЛЕНО!")
    else:
        await bot.send_message(message.from_user.id, text=f"Напишите и отправьте сообщение для "
                                                          f"рассылки оно будет отправлено {len(db.all_user())} пользователям")
        await MassSend.sendd.set()



@dp.message_handler(content_types=aiogram.types.ContentType.ANY,
                    state=MassSend.sendd)
async def send(message: types.Message, state: FSMContext):
    good, bad = 0, 0
    await state.finish()
    errors_list = []
    for i in db.all_user():
        try:
            await bot.send_message(i[0], message.text)
            good += 1
        except Exception as e:
            bad += 1
            errors_list.append(e)
    await bot.send_message(message.from_user.id, 'Рассылка завершена успешно\n'
                                                 f'Доставлено: {good}\n'
                                                 f'Не доставлено: {bad}\n'
                                                 f'Ошибки {set(errors_list)}')


# ******************************************************************************************************************
# 1 ВОПРОС

@dp.callback_query_handler(text='start_again', state=None)
@dp.message_handler(text_startswith='Почати опитування', state=None)
async def question_1(message: types.Message):
    #    await db.start_num_db()
    #    await db.add_pnt(message.from_user.id)
    await quest.q1.set()
    await bot.send_message(message.from_user.id, 'Дайте відповідь на 13 питань та дізнайтеся наскільки ви '
                                                 'обізнані у грудному вигодовуванні 🤔',
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, text="1 запитання з 13\n\n"
                                                      "Грудне вигодовування можливе лише в тому випадку, "
                                                      "якщо жінка народила природнім шляхом?",
                           reply_markup=button.yes_no())


@dp.callback_query_handler(text='yes_yes', state=quest.q1)
async def question_1(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Це неправда!\n'
                                                   f'ГВ можна налаштувати не лише після кесаревого розтину, '
                                                   f'але й у тому випадку, коли жінка не народжувала дитину, а, '
                                                   f'наприклад, стала його прийомною чи второю мамою. '
                                                   f'Явище має назву індукована лактація.\n'
                                                   f'ЇЇ можна налаштувати, якщо дотримуватись певної схеми дій.',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q1)
async def question_1(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Абсолютно вірно!\n'
                                                   f'Індукована лактація можлива у самих різних випадках та '
                                                   f'дозволяє жінці вигодувати свою дитину, навіть не народжуючи його.\n'
                                                   f'Кажуть, Кім Кардашьян годувала груддю свою третю дитину, '
                                                   f'якого їй народила сурогатна мати.',
                           reply_markup=button.next())
    await call.answer()


# 1 ВОПРОС
# ******************************************************************************************************************
# 2 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q1)
async def question_2(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f"2 запитання з 13\n\n"
                                                   f"Грудне молоко залежно від обставин може змінювати колір?",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q2)
async def question_2(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Це правда!\n'
                                                   f'Молоко може бути не лише білим, '
                                                   f'але й мати блакитний, зелений, рожевий, помаранчевий, '
                                                   f'жовтий (вважайте: золотий!) відтінок.\n'
                                                   f'Це залежить від безлічі факторів: наприклад, від того, '
                                                   f'яка сьогодні погода, як відчуває себе дитина, що з’їла її мама.',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q2)
async def question_2(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Дуже навіть може!\n'
                                                   f'Воно буває найрізноманітніших відтінків, '
                                                   f'які обумовлюються різними обставинами у житті матері '
                                                   f'та дитини: від температури повітря до раціону жінки.',
                           reply_markup=button.next())


# 2 ВОПРОС
# ******************************************************************************************************************
# 3 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q2)
async def question_3(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text="3 запитання з 13\n\n"
                                                   "Грудне молоко захищає малюків від інфекцій?",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q3)
async def question_3(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Захищає!\nІ за допомогою антитіл, '
                                                   f'і за допомогою лейкоцитів, і навіть за допомогою цукрів, '
                                                   f'які допомагають росту корисних бактерій у кишківнику малюка, '
                                                   f'а також перешкоджають заселенню слизових патогенними мікробами. '
                                                   f'Дива та й годі! '
                                                   f'Так, годувати під час хвороби (і дитини, і мами) можна!',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q3)
async def question_3(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Ще й як захищає!\n'
                                                   f'У молоці містяться клітини, '
                                                   f'які допомагають вести боротьбу з усілякими неприємними мікробами, '
                                                   f'що атакують малюка з перших хвилин його життя.',
                           reply_markup=button.next())


# 3 ВОПРОС
# ******************************************************************************************************************
# 4 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q3)
async def question_4(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text="4 запитання з 13\n\n"
                                                   "Молоко не змінює свого смаку та складу протягом усього "
                                                   "періоду годування, саме тому після шести місяців лактації "
                                                   "воно стає порожнім",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q4)
async def question_4(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Це твердження невірне.\nМолоко – дизайнерський продукт, '
                                                   f'склад якого залежить від потреб та віку малюка.\nНаприклад, '
                                                   f'молоко, яке жіночій організм продукує для недоношеної дитини, '
                                                   f'є більш насиченим та поживним, '
                                                   f'оскільки дитині необхідна особлива підтримка.\n'
                                                   f'Крім того, у кожної жінки молоко індивідуальне за своїм складом.',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q4)
async def question_4(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Ви праві, молоко змінюється протягом усього часу лактації.\n'
                                                   f'На його смак впливають продукти, які споживає лактуюча жінка '
                                                   f'(є версія, що чим різноманітніше вона харчується, '
                                                   f'тим меншою є вірогідність того, '
                                                   f'що в неї виросте маленький привереда).\n'
                                                   f'А на склад – і вік дитини, і особливості її фізичного стану, '
                                                   f'і потреба в певних речовинах.',
                           reply_markup=button.next())


# 4 ВОПРОС
# ******************************************************************************************************************
# 5 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q4)
async def question_5(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text="5 запитання з 13\n\n"
                                                   "Мама, що годує, має фізичні супер-сили через гормони, "
                                                   "тому може встигнути абсолютно все: малюк, пиріг, секс, кар’єра.",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q5)
async def question_5(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Це не так.\nНа щастя, є сучасні нутриціологічні продукти, '
                                                   f'які не тільки підтримують лактацію, а й мають ще багато ефектів, '
                                                   f'які допомагають саме мамі:\n'
                                                   f'- додають сили та витривалості\n'
                                                   f'- заспокоюють,покращують сон\n'
                                                   f'- щоб можна було виспатися навіть з '
                                                   f'частими перервами на годування\n'
                                                   f'- пришвидшують схуднення після пологів\n'
                                                   f'- зміцнюють імунітет\n'
                                                   f'- сприяють відновленню шкіри та волосся\n',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q5)
async def question_5(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Правильно!\nМама – це жива людина, а не реактор.\n'
                                                   f'На щастя, є сучасні нутриціологічні продукти, які не тільки '
                                                   f'підтримують лактацію, а й мають ще багато ефектів, '
                                                   f'які допомагають саме мамі:\n'
                                                   f'- додають сили та витривалості\n'
                                                   f'- заспокоюють\n'
                                                   f'- покращують сон, щоб можна було виспатися навіть з '
                                                   f'частими перервами на годування\n'
                                                   f'- пришвидшують схуднення після пологів\n'
                                                   f'- зміцнюють імунітет\n'
                                                   f'- сприяють відновленню шкіри та волосся\n',
                           reply_markup=button.next())


# 5 ВОПРОС
# ******************************************************************************************************************
# 6 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q5)
async def question_6(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text="6 запитання з 13\n\n"
                                                   "Грудничків треба допоювати водою?",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q6)
async def question_6(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Не варто!\nМолоко майже повністю складається з води, '
                                                   f'яка на усі сто задовольняє потреби малюка в рідині.\n'
                                                   f'Навіть у спекотний день, оскільки, як ми встановили раніше, '
                                                   f'молоко підлаштовується під зовнішні обставини: '
                                                   f'в особливо спекотні дні воно стає більш водянистим.',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q6)
async def question_6(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Правильно, робити цього не варто.\n'
                                                   f'Це не лише марно, але й навіть може бути шкідливим: '
                                                   f'вода створює несправжнє відчуття ситості, '
                                                   f'а також навантажує незрілі нирки малюка. '
                                                   f'Від надмірної кількості рідини може наступити навіть так звана '
                                                   f'«водна інтоксикація».',
                           reply_markup=button.next())


# 6 ВОПРОС
# ******************************************************************************************************************
# 7 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q6)
async def question_7(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text="7 запитання з 13\n\n"
                                                   "Після кожного годування необхідно зціджуватись",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q7)
async def question_7(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Ні, не треба.\nЗціджувати молоко варто в тому випадку, '
                                                   f'якщо ви відчуваєте нагрівання та дискомфорт, '
                                                   f'в усіх інших випадках цього робити не слід '
                                                   f'(надмірні зусилля з видалення молока, що залишилось у грудях, '
                                                   f'може призвести до лактостазів).',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q7)
async def question_7(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Правильно.\nЗціджуватись після кожного годування '
                                                   f'не потрібно – це зайва процедура, '
                                                   f'що може призвести до порушення природнього ходу лактації.',
                           reply_markup=button.next())


# 7 ВОПРОС
# ******************************************************************************************************************
# 8 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q7)
async def question_8(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text="8 запитання з 13\n\n"
                                                   "Грудне вигодовування корисне не лише для дитини, "
                                                   "але й для матері",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q8)
async def question_8(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Правильно!\nГрудне вигодовування вважається гарною профілактикою '
                                                   f'раку грудей та яєчників, знижує ризик серцево-судинних '
                                                   f'захворювань, цукрового діабету 2-го типу, '
                                                   f'артриту та навіть перелому шийки стегна у зрілому віці!',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q8)
async def question_8(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Не все лише дитині!\n'
                                                   f'ГВ корисне для материнського здоров’я – про це свідчать '
                                                   f'результати багатьох досліджень по всьому світу.\n'
                                                   f'Лактація захищає жінок від багатьох захворювань, '
                                                   f'у тому числі від раку органів репродуктивної системи.',
                           reply_markup=button.next())


# 8 ВОПРОС
# ******************************************************************************************************************
# 9 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q8)
async def question_9(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text="9 запитання з 13\n\n"
                                                   "На ГВ можна схуднути?",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q9)
async def question_9(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Це правда!\nНа те, аби виробити молоко, '
                                                   f'організм витрачає приблизно стільки ж калорій, '
                                                   f'скільки потрібно на підтримку роботи мозку протягом дня.\n'
                                                   f'Існує версія, що день лактації за енерговитратами дорівнює '
                                                   f'дев’ятикілометровій прогулянці. Хоча, далеко не усі жінки худнуть '
                                                   f'на ГВ – це не універсальний рецепт. Саме тому в формулюванні '
                                                   f'обрано слово «можна» – тому що можна схуднути, а можна і ні.',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q9)
async def question_9(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Насправді можна.\nЗовсім необов’язково, '
                                                   f'що ГВ змусить вас набрати вагу.\n'
                                                   f'Твердження, що «годування груддю – обов’язковий набір ваги» '
                                                   f'невірне. Витрата енергії під час годування дуже висока.',
                           reply_markup=button.next())


# 9 ВОПРОС
# ******************************************************************************************************************
# 10 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q9)
async def question_10(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text="10 запитання з 13\n\n"
                                                   "Абсолютно всі добавки та чаї для покращення "
                                                   "лактації корисні та безпечні.",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q10)
async def question_10(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Це не так.\nЗастарілі засоби для покращення лактації можуть '
                                                   f'містити в собі кмин (фенхель), який проникає у грудне молоко '
                                                   f'та викликає нервове перезбудження у дитини (а значить і у мами, '
                                                   f'і у тата, і у сусідів…). Також є продукти для покращення '
                                                   f'лактації з вмістом продуктів бджолярства, наприклад, '
                                                   f'з маточним молочком. Це штука корисна, але дуже алергенна. '
                                                   f'Маленькому організму алергенів і так вистачить. Хай краще звикає, '
                                                   f'що мама їсть шоколад.',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q10)
async def question_10(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Правильно!\nПродукти з кмином (фенхель) заборонені для немовля '
                                                   f'та для годуючої мами, тому що викликають нервове збудження '
                                                   f'у дитини.\nТакож продукти з бджолиним маточним молочком занадто '
                                                   f'алергенні, не варто ризикувати, є ж і інші продукти для '
                                                   f'покращення лактації.',
                           reply_markup=button.next())


# 10 ВОПРОС
# ******************************************************************************************************************
# 11 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q10)
async def question_11(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text="11 запитання з 13\n\n"
                                                   "Мама, що годує, обов’язково повинна дотримуватися суворої дієти?",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q11)
async def question_11(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Це не так.\nСувора дієта у спробі уникнути ризику розвитку '
                                                   f'алергії у малюка може призвести… до ризику розвитку алергії '
                                                   f'у малюка!\nЧим різноманітнішим є харчування мами, що годує, '
                                                   f'тим краще вона себе почуває, тим більше у неї сил, тим більше '
                                                   f'смаків дізнається її дитина (так, молоко може транслювати смаки '
                                                   f'їжі, що її з’їла мати, її дитині).',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q11)
async def question_11(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Правильно!\nЖодних дієт без причини не потрібно, '
                                                   f'що б там не казали суворі тітоньки у пологових будинка на '
                                                   f'пострадянському просторі. Тому що поняття «дієта матері, '
                                                   f'що годує» – оксюморон, який існує тільки на тому самому просторі.',
                           reply_markup=button.next())


# 11 ВОПРОС
# ******************************************************************************************************************
# 12 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q11)
async def question_12(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text="12 запитання з 13\n\n"
                                                   "Відлучення від грудей може спровокувати депресивний стан у "
                                                   "жінки?",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q12)
async def question_12(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Це правда.\nІснує таке поняття – депресія відлучення. '
                                                   f'Це стан пригнічення та туги, який може відчувати навіть та мати, '
                                                   f'яка чекала на день завершення лактації як манни небесної. '
                                                   f'Це пояснюється тим, що в жіночому організмі відбуваються великі '
                                                   f'гормональні зміни (так, знову). Сумувати після завершення '
                                                   f'ГВ – нормально.',
                           reply_markup=button.next())


@dp.callback_query_handler(text='nope', state=quest.q12)
async def question_12(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'На справді ні.\nТобто так. У жінки може розвиватись стан '
                                                   f'пригніченості, який має назву депресія відлучення. Все гормони!',
                           reply_markup=button.next())


# 12 ВОПРОС
# ******************************************************************************************************************
# 13 ВОПРОС


@dp.callback_query_handler(text='nxt', state=quest.q12)
async def question_13(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text="13 запитання з 13\n\n"
                                                   "Добавки для підтримання лактації потрібні лише тим, "
                                                   "у кого пропало молоко. ",
                           reply_markup=button.yes_no())
    await quest.next()


@dp.callback_query_handler(text='yes_yes', state=quest.q13)
async def question_13(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['points'] = data.get('points', 0) + 1
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Це не так.\nСучасні дієтичні добавки розроблені для підтримки '
                                                   f'грудного вигодовування. Існують спеціалізовані дієтичні добавки, '
                                                   f'що запобігають втраті молока та насичують його корисними '
                                                   f'речовинами, наприклад цинком.',
                           reply_markup=button.end())


@dp.callback_query_handler(text='nope', state=quest.q13)
async def question_13(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message(call.from_user.id, text=f'Правильно!\nВи можете обрати найсучаснішу добавку до раціону мами, '
                                                   f'що годує. Ця добавка допоможе не тільки підтримувати лактацію та '
                                                   f'насичувати молоко корисними речовинами, а й покращити '
                                                   f'витривалість мами та прискорити зменшення ваги після пологів.',
                           reply_markup=button.end())


# 13 ВОПРОС
# ******************************************************************************************************************
# КОНЕЦ. ИТОГИ


@dp.callback_query_handler(text='endd', state=quest.q13)
async def back_end(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    async with state.proxy() as data:
        counter = data.get('points')
    db.update_point(call.from_user.id, counter)
    if counter == 0 or counter <= 4:
        await bot.send_photo(call.from_user.id,
                             photo=open(os.path.join(config.path_photo, 'image_2022-08-16_14-26-03.png'), 'rb'),
                             caption=f"{config.minimum}\n"
                                     f"Ваши баллы: {counter}\n",
                             reply_markup=button.axxe(counter, config.minimum))
    elif counter >= 5 and counter <= 9:
        await bot.send_photo(call.from_user.id,
                             photo=open(os.path.join(config.path_photo, 'image_2022-08-16_14-26-31.png'), 'rb'),
                             caption=f"{config.medium}\n"
                                     f"Ваши баллы: {counter}\n",
                             reply_markup=button.axxe(counter, config.medium))
    else:
        await bot.send_photo(call.from_user.id,
                             photo=open(os.path.join(config.path_photo, 'image_2022-08-16_14-26-39.png'), 'rb'),
                             caption=f"{config.maximum}\n"
                                     f"Ваши баллы: {counter}\n",
                             reply_markup=button.axxe(counter, config.maximum))
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
