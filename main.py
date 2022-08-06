import logging
from aiogram import Bot, Dispatcher, executor, types
import markups as nav
import config as cfg
from pycoingecko import CoinGeckoAPI


logging.basicConfig(level=logging.INFO)

bot = Bot(token=cfg.TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
cg = CoinGeckoAPI()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        photo_url = "https://www.yuglink.ru/mycryptoworld.jpg"
        await bot.send_photo(chat_id=message.from_user.id, photo=photo_url)
        await bot.send_message(message.from_user.id, f'Привет, {message.from_user.full_name}! Я криптобот и я помогу тебе узнать стоимость электронных монеток!\nВыбери ТОП-3 крипту или отправь мне любую другую монету:', reply_markup=nav.crypto_list)
        await bot.send_message(message.from_user.id, 'Реклама: <a href="https://t.me/code_nvrsk">CodeNvrsk</a>',
                               parse_mode='HTML')


@dp.callback_query_handler(text_contains='cc_')
async def crypto(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    callback_data = call.data
    currency = str(callback_data[3:])
    result = cg.get_price(ids=currency, vs_currencies=['usd', 'rub'])
    await bot.send_message(call.from_user.id, f'Крипта {currency} на данный момент стоит: {result[currency]["usd"]} $ или {result[currency]["rub"]} руб.')
    await bot.send_message(call.from_user.id, 'Хочешь узнать стоимость другой криптовалюты ?\nПросто отправь мне название монеты!')


@dp.message_handler()
async def any_crypto(message: types.Message):
    if message.chat.type == 'private':
        result = cg.get_price(ids=message.text.lower(), vs_currencies=['usd', 'rub'])
        try:
            await bot.send_message(message.from_user.id, f'Крипта {message.text.lower()} на данный момент стоит: {result[message.text.lower()]["usd"]} $ или {result[message.text.lower()]["rub"]} руб.')
        except KeyError:
            await bot.send_message(message.from_user.id, 'Извините, что-то я не могу найти такую монету, проверьте ее название, оно должно быть на английском языке.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
