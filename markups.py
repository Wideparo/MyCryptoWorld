from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

btnBtc = InlineKeyboardButton(text='Bitcoin', callback_data='cc_bitcoin')
btnEth = InlineKeyboardButton(text='Etherium', callback_data='cc_ethereum')
btnXrp = InlineKeyboardButton(text='Ripple', callback_data='cc_ripple')

crypto_list = InlineKeyboardMarkup(row_width=1)
crypto_list.insert(btnBtc)
crypto_list.insert(btnEth)
crypto_list.insert(btnXrp)