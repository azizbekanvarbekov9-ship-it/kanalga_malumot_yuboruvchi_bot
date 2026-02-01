from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


CHANNEL_ID =-1003130885017


class UserForm(StatesGroup):
    phone = State()
    fullname = State()
    age = State()
    region = State()
    district = State()


async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📞 Telefon raqamingizni kiriting:")
    await state.set_state(UserForm.phone)


async def phone_handler(message: Message, state: FSMContext):
    phone = message.text.strip()


    if phone.startswith("+"):
        phone = phone[1:]


    for ch in phone:
        if ch not in "0123456789":
            await message.answer(
                "❌ Telefon raqam faqat raqamlardan iborat bolishi kerak!\nMasalan: 998901234567 yoki 901234567"
            )
            return


    if len(phone) == 12 and phone.startswith("998"):
        normalized = phone
    elif len(phone) == 9:
        normalized = "998" + phone
    else:
        await message.answer(
            "❌ Telefon raqam notogri formatda!\nMasalan:\n998901234567\n+998901234567\n901234567"
        )
        return


    operator = normalized[3:5]
    allowed_operators = ["90", "91", "93", "94", "95", "97", "99", "88"]
    if operator not in allowed_operators:
        await message.answer("❌ Operator kodi notogri!")
        return


    normalized_for_channel = "+" + normalized
    await state.update_data(phone=normalized_for_channel)
    await message.answer("👤 Ism va familiyangizni kiriting:")
    await state.set_state(UserForm.fullname)



async def fullname_handler(message: Message, state: FSMContext):
    name = message.text.strip()
    if len(name) == 0 or len(name) > 20:
        await message.answer("❌ Ism va familiya 1-20 ta belgi bolishi kerak!")
        return

    await state.update_data(fullname=name)
    await message.answer("🎂 Yoshingizni kiriting:")
    await state.set_state(UserForm.age)



async def age_handler(message: Message, state: FSMContext):
    age_text = message.text.strip()
    for ch in age_text:
        if ch not in "0123456789":
            await message.answer("❌ Yosh faqat raqam bolishi kerak!")
            return

    age = int(age_text)
    if age < 10 or age > 70:
        await message.answer("❌ Yosh 10 dan 70 gacha bolishi kerak!")
        return

    await state.update_data(age=str(age))
    await message.answer("🏙 Viloyatingizni kiriting:")
    await state.set_state(UserForm.region)



async def region_handler(message: Message, state: FSMContext):
    region = message.text.strip()
    if len(region) == 0 or len(region) > 20:
        await message.answer("❌ Viloyat nomi 1-20 ta belgi bolishi kerak!")
        return

    for ch in region:
        if ch in "0123456789":
            await message.answer("❌ Viloyat nomida raqam bolmaydi!")
            return

    await state.update_data(region=region)
    await message.answer("📍 Tumaningizni kiriting:")
    await state.set_state(UserForm.district)


async def district_handler(message: Message, state: FSMContext, bot: Bot):
    district = message.text.strip()
    if len(district) == 0 or len(district) > 20:
        await message.answer("❌ Tuman nomi 1-20 ta harif bolishi kerak!")
        return

    for ch in district:
        if ch in "0123456789":
            await message.answer("❌ Tuman nomida raqam bolmaydi!")
            return

    await state.update_data(district=district)
    data = await state.get_data()

    text = (
        "📥 Yangi foydalanuvchi:\n\n"
        f"📞 Telefon: {data['phone']}\n"
        f"👤 Ism: {data['fullname']}\n"
        f"🎂 Yosh: {data['age']}\n"
        f"🏙 Viloyat: {data['region']}\n"
        f"📍 Tuman: {data['district']}"
    )

    await bot.send_message(CHANNEL_ID, text)
    await message.answer("✅ Malumotlaringiz qabul qilindi. Rahmat!")
    await state.clear()
