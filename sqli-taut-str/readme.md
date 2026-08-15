Same bug, different spot. The [staff directory](https://sqli-taut-str.{host}) looks a colleague up by
**username** — and this time your input lands *inside a quoted string*. The `admin` account is
filtered out of normal results, and its (plaintext) password is the prize.

Break out of the quote.
