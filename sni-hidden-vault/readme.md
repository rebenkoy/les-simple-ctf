Итак, Secret Store переехал на **HTTPS**. Логин теперь зашифрован — трафик больше не прочитать. Вот
дамп в доказательство: [**hidden-vault.pcap**](/static/files/hidden-vault.pcap).

Давай, попробуй его прочитать. Там сплошной TLS — содержимое запечатано.

---
Но шифрование прячет, *что* ты отправляешь, а не *куда*. Каждое HTTPS-соединение всё ещё объявляет хост
назначения открытым текстом — ещё до начала шифрования (это SNI в ClientHello). Пробегись по дампу:
большинство хостов совершенно обычные. **Одного из них существовать не должно.** Найди этот хост и
загляни к нему.

---
Полезные ссылки:

- [Server Name Indication (SNI)](https://ru.wikipedia.org/wiki/Server_Name_Indication)
- [фильтр Wireshark `tls.handshake.extensions_server_name`](https://wiki.wireshark.org/DisplayFilters)
- [Wireshark](https://www.wireshark.org/)

Хороший план — гуглить "Wireshark + TLS SNI filter".
