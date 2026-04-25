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
    if lang == "uz":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Mahsulot bo'limi")],
                [KeyboardButton(text="📞 Bog'lanish")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📦 Device menu")],
                [KeyboardButton(text="📞 Contact")]
            ],
            resize_keyboard=True
        )


def menu_kb(lang):
    if lang == "uz":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Kiyimlar")],
                [KeyboardButton(text="Elektronika")],
                [KeyboardButton(text="Oziq ovqat")],
                [KeyboardButton(text="⬅️ Orqaga")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Clothes")],
                [KeyboardButton(text="Electronics")],
                [KeyboardButton(text="Food")],
                [KeyboardButton(text="⬅️ Back")]
            ],
            resize_keyboard=True
        )


def make_kb(items, back_text):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=i)] for i in items] + [[KeyboardButton(text=back_text)]],
        resize_keyboard=True
    )


async def start(message: Message):
    await message.answer("Tilni tanlang / Choose language", reply_markup=lang_kb)


async def handle_message(message: Message):
    user_id = message.from_user.id
    text = message.text

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

    if lang == "uz":

        if text == "Mahsulot bo'limi":
            await message.answer("Menyuni tanlang:", reply_markup=menu_kb("uz"))

        elif text == "📞 Bog'lanish":
            await message.answer("📱 Aloqa: +998 33 339 3363")

        elif text == "Kiyimlar":
            devices = db.get_devices_by_category("cloths")
            await message.answer("Kiyimlar:", reply_markup=make_kb(devices, "⬅️ Orqaga"))

        elif text == "Elektronika":
            devices = db.get_devices_by_category("electronics")
            await message.answer("Elektronika:", reply_markup=make_kb(devices, "⬅️ Orqaga"))

        elif text == "Oziq ovqat":
            devices = db.get_devices_by_category("food")
            await message.answer("Oziq ovqat:", reply_markup=make_kb(devices, "⬅️ Orqaga"))

        elif text == "⬅️ Orqaga":
            await message.answer("Asosiy menyu:", reply_markup=main_kb("uz"))

        else:
            all_devices = (
                db.get_devices_by_category("cloths") +
                db.get_devices_by_category("electronics") +
                db.get_devices_by_category("food")
            )

            if text in all_devices:
                await message.answer(f"✅ Buyurtma qabul qilindi: {text}")

    else:

        if text == "📦 Device menu":
            await message.answer("Choose category:", reply_markup=menu_kb("en"))

        elif text == "📞 Contact":
            await message.answer("📱 Phone: +998 33 339 3363")

        elif text == "Clothes":
            devices = db.get_devices_by_category("cloths")
            await message.answer("Clothes:", reply_markup=make_kb(devices, "⬅️ Back"))

        elif text == "Electronics":
            devices = db.get_devices_by_category("electronics")
            await message.answer("Electronics:", reply_markup=make_kb(devices, "⬅️ Back"))

        elif text == "Food":
            devices = db.get_devices_by_category("food")
            await message.answer("Food:", reply_markup=make_kb(devices, "⬅️ Back"))

        elif text == "⬅️ Back":
            await message.answer("Main menu:", reply_markup=main_kb("en"))

        else:
            all_devices = (
                db.get_devices_by_category("cloths") +
                db.get_devices_by_category("electronics") +
                db.get_devices_by_category("food")
            )

            if text in all_devices:
                await message.answer(f"✅ Order confirmed: {text}")