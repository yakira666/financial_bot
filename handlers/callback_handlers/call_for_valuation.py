import time

from keyboards.reply.symbol_menu import cmd_create_menu
from loader import main_router
from aiogram import types, F
from loguru import logger
from keyboards.inline.keyboards_for_valuation import valuation_list
from aiogram.fsm.context import FSMContext
from utils.api_request import request
from keyboards.inline.decryption import cmd_start_decryption
from utils.custom_format_func import custom_format

res = {}
@main_router.callback_query(lambda callback_value: callback_value.data in valuation_list)
async def top_gainers(callback: types.CallbackQuery, state: FSMContext):
    logger.info("Пришел callback в valuation")
    print(callback.data)
    res_request = (request("GET", "https://seeking-alpha.p.rapidapi.com/symbols/get-valuation",
                           querystring={"symbols": f"{callback.data[:-10:]}"})).json()['data'][0]['attributes']
    # Отправка сообщения с финансовыми показателями компании пользователю
    await callback.message.answer(f'Вот оценка по тикеру <b>{callback.data[:-10:]}</b>:')
    await callback.message.answer(
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
    print("УШЛО: ", res_request)
    await state.update_data(decryption_req=res_request)
    res['1'] = res_request
    time.sleep(0.5)
    await cmd_start_decryption(callback.message)
    # Очистка состояния после отправки сообщения
    await state.clear()


@main_router.callback_query(F.data == "Да, получить!")
async def yes_g(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    res_request = data.get('decryption_req')
    # ДОБАВЛЕНО В СВЯЗИ НЕИЗВЕСТНОЙ ОШИБКИ, не понимаю почему через состояние после клавиатуры не ловиться request, решения не нашел
    if res_request is None:
        res_request = res['1']
    await callback.message.answer(
        # Форматирование и отправка рыночной капитализации (в миллиардах долларов США)
        f"Рыночная капитализация: <b>${custom_format(res_request['marketCap'])} миллиардов</b>\n"
        # Форматирование и отправка общей стоимости предприятия (в миллиардах долларов США)
        f"Общая стоимость предприятия (включает долги и вычитает наличные средства): <b>${custom_format(res_request['totalEnterprise'])} миллиардов</b>\n"
        # Отправка коэффициента цена/прибыль (P/E), показывающего отношение рыночной цены акции к её прибыли
        f"Коэффициент цена/прибыль (P/E) (показывает отношение рыночной цены акции к её прибыли): <b>{res_request['lastClosePriceEarningsRatio']}</b>\n"
        # Форматирование и отправка коэффициента цена/денежный поток, показывающего отношение цены акции к денежному потоку
        f"Коэффициент цена/денежный поток (показывает отношение рыночной цены акции к денежному потоку компании): <b>{custom_format(res_request['priceCf'])}</b>\n"
        # Форматирование и отправка коэффициента цена/выручка, показывающего отношение рыночной цены акции к выручке
        f"Коэффициент цена/выручка (показывает отношение рыночной цены акции к выручке компании): <b>{custom_format(res_request['priceSales'])}</b>\n"
        # Форматирование и отправка коэффициента цена/балансовая стоимость, показывающего отношение рыночной цены акции к её балансовой стоимости
        f"Коэффициент цена/балансовая стоимость (показывает отношение рыночной цены акции к её балансовой стоимости): <b>{custom_format(res_request['priceBook'])}</b>\n"
        # Форматирование и отправка коэффициента цена/материальная балансовая стоимость, исключающего нематериальные активы
        f"Коэффициент цена/материальная балансовая стоимость (показывает отношение рыночной цены акции к материальной балансовой стоимости, исключая нематериальные активы): <b>{custom_format(res_request['priceTangb'])}</b>\n"
        # Форматирование и отправка коэффициента стоимости предприятия к EBITDA (в миллиардах долларов США)
        f"Коэффициент стоимости предприятия к EBITDA (EV/EBITDA) (показывает отношение общей стоимости предприятия к прибыли до вычета процентов, налогов и амортизации): <b>{custom_format(res_request['evEbitda'])}</b>\n"
        # Форматирование и отправка коэффициента стоимости предприятия к выручке (в миллиардах долларов США)
        f"Коэффициент стоимости предприятия к выручке (EV/Sales) (показывает отношение общей стоимости предприятия к выручке): <b>{custom_format(res_request['evSales'])}</b>\n"
        # Форматирование и отправка коэффициента стоимости предприятия к свободному денежному потоку (в миллиардах долларов США)
        f"Коэффициент стоимости предприятия к свободному денежному потоку (EV/FCF) (показывает отношение общей стоимости предприятия к свободному денежному потоку): <b>{custom_format(res_request['evFcf'])}</b>\n"
        # Форматирование и отправка общего количества акций компании (в миллиардах акций)
        f"Общее количество акций: <b>{custom_format(res_request['cShare'])} миллиардов</b>\n"
        # Форматирование и отправка прогнозируемого коэффициента цена/прибыль (Forward P/E Ratio)
        f"Прогнозируемый коэффициент цена/прибыль (Forward P/E Ratio) (показывает отношение рыночной цены акции к её ожидаемой прибыли): <b>{custom_format(res_request['peRatioFwd'])}</b>\n"
        # Форматирование и отправка коэффициента PEG (отношение P/E к прогнозируемому росту прибыли)
        f"Коэффициент PEG (показывает отношение P/E к прогнозируемому росту прибыли): <b>{custom_format(res_request['pegRatio'])}</b>\n"
        # Форматирование и отправка коэффициента PEG Non-GAAP для первого финансового года (FY1)
        f"Коэффициент PEG Non-GAAP для первого финансового года (FY1) (показывает отношение PEG по Non-GAAP для первого финансового года): <b>{custom_format(res_request['pegNongaapFy1'])}</b>\n"
        # Форматирование и отправка прогнозируемого коэффициента цена/прибыль по GAAP для первого финансового года (FY1)
        f"Прогнозируемый коэффициент цена/прибыль по GAAP для первого финансового года (FY1) (показывает отношение рыночной цены акции к её прибыли по GAAP для первого финансового года): <b>{custom_format(res_request['peGaapFy1'])}</b>\n"
        # Форматирование и отправка прогнозируемого коэффициента цена/прибыль Non-GAAP для первого финансового года (FY1)
        f"Прогнозируемый коэффициент цена/прибыль Non-GAAP для первого финансового года (FY1) (показывает отношение рыночной цены акции к её прибыли по Non-GAAP для первого финансового года): <b>{custom_format(res_request['peNongaapFy1'])}</b>\n"
        # Форматирование и отправка текущего коэффициента цена/прибыль Non-GAAP
        f"Текущий коэффициент цена/прибыль Non-GAAP (показывает отношение рыночной цены акции к её прибыли по Non-GAAP): <b>{custom_format(res_request['peNongaap'])}</b>\n"
        # Форматирование и отправка прогнозируемого коэффициента стоимости предприятия к EBITDA для первого финансового года (FY1)
        f"Прогнозируемый коэффициент стоимости предприятия к EBITDA для первого финансового года (FY1) (показывает отношение общей стоимости предприятия к прибыли до вычета процентов, налогов и амортизации для первого финансового года): <b>{custom_format(res_request['evEbitdaFy1'])}</b>\n"
        # Форматирование и отправка прогнозируемого коэффициента стоимости предприятия к выручке для первого финансового года (FY1)
        f"Прогнозируемый коэффициент стоимости предприятия к выручке для первого финансового года (FY1) (показывает отношение общей стоимости предприятия к выручке для первого финансового года): <b>{custom_format(res_request['evSalesFy1'])}</b>\n",
        parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove()
        # Указываем Telegram, что используем HTML теги для форматирования текста
    )
    await state.clear()
    await callback.message.answer("Это все по оценке этой компании... Выбирете пожалуйста другую команду!",
                                  reply_markup=types.ReplyKeyboardRemove())
    await cmd_create_menu(callback.message)


@main_router.callback_query(F.data == "Нет, отказаться!")
async def no(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Это все по оценке этой компании... Выбирете пожалуйста другую команду!",
                                  reply_markup=types.ReplyKeyboardRemove())
    await cmd_create_menu(callback.message)
