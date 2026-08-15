An `eval` in a service is rare — but plenty of services forget that **SQL is also a language**.
[SecureNotes](https://sqli-taut-num.{host}) lets you pull up a note by its numeric **ID**, and it builds
that lookup by pasting your input straight into a query.

Some notes are marked unpublished. Convince the database to hand them over anyway. The ID is a
number — you won't even need a quote.
