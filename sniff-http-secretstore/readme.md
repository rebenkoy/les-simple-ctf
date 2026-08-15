Someone left a packet capture lying around: [**challenge.pcap**](/static/files/challenge.pcap).

It's a slice of ordinary network traffic — browsing, API calls, the usual chatter. But
somewhere in there, an admin signed in to the **Secret Store** (`http://secretstore.local`)
over plain **HTTP**. HTTP sends everything in the clear.

Open the capture in **Wireshark**, dig through the noise, and find what the admin typed.
Then do the obvious thing with it: the flag is a secret sitting in *their* vault, and only
*they* can read it.

*Tip: not every login you see is the one you want.*
