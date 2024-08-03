import time

from keyboards.inline.decryption import cmd_start_decryption
import locale
from loguru import logger
from loader import main_router
from keyboards.inline.keyboards_for_valuation import create_keyboards
from aiogram.fsm.context import FSMContext
from states.user_states import UserState
from utils.api_request import request, auto_complete_func
from aiogram.types import Message

from utils.custom_format_func import custom_format


@main_router.message(UserState.valuation)
async def create_valuation(message: Message, state: FSMContext):
    res_req = await auto_complete_func(message)
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    if res := res_req.json()['symbols']:
        for k in res:
            if k['slug'] == message.text.lower():
                logger.info(f"Все вверно введено пользователем c User_id:{message.chat.id}, выдаем оценку по тикеру")
                await message.answer(f"Вот оценка тикера <b>{k['name'].replace('</b>', '').replace('<b>', '')}</b>:")
                res_request = (request("GET", "https://seeking-alpha.p.rapidapi.com/symbols/get-valuation",
                                       querystring={"symbols": f"{message.text}"})).json()['data'][0]['attributes']
                # Отправка сообщения с финансовыми показателями компании пользователю
                await message.answer(
                    # Форматирование и отправка рыночной капитализации
                    f"Market Capitalization: <b>${custom_format(res_request['marketCap'])}</b>\n"
                    # Форматирование и отправка общей стоимости предприятия (включает долги и вычитает наличные средства)
                    f"Total Enterprise Value: <b>${custom_format(res_request['totalEnterprise'])}</b>\n"
                    # Отправка коэффициента цена/прибыль (P/E), показывающего отношение рыночной цены акции к её прибыли
                    f"Price-to-Earnings (P/E) Ratio: <b>{res_request['lastClosePriceEarningsRatio']}</b>\n"
                    # Форматирование и отправка коэффициента цена/денежный поток, показывающего отношение цены акции к денежному потоку
                    f"Price-to-Cash Flow: <b>{custom_format(res_request['priceCf'])}</b>\n"
                    # Форматирование и отправка коэффициента цена/выручка, показывающего отношение рыночной цены акции к выручке
                    f"Price-to-Sales: <b>{custom_format(res_request['priceSales'])}</b>\n"
                    # Форматирование и отправка коэффициента цена/балансовая стоимость, показывающего отношение рыночной цены акции к её балансовой стоимости
                    f"Price-to-Book: <b>{custom_format(res_request['priceBook'])}</b>\n"
                    # Форматирование и отправка коэффициента цена/материальная балансовая стоимость, исключающего нематериальные активы
                    f"Price-to-Tangible Book: <b>{custom_format(res_request['priceTangb'])}</b>\n"
                    # Форматирование и отправка коэффициента стоимости предприятия к EBITDA (прибыль до вычета процентов, налогов и амортизации)
                    f"Enterprise Value-to-EBITDA (EV/EBITDA): <b>{custom_format(res_request['evEbitda'])}</b>\n"
                    # Форматирование и отправка коэффициента стоимости предприятия к выручке (EV/Sales)
                    f"Enterprise Value-to-Sales (EV/Sales): <b>{custom_format(res_request['evSales'])}</b>\n"
                    # Форматирование и отправка коэффициента стоимости предприятия к свободному денежному потоку (EV/FCF)
                    f"Enterprise Value-to-Free Cash Flow (EV/FCF): <b>{custom_format(res_request['evFcf'])}</b>\n"
                    # Форматирование и отправка общего количества акций компании
                    f"Common Shares: <b>{custom_format(res_request['cShare'])}</b> billion\n"
                    # Форматирование и отправка прогнозируемого коэффициента цена/прибыль (Forward P/E Ratio)
                    f"Forward P/E Ratio: <b>{custom_format(res_request['peRatioFwd'])}</b>\n"
                    # Форматирование и отправка коэффициента PEG (отношение P/E к прогнозируемому росту прибыли)
                    f"PEG Ratio: <b>{custom_format(res_request['pegRatio'])}</b>\n"
                    # Форматирование и отправка коэффициента PEG Non-GAAP для первого финансового года (FY1)
                    f"PEG Non-GAAP for FY1: <b>{custom_format(res_request['pegNongaapFy1'])}</b>\n"
                    # Форматирование и отправка прогнозируемого коэффициента цена/прибыль по GAAP для первого финансового года (FY1)
                    f"P/E GAAP for FY1: <b>{custom_format(res_request['peGaapFy1'])}</b>\n"
                    # Форматирование и отправка прогнозируемого коэффициента цена/прибыль Non-GAAP для первого финансового года (FY1)
                    f"P/E Non-GAAP for FY1: <b>{custom_format(res_request['peNongaapFy1'])}</b>\n"
                    # Форматирование и отправка текущего коэффициента цена/прибыль Non-GAAP
                    f"P/E Non-GAAP: <b>{custom_format(res_request['peNongaap'])}</b>\n"
                    # Форматирование и отправка прогнозируемого коэффициента стоимости предприятия к EBITDA для первого финансового года (EV/EBITDA for FY1)
                    f"EV/EBITDA for FY1: <b>{custom_format(res_request['evEbitdaFy1'])}</b>\n"
                    # Форматирование и отправка прогнозируемого коэффициента стоимости предприятия к выручке для первого финансового года (EV/Sales for FY1)
                    f"EV/Sales for FY1: <b>{custom_format(res_request['evSalesFy1'])}</b>\n",
                    parse_mode='HTML'  # Указываем Telegram, что используем HTML теги для форматирования текста
                )
                await state.update_data(decryption_req=res_request)
                time.sleep(0.5)
                await cmd_start_decryption(message)
                return
            else:
                await create_keyboards(message, res_req, 'valuation')
                return


