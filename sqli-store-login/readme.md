Открыли [Secret Store](https://sqli-store-login.{host}) — хранилище личных заметок. Входишь под своим
именем и паролем, видишь свои заметки. 
Наш `admin` сохранил там флаг.

---
Интересное место в исходниках сервиса — как собирается запрос входа на `/login`:
https://github.com/rebenkoy/les-simple-ctf/blob/master/sqli-store-login/app.py#L48

---
Полезные ссылки:

- [оператор WHERE](https://www.sqlitetutorial.net/sqlite-where/)
- [комментарии в SQL](https://sqlite.org/lang_comment.html)
- [выражения и операторы (AND / OR)](https://sqlite.org/lang_expr.html)

Хороший план — гуглить "SQLite + интересующее вас действие".
