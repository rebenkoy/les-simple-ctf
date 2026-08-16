[Secrets Storage](https://store.{host}) хранит твои личные заметки за небольшим JSON-API `/api/account`
— он отдаёт их только по действующей сессии. А чтобы дружить с *партнёрскими приложениями*, API
возвращает твой `Origin` обратно и разрешает передавать креды.

---
Ревьюеры проверяют присланные макеты в **Design Grader** ([https://grader.{host}](https://grader.{host})),
будучи в это время залогинены здесь. Пришли страницу, которая кросс-доменно прочитает их
`/api/account` и отправит `secret_note` тебе — свой личный адрес возьми во вкладке **Listener**. Хостить
ничего не надо: грейдер сам покажет ревьюеру твою страницу.

---
Полезные ссылки:

- [что такое CORS](https://developer.mozilla.org/ru/docs/Web/HTTP/CORS)
- [fetch с `credentials: include`](https://developer.mozilla.org/ru/docs/Web/API/Fetch_API/Using_Fetch)
- [заголовок Access-Control-Allow-Credentials](https://developer.mozilla.org/ru/docs/Web/HTTP/Headers/Access-Control-Allow-Credentials)

Хороший план — гуглить "CORS misconfiguration + credentials".
