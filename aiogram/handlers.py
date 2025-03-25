import os
import aiohttp
import keyboards
from aiogram.filters import CommandStart
from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.formatting import Text, Bold


router = Router()


class CreateTask(StatesGroup):

	title = State()
	description = State()
	response_about_tag = State()
	tag = State()


class CreateTag(StatesGroup):

	text = State()


@router.message(CommandStart())
async def start_handler(message):

    await message.answer(f"Привет, {message.from_user.first_name}!", reply_markup=keyboards.main_menu)


@router.message(F.text == 'Старт')
async def cancel_and_start_handler(message, state):

	await message.answer(f"Привет, {message.from_user.first_name}!", reply_markup=keyboards.main_menu)
	await state.clear()


@router.message(F.text == 'Создать задачу')
async def create_task_handler(message, state):

	await state.set_state(CreateTask.title)
	await message.answer('Введите название задачи.')


@router.message(CreateTask.title)
async def create_task_title_handler(message, state):

	await state.update_data(title=message.text)
	await state.set_state(CreateTask.description)
	await message.answer('Введите описание задачи.')


@router.message(CreateTask.description)
async def create_task_description_handler(message, state):

	await state.update_data(description=message.text)
	await state.set_state(CreateTask.response_about_tag)
	await message.answer('Прикрепить к задаче тег?', reply_markup=keyboards.yes_or_no)


@router.message(CreateTask.response_about_tag)
async def response_about_tag_handler(message, state):

	await state.update_data(response_about_tag=message.text)
	await state.set_state(CreateTask.tag)

	data = await state.get_data()
	async with aiohttp.ClientSession(cookies={'telegram_user_id': message.from_user.id}) as session:
		if data.pop('response_about_tag') == 'Да':
			async with session.get(f'http://{os.getenv("BACKEND_HOST")}:8000/api/tags/') as response:
				if response.status == 200:
					tags = await response.json()
					if tags:
						await message.answer('Выберите тег...', reply_markup=keyboards.main_menu)
						for tag in tags:
							await message.answer(
								f'{tag["text"]}',
								reply_markup=keyboards.select_tag
							)
					else:
						await message.answer(
							'Пока нет ни одного тега. Отмена...',
							reply_markup=keyboards.main_menu
						)
				else:
					await message.answer(
						'Не удалось открыть список тегов...',
						reply_markup=keyboards.main_menu
					)
		else:
			async with session.post(f'http://{os.getenv("BACKEND_HOST")}:8000/api/tasks/', json=data) as response:
				if response.status == 201:
					await message.answer(
						'Задача создана!',
						reply_markup=keyboards.main_menu
					)
					text = Text(Bold(data["title"]), f'''\n\n{data["description"]}''')
					await message.answer(
						**text.as_kwargs(),
						reply_markup=keyboards.task_options
					)
				else:
					print(await response.text())
					await message.answer(
						'Не удалось создать задачу...',
						reply_markup=keyboards.main_menu
					)
				await state.clear()


@router.callback_query(F.data == 'select_tag')
async def select_tag_handler(callback, state):

	tag_text = callback.message.text
	data = await state.get_data()

	async with aiohttp.ClientSession(cookies={'telegram_user_id': callback.from_user.id}) as session:
		async with session.get(f'http://{os.getenv("BACKEND_HOST")}:8000/api/tags/{tag_text}/') as response:
			tag_data = await response.json()
			data['tag'] = tag_data['pk']
		async with session.post(f'http://{os.getenv("BACKEND_HOST")}:8000/api/tasks/', json=data) as response:
			if response.status == 201:
				await callback.answer(
					'Задача создана!',
					reply_markup=keyboards.main_menu
				)
				await callback.message.answer(
					'Задача создана!',
					reply_markup=keyboards.main_menu
				)
				text = Text(Bold(data["title"]), f'''\n\n{data["description"]}\n\n#{tag_text}''')
				await callback.message.answer(
					**text.as_kwargs(),
					reply_markup=keyboards.task_options
				)
			else:
				print(await response.text())
				await callback.message.answer(
					'Не удалось создать задачу...',
					reply_markup=keyboards.main_menu
				)
	await state.clear()


@router.message(F.text == 'Список задач')
async def task_list_handler(message):

	async with aiohttp.ClientSession(cookies={'telegram_user_id': message.from_user.id}) as session:
		tags = await get_tag_list(message, session)
		async with session.get(f'http://{os.getenv("BACKEND_HOST")}:8000/api/tasks/') as response:
			if response.status == 200:
				tasks = await response.json()
				if tasks:
					for task in tasks:
						tag_text = None
						try:
							tag_text = next(filter(lambda tag: tag['pk'] == task["tag"], tags))['text']
						except:
							pass
						text = Text(
							Bold(task["title"]),
							f'''\n\n{task["description"]}''',
							f'''\n\n#{tag_text}''' if tag_text else '',
							f'''\n\n{task["created"][:10]}'''
						)
						await message.answer(
							**text.as_kwargs(),
							reply_markup=keyboards.task_options
						)
				else:
					await message.answer(
						'Пока нет ни одной задачи...',
						reply_markup=keyboards.main_menu
					)
			else:
				await message.answer(
					'Не удалось открыть список задач...',
					reply_markup=keyboards.main_menu
				)


@router.callback_query(F.data == 'delete_task')
async def delete_task_handler(callback):

	task_title = callback.message.text.partition('\n')[0]

	async with aiohttp.ClientSession(cookies={'telegram_user_id': callback.from_user.id}) as session:
		async with session.delete(f'http://{os.getenv("BACKEND_HOST")}:8000/api/tasks/{task_title}/') as response:
			if response.status == 204:
				await callback.message.answer('Задача удалена!')
				await callback.answer('Задача удалена!')
			else:
				await callback.message.answer(
					'Не удалось удалить задачу...',
				)


@router.message(F.text == 'Создать тег')
async def create_tag_handler(message, state):

	await state.set_state(CreateTag.text)
	await message.answer('Введите название тега.')


@router.message(CreateTag.text)
async def create_tag_text_handler(message, state):

	await state.update_data(text=message.text)
	data = await state.get_data()

	async with aiohttp.ClientSession(cookies={'telegram_user_id': message.from_user.id}) as session:
		async with session.post(f'http://{os.getenv("BACKEND_HOST")}:8000/api/tags/', json=data) as response:
			if response.status == 201:
				await message.answer(
					f'''Тег "{data['text']}" создан!''',
					reply_markup=keyboards.main_menu
				)
			else:
				await message.answer(
					'Не удалось создать тег...',
					reply_markup=keyboards.main_menu
				)
	await state.clear()


async def get_tag_list(message, session):

	async with session.get(f'http://{os.getenv("BACKEND_HOST")}:8000/api/tags/') as response:
		if response.status == 200:
			return await response.json()
		else:
			await message.answer(
				'Не удалось открыть список тегов...',
				reply_markup=keyboards.main_menu
			)


@router.message(F.text == 'Список тегов')
async def tag_list_handler(message):

	async with aiohttp.ClientSession(cookies={'telegram_user_id': message.from_user.id}) as session:
		tags = await get_tag_list(message, session)
		if tags:
			for tag in tags:
				await message.answer(
					f'{tag["text"]}',
					reply_markup=keyboards.tag_options
				)
		else:
			await message.answer(
				'Пока нет ни одного тега...',
				reply_markup=keyboards.main_menu
			)
			


@router.callback_query(F.data == 'delete_tag')
async def delete_tag_handler(callback):

	async with aiohttp.ClientSession(cookies={'telegram_user_id': callback.from_user.id}) as session:
		async with session.delete(f'http://{os.getenv("BACKEND_HOST")}:8000/api/tags/{callback.message.text}/') as response:
			if response.status == 204:
				await callback.message.answer('Тег удален!')
				await callback.answer('Тег удален!')
			else:
				await message.answer(
					'Не удалось удалить тег...',
				)
