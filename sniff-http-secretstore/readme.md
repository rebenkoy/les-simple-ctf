Кто-то оставил дамп трафика: [**challenge.pcap**](/static/files/challenge.pcap).

Это срез обычного сетевого трафика — браузинг, вызовы API, привычная болтовня. Но где-то там админ
вошёл в **Secret Store** (`http://secretstore.local`) по обычному **HTTP**. А HTTP передаёт всё
открытым текстом.

---
Открой дамп в **Wireshark**, покопайся в шуме и найди, что именно ввёл админ. Дальше сделай очевидное:
флаг — это секрет в *его* хранилище, и прочитать его может только *он*.

*Подсказка: не каждый логин, что ты видишь, — тот самый.*

---
Полезные ссылки:

- [Wireshark](https://www.wireshark.org/)
- [фильтры отображения (напр. `http.request`)](https://wiki.wireshark.org/DisplayFilters)
- [Follow → HTTP Stream](https://www.wireshark.org/docs/wsug_html_chunked/ChAdvFollowStreamSection.html)

Хороший план — гуглить "Wireshark + follow HTTP stream".
