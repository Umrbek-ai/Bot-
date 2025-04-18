import logging
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
import asyncio

# Admin Telegram ID
ADMIN_ID = 1222447074

# Bot token
TOKEN = "7706479452:AAE2VUyTx9bX4-egVtJu9jv0nCvpQhh6CAY"

# Bot va dispatcher
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)

# --- TUGMALAR ---
language_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="O'zbek"), KeyboardButton(text="Русский"), KeyboardButton(text="English")]
    ],
    resize_keyboard=True
)

main_menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Bepul xizmatlar ro'yxati")],
        [KeyboardButton(text="Shikoyat yuborish")]
    ],
    resize_keyboard=True
)

# --- START ---
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Tilni tanlang / Choose your language / Выберите язык:",
        reply_markup=language_kb
    )

# --- TIL TANLASH ---
@router.message(F.text.in_(["O'zbek", "Русский", "English"]))
async def language_selected(message: Message):
    await message.answer(
        f"<b>{message.text} tili tanlandi.</b>\nIltimos, kerakli bo'limni tanlang:",
        reply_markup=main_menu_kb
    )

# --- XIZMATLAR ---
@router.message(F.text == "Bepul xizmatlar ro'yxati")
async def show_services(message: Message):
    await message.answer(
        "<b>Bepul xizmatlar:</b>\n"
        "- Qon tahlili\n"
        "- UZI\n"
        "- Terapevt ko'rigi\n"
        "- Rentgen\n"
        "- EKG (Yurak tekshiruvi)\n"
        "- Pediatr maslahatlari"
    )

# --- SHIKOYAT YUBORISH ---
@router.message(F.text == "Shikoyat yuborish")
async def get_complaint(message: Message):
    await message.answer("Iltimos, shikoyatingizni yozing. Biz uni maxfiy saqlaymiz.")

async def forward_to_admin(message: Message, media_type: str):
    user_info = (
        f"<b>Yangi {media_type} yuborildi!</b>\n"
        f"<b>Foydalanuvchi:</b> {message.from_user.full_name} (@{message.from_user.username})\n"
        f"<b>ID:</b> {message.from_user.id}\n\n"
    )
    
    if media_type == "matn":
        content = f"<b>Matn:</b>\n{message.text}"
        await bot.send_message(ADMIN_ID, user_info + content)
    elif media_type == "rasm":
        await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=user_info)
    elif media_type == "video":
        await bot.send_video(ADMIN_ID, message.video.file_id, caption=user_info)
    elif media_type == "ovoz":
        await bot.send_voice(ADMIN_ID, message.voice.file_id, caption=user_info)

# --- MATN QABULI ---
@router.message(F.text)
async def receive_text(message: Message):
    if message.text not in ["O'zbek", "Русский", "English", "Bepul xizmatlar ro'yxati", "Shikoyat yuborish"]:
        await forward_to_admin(message, "matn")
        await message.answer("<i>Xabaringiz qabul qilindi. Rahmat!</i>", reply_markup=main_menu_kb)

# --- RASM QABULI ---
@router.message(F.photo)
async def receive_photo(message: Message):
    await forward_to_admin(message, "rasm")
    await message.answer("<i>Rasm qabul qilindi. Rahmat!</i>", reply_markup=main_menu_kb)

# --- VIDEO QABULI ---
@router.message(F.video)
async def receive_video(message: Message):
    await forward_to_admin(message, "video")
    await message.answer("<i>Video qabul qilindi. Rahmat!</i>", reply_markup=main_menu_kb)

# --- OVOZLI XABAR QABULI ---
@router.message(F.voice)
async def receive_voice(message: Message):
    await forward_to_admin(message, "ovoz")
    await message.answer("<i>Ovozli xabar qabul qilindi. Rahmat!</i>", reply_markup=main_menu_kb)

# --- BOTNI ISHGA TUSHURISH ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))
