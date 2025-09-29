import aiohttp

API_URL = "http://0.0.0.0:8000/digitalMaturity"

async def fetch_digital_maturity(data: dict) -> dict:

    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, json=data) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return {"result": f"Ошибка при запросе API: {resp.status}"}


# Использование в конце опроса
async def send_result_to_user(message, answers: dict):
    try:
        response = await fetch_digital_maturity(answers)
        result_text = response.get("result", "Не удалось получить результат.")

        # Отправляем пользователю в Markdown
        await message.answer(result_text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")