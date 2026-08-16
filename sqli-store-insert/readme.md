Тот же [Secret Store](https://sqli-store-insert.{host}), но вход мы наконец починили — теперь он на
параметрах, и трюк из v1 не сработает. Войди под демо-доступом (`alice` / `letmein`) — увидишь только
свои заметки.

---
Код сервиса тот же, что в v1, но `/login` теперь идёт по безопасной ветке. Сравни её со старой,
уязвимой — и подумай, нет ли где-то ещё точно такой же дыры (например, когда заметка сохраняется).

- [безопасная ветка логина](https://github.com/rebenkoy/les-simple-ctf/blob/master/sqli-store-insert/app.py#L45)
- [как было раньше](https://github.com/rebenkoy/les-simple-ctf/blob/master/sqli-store-insert/app.py#L48)

---
Полезные ссылки:

- [вставка INSERT](https://www.sqlitetutorial.net/sqlite-insert/)
- [подзапросы](https://www.sqlitetutorial.net/sqlite-subquery/)

Хороший план — гуглить "SQLite + интересующее вас действие".
