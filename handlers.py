from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
import db

user_lang = {}

lang_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇿 O'zbek"), KeyboardButton(text="🇬🇧 English")]
    ],
    resize_keyboard=True
)


def main_kb(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Mahsulot bo'limi" if lang == "uz" else "📦 Device menu")],
            [KeyboardButton(text="📞 Bog'lanish" if lang == "uz" else "📞 Contact")]
        ],
        resize_keyboard=True
    )


def menu_kb(lang):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Kiyimlar" if lang == "uz" else "Clothes")],
            [KeyboardButton(text="Elektronika" if lang == "uz" else "Electronics")],
            [KeyboardButton(text="Oziq ovqat" if lang == "uz" else "Food")],
            [KeyboardButton(text="⬅️ Orqaga" if lang == "uz" else "⬅️ Back")]
        ],
        resize_keyboard=True
    )


def make_kb(items, back_text):
    keyboard = [[KeyboardButton(text=i)] for i in items]

    if not items:
        keyboard.append([KeyboardButton(text="❌ Bo'sh" if back_text == "⬅️ Orqaga" else "❌ Empty")])

    keyboard.append([KeyboardButton(text=back_text)])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


async def start(message: Message):
    await message.answer("Tilni tanlang / Choose language", reply_markup=lang_kb)


async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    if text == "🇺🇿 O'zbek":
        user_lang[user_id] = "uz"
        await message.answer("Asosiy menyu:", reply_markup=main_kb("uz"))
        return

    if text == "🇬🇧 English":
        user_lang[user_id] = "en"
        await message.answer("Main menu:", reply_markup=main_kb("en"))
        return

    lang = user_lang.get(user_id)

    if not lang:
        await message.answer("Tilni tanlang / Choose language", reply_markup=lang_kb)
        return

    categories = {
        "Kiyimlar": "clothes",
        "Elektronika": "electronics",
        "Oziq ovqat": "food",
        "Clothes": "clothes",
        "Electronics": "electronics",
        "Food": "food",
    }

    if text in ["Mahsulot bo'limi", "📦 Device menu"]:
        await message.answer(
            "Menyuni tanlang:" if lang == "uz" else "Choose category:",
            reply_markup=menu_kb(lang)
        )
        return

    if text in ["📞 Bog'lanish", "📞 Contact"]:
        await message.answer("📱 +998 33 339 3363")
        return

    if text in ["⬅️ Orqaga", "⬅️ Back"]:
        await message.answer(
            "Asosiy menyu:" if lang == "uz" else "Main menu:",
            reply_markup=main_kb(lang)
        )
        return

    if text in categories:
        devices = db.get_devices_by_category(categories[text])

        await message.answer(
            text + ":",
            reply_markup=make_kb(
                devices,
                "⬅️ Orqaga" if lang == "uz" else "⬅️ Back"
            )
        )
        return

  
    all_devices = (
        db.get_devices_by_category("clothes") +
        db.get_devices_by_category("electronics") +
        db.get_devices_by_category("food")
    )

    if text in all_devices:
        await message.answer(
            f"✅ Buyurtma qabul qilindi: {text}" if lang == "uz"
            else f"✅ Order confirmed: {text}"
        )