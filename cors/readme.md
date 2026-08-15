[Secrets Storage](https://store.{host}) keeps your private notes behind a small JSON API at
`/api/account` — revealed only with a valid session. To let *partner apps* integrate, the API echoes
your `Origin` back and allows credentials.

Reviewers grade design submissions on the **Design Grader** ([https://grader.{host}](https://grader.{host}))
while signed in here. Submit a page that reads the reviewer's `/api/account` across origins and beacons
the `secret_note` to you — open the **Listener** tab for your private address. No self-hosting: the
grader serves your page to the reviewer.
