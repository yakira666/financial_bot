from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from loguru import logger
import traceback
from aiogram.types import Message

category_fund = [str(i) + "fundamentals" for i in (
    'revenues|other_revenues_summary_subtotal|total_revenue|cost_revenue|gross_profit|selling_general_admin_expenses_total|rd_expenses|other_operating_exp_total|operating_income|interest_expense_total|interest_and_investment_income|net_interest_exp_standard|currency_exchange_gains_loss|other_non_operating_income|ebt_incl_unusual_items|income_tax_expense|earnings_from_cont_ops|net_income_to_company|net_income|ni_to_common_incl_extra_items|ni_to_common_excl_extra_items|revenue_per_share|eps|basic_eps_excl_extra_items|weighted_average_basic_shares_outstanding|diluted_eps|diluted_eps_excl_extra_itmes|weighted_average_diluted_shares_outstanding|normalized_basic_eps|normalized_diluted_eps|div_rate|payout_ratio|ebitda|ebita|ebit_op_in|ebitdar|effective_tax_rate|normalized_net_income|interest_on_long_term_debt|r_d_exp|foreign_sales').split(
    '|')]


async def create_keyboards_fundamentals(message: Message):
    keyboard = InlineKeyboardBuilder()
    try:
        for name_c in category_fund:
            keyboard.add(InlineKeyboardButton(text=name_c[:-12:].strip(), callback_data=name_c))
        keyboard.adjust(4)
        await message.answer("\n\nкатегории:\n\n",
                             reply_markup=keyboard.as_markup(resize_keyboard=True),
                             parse_mode="HTML")
    except:
        logger.info(
            f"Что-то пошло не так с созданием клавиатуры: {traceback.format_exc()}")

    return keyboard


async def create_keyboards_for_symbol_for_fundamentals(message, res, string):
    keyboard = InlineKeyboardBuilder()
    try:

        for name_attr in res.json()['symbols']:
            keyboard.add(
                InlineKeyboardButton(
                    text=f"{name_attr['name'].replace('</b>', '').replace('<b>', '')}-{name_attr['content'].replace('</b>', '').replace('<b>', '')}",
                    callback_data=(name_attr['name'].replace('</b>', '').replace('<b>', '')) + {string}))
            values_list_news.append(name_attr['name'].replace('</b>', '').replace('<b>', '') + {string})
        keyboard.adjust(2)
        keyboard.row(
            InlineKeyboardButton(text='Назад (выбрать другой тикер)', callback_data=('back_to_symbol' + 'news')))
        await message.answer("Вот что нам удалось найти по вашему запросу:\n",
                             reply_markup=keyboard.as_markup(resize_keyboard=True))

    except KeyError:
        logger.info(
            f"Что-то пошло не так с созданием клавиатуры. Код ошибки: {res.status_code}\n{traceback.format_exc()}")
    return keyboard
