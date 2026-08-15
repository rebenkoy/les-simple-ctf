[VaultKeep](https://csrf.{host}) keeps a private recovery note that **only the admin can publish**.
No injection here — the admin **opens links you report** every couple of minutes, and their browser
does what your page tells it to, using their session.

Craft a page that makes the admin publish the note without meaning to. The result shows up on
`/public`. (The challenge README has the exact host-a-page steps.)
