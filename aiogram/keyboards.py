from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main_menu = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text='Создать задачу'),
			KeyboardButton(text='Создать тег'),
		],
		[
			KeyboardButton(text='Список задач'),
			KeyboardButton(text='Список тегов'),
		],
		[
			KeyboardButton(text='Старт'),
		],
	],
	resize_keyboard=True,
)


yes_or_no = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text='Да'),
			KeyboardButton(text='Нет'),
		],
		[
			KeyboardButton(text='Старт'),
		],
	],
	resize_keyboard=True,
)


task_options = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text='Удалить', callback_data='delete_task')
		]
	]
)


tag_options = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text='Удалить', callback_data='delete_tag')
		]
	]
)


select_tag = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text='Выбрать', callback_data='select_tag')
		]
	]
)
