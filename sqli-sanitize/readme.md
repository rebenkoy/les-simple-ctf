The final version [added a firewall](https://sqli-sanitize.{host}): send a quote, a `UNION`, a `;` or a
comment and the request is rejected outright. The note viewer underneath is still injectable in its
numeric ID slot, and there's a hidden note to reach — you just have to do it **without typing any
of the forbidden characters**. SQL is more flexible about how you spell things than the filter
assumes.
