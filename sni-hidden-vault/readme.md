So the Secret Store switched to **HTTPS**. The login is encrypted now — you can't read the
traffic anymore. Here's a capture to prove it: [**hidden-vault.pcap**](/static/files/hidden-vault.pcap).

Go ahead, try to read it. It's all TLS — the contents are sealed.

But encryption hides *what* you send, not *where* you send it. Every HTTPS connection still
announces its destination host in the clear, before the crypto starts. Skim the capture:
most of these hosts are perfectly ordinary. **One of them shouldn't exist.**

Find that host and pay it a visit.
