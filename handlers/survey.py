from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import json
import os
from misc.keyboards import main_kb, cancel_kb

router = Router()

class SurveyStates(StatesGroup):
    answering = State()

questions = [
    "Насколько бизнес-процессы компании формализованы и документированы (регламенты, инструкции)?",
    "Используете ли вы систему для автоматизации основных процессов (например, CRM для продаж, ERP для учета ресурсов, СЭД/ECM для документооборота)?",
    "Есть ли в компании KPI или метрики, которые собираются и анализируются автоматически (BI-системы, дашборды)?",
    "Как часто принимаются управленческие решения на основе данных (data-driven)?",
    "Какие ИТ-системы сейчас используются (1С, CRM, ERP, СЭД, самописные решения, Excel/Google Sheets)?",
    "Есть ли интеграция между системами (например, CRM ↔️ бухгалтерия ↔️ склад)?",
    "Используете ли вы облачные сервисы (SaaS/PaaS/IaaS) или все системы развернуты локально?",
    "Как обеспечивается информационная безопасность (резервное копирование, антивирус, контроль доступа)?",
    "Каков уровень цифровой грамотности сотрудников (умение работать с современными ИТ-системами, готовность к обучению)?",
    "Проводится ли регулярное обучение персонала по работе с новыми цифровыми инструментами?",
    "Есть ли в штате ИТ-специалисты или работа ведется через подрядчиков/аутсорс?",
    "Как сотрудники воспринимают инициативы по автоматизации (сопротивление/нейтрально/поддержка)?",
    "Есть ли у компании стратегия цифровой трансформации или план развития ИТ?",
    "Используете ли вы электронные сервисы взаимодействия с государством (Госуслуги, ЭДО, маркировка, контур «Честный знак»)?",
    "Планируете ли вы внедрение новых решений в ближайшие 1–2 года (CRM, СЭД, электронная торговая площадка и т.д.)?"
]

@router.message(F.text == "Отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=main_kb)

@router.message(F.text == "Анкета")
async def survey_start(message: Message, state: FSMContext):
    await state.set_state(SurveyStates.answering)
    await state.update_data(current_question=0, answers={})
    await message.answer(questions[0], reply_markup=cancel_kb)


@router.message(SurveyStates.answering)
async def get_answers(message: Message, state: FSMContext):
    data = await state.get_data()
    curQuest = data.get("current_question", 0)
    answers = data.get("answers", {})

    answers[f"question_{curQuest + 1}"] = message.text
    await state.update_data(answers=answers)

    # Есть ли следующий вопрос
    nextQuest = curQuest + 1
    if nextQuest < len(questions):
        await state.update_data(current_question=nextQuest)
        await message.answer(questions[nextQuest], reply_markup=cancel_kb)
    else:
        try:
            # Мапчик ответов
            answersMap = {f"question_{i+1}": answers[f"question_{i+1}"] for i in range(len(questions))}
             
            # Перезаписываем файл results.json
            with open("results.json", "w", encoding="utf-8") as jsonFile:
                json.dump(answersMap, jsonFile, ensure_ascii=False)

            await message.answer("Спасибо за участие в опросе! Данные сохранены.", reply_markup=main_kb)
        except Exception as e:
            await message.answer(f"Произошла ошибка при сохранении данных: {str(e)}", reply_markup=main_kb)

        # Очищаем состояние
        await state.clear()