title: Lack of Privacy with Matrix
date: 2025-12-24 03:11
status: published
tags: Matrix, P2P, IM
category: research
lang: en
private: False


Matrix’s E2EE does not, however, encrypt everything. The following information is not encrypted:

Message senders
====

* Message senders are never encrypted
* Due to Matrix’s design, encrypting session/device IDs would break verification
* It’s impossible to prevent timestamps from leaking, since the server can simply note when an event is received anyway
* Join/leave/invite and other room events are never encrypted
* While contents are not leaked, an attacker can know when messages are edited
* Reactions are never encrypted
* Read receipts are never encrypted
* Nicknames are never encrypted
* Profile pictures are never encrypted

Passive information gathering
====

There’s a lot of passive information gathering a malicious admin can do just by querying the Synapse database and this can happen retroactively. Some of the (meta)data include:

* Chat history of any unencrypted room (duh!)
* Information about the users of their homeserver (duh!), like devices, IPs, etc.
* Reactions to end-to-end-encrypted (e2ee) messages, because reactions aren’t encrypted.
* Room related metadata (even for e2ee rooms), room participants and their avatars/nicks, the room topic, power levels, number of messages people sent and when, etc.
* URL previews of shared links (if enabled on a per room setting)


Telegram's Claims
====
There are significant issues and risks using Matrix:

* Append-only Design: Events cannot be deleted, leading to potentially endless history accumulation, which can compromise user deniability.
* Redaction Limitations: Redaction events are advisory; poorly behaving servers may ignore them, retaining the original content.
* Data Leakage: Servers that ignore redactions can inadvertently share supposedly deleted data with new servers joining the room.
* Irreversible Events: Certain events, like membership changes, cannot be deleted as they become part of the room’s auth chain.
* Spam Vulnerability: Bots can be used to spam rooms, complicating the graph and consuming server resources, necessitating room recreation to eliminate spam.
* History Linearization Challenges: Linearizing history is difficult, leading to different servers potentially seeing messages in varying orders.
* Message Forging: It is possible to insert messages into history by crafting plausible events, which may go unnoticed by users.
* Optional Encryption: End-to-end encryption is not mandatory, risking exposure of unencrypted messages in federated rooms.
* Fragile Encryption: Encryption relies on reliable device list updates; failures can lead to broken encryption.
* Device Information Leakage: Device list updates may inadvertently reveal user device information.
* API Interoperability Issues: The lack of a strict definition for canonical JSON can lead to signature mismatches between different server implementations.
* Signature Check Failures: Different programming languages used for homeservers can cause JSON interoperability issues, leading to failed signature checks.
* Arbitrary Signing Key Expiry: Signing keys can expire arbitrarily, causing new servers to reject events from the original server, leading to split-brained rooms.
* Common Split-Brained Rooms: The consensus algorithm for resolving conflicting states is not foolproof, leading to frequent state resets.
* State Reset Chaos: State resets can occur more often with servers written in different languages, causing significant disruptions.
* Loss of Admin Powers: State resets can strip room admins of their powers, making it difficult to manage rooms effectively.
* Room Shutdown Limitations: A room cannot be universally shut down across the federation, which can lead to abuse.
* Moderation Challenges: Effective moderation is hindered by the event auth system’s reliance on accurate state resolution.
* Unauthenticated Media Uploads: Users can upload media without authentication, potentially leading to misuse of the media repository.
* Media Replication Risks: Homeservers can replicate media from other servers, which could lead to denial-of-service issues.
* Unverified Media Uploads: Media uploads are unverified by default, posing risks if harmful content is uploaded.
* Liability for Illegal Media: Homeservers could unknowingly host illegal media due to eager replication from undesirable rooms.

Vulneralbility
====
Following vulnerabilities and attacks to Matrix:

* Simple confidentiality break
* Attack against out-of-band verification
* Semi-trusted impersonation
* Trusted impersonation
* Impersonation to confidentiality break
* IND-CCA break


Data Collection by Matrix.Org and Vector.im
====
Summary of the Notes on privacy and data collection of Matrix.org

matrix.org and vector.im receive a lot of private, personal and identifiable data on a regular basis, or metadata that can be used to precisely identify and/or track users/server, their social graph, usage pattern and potential location. This is possible both by the default configuration values in synapse/Riot that do not promote privacy, and by specific choices made by their developers to not disclose, inform users or resolve in a timely manner several known behaviors of the software.

Data sent on a potential regular basis based on a common web/desktop+smartphone usage even with a self-hosted client and Homeserver:

* The Matrix ID of users, usually including their username.
* Email addresses, phone numbers of the user and their contacts.
* Associations of Email, phone numbers with Matrix IDs.
* Usage patterns of the user.
* IP address of the user, which can give more or less precise geographical location information.
* The user’s devices and system information.
* The other servers that users talks to.
* Room IDs, potentially identifying the Direct chat ones and the other user/server.

With default settings, they allow unrestricted, non-obfuscated public access to the following potentially personal data/info:

* Matrix IDs mapped to Email addresses/phone numbers added to a user’s settings.
* Every file, image, video, audio that is uploaded to the Homeserver.
* Profile name and avatar of users.


References
====
* [Matrix? No thanks.](https://hackea.org/notas/matrix.html)
* [Practically-exploitable Cryptographic Vulnerabilities in Matrix](https://nebuchadnezzar-megolm.github.io/)
* [why not Matrix?](https://telegra.ph/why-not-matrix-08-07)
* [What a malicious Matrix homeserver can do?](https://blog.erethon.com/blog/2022/07/13/what-a-malicious-matrix-homeserver-admin-can-do/)
* [Matrix (metadata leaks)](https://web.archive.org/web/20210202175947/https://serpentsec.1337.cx/matrix)

