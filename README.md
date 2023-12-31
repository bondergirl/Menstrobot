# Menstrobot

Этот проект создан, чтобы упростить мою жизнь и пополнить портфолио.

Во время создания этого простого и нехитрого бота я научилась работать с SQL, Telebot, Git, своими классами и многое поняла об архитектуре проекта.
Опыт встраивания инлайн-клавиатуры в свой проект на основе телеграмм-календаря от grcanosa: https://github.com/grcanosa позволил мне научиться понимать и модифицировать чужой код:
от предложенного автором варианта осталось немногое. Я русифицировала названия месяцев и дней с помощью манипуляций со стандартным модулем calendar, что было весьма интересно.


Чтобы запустить исходный код проекта, необходимо вставить в строковую переменную TOKEN файла config.py токен своего бота, полученный в Телеграмм от @BotFather.
Воспользоваться готовым ботом: @Menstrobot в поиске Телеграмм.  

**Структура проекта:**  
- main.py: обработка команд пользователя, перенаправление в основную логику  
- actions.py: основная логика  
- db.py: работа с базой данных
- telegramcalendar.py: генерация календаря в удобном виде, по мотивам https://github.com/grcanosa  
- config.py: токен бота  


**Доступные команды:**  
**/start** - отметить начало цикла. При первом запуске бота происходит регистрация. Также выводится информация о количестве дней, прошедших с отметки предыдущего цикла.  
**/change** - изменить начало цикла. Выводится список дат, отмеченных пользователем, в виде инлайн-кнопок. Выбранная дата по нажатию удаляется, затем пользователь может выбрать новую дату начала цикла.  
**/cycle** - посмотреть текущий день цикла. Выводится информация о количестве дней, прошедших с отметки предыдущего цикла.  
**/statistics** - посмотреть статистику циклов. Выводится список дат, отмеченных пользователем, в виде информационных инлайн-кнопок.  
**/help** - список действий. Выводится информация о доступных командах.  
**/hi** - приветствие пользователя.  


**По мере развития проекта будут добавлены функции:**
- Напоминание пользователю отметить начало цикла при приближении дней, прошедших с последней отметки, к средней длительности цикла пользователя
- Обработка не связанных с темой бота сообщений пользователя
- Автоматическое определение языка для дней недели и месяцев в календаре
- Логирование ошибок 
