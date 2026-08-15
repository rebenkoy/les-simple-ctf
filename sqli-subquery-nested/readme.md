[This page](https://sqli-subquery-nested.{host}) lists the notes shared to a username — but your input is buried
*inside a subquery*, not the main query. Naively injecting just throws a syntax error. Figure out
what you need to close first, then reach the outer query.
