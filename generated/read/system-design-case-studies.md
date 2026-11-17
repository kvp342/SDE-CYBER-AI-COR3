SYSTEM DESIGN · CASE STUDIES

# Five designs worked end to end

URL shortener, chat, news feed, notifications and file sync, each following the approach on the System Design one-pager: requirements → estimates → API → data model → design → trade-offs, with a diagram. Every estimate is computed from the stated assumptions, so you can change an assumption and redo the maths the same way.

**In the interview.** Spend 5 minutes on requirements and estimates, 10 on the API, data and high-level diagram, 15 on one or two deep dives the interviewer picks, and the rest on trade-offs and failure cases. Freshers are mostly judged on clear reasoning, not on knowing every tool. See the [system design](knowledge-base/design.md#high-level-system-design-hld) Knowledge Base page.

|                                             |
|---------------------------------------------|
| [URL shortener](#url-shortener)                    |
| [Chat app (one-to-one and groups)](#chat-app-one-to-one-and-groups) |
| [News feed](#news-feed)                       |
| [Notification service](#notification-service)            |
| [File storage and sync](#file-storage-and-sync)           |

## URL shortener

### Functional requirements

- Create a short link for a long URL, optionally with a custom alias and expiry
- Redirect a short link to the long URL
- Basic click counts

### Non-functional

- Redirects fast (tens of milliseconds) and highly available
- Short codes unguessable enough not to enumerate easily
- Read-heavy: reads far exceed writes

### Estimates

Assumptions: new per month = 100,000,000, read write = 100, bytes per row = 500, years = 5.

|                               |        |
|-------------------------------|--------|
| Write QPS                     | 38.6   |
| Read QPS                      | 3.9 K  |
| Rows in 5 years               | 6.0 G  |
| Storage in 5 years (bytes)    | 3.0 TB |
| 7-char base62 codes available | 3.5 T  |

### API

- POST /urls {long_url, alias?, expires_at?} → {code}
- GET /{code} → 302 Location: long_url
- GET /urls/{code}/stats → {clicks}

### Data model

- urls(code PK, long_url, owner_id, created_at, expires_at)
- Key-value store (DynamoDB or Cassandra) keyed by code; clicks counted asynchronously

### Design

- ID generation: each app server takes a block of counter values from a coordinator and base62-encodes them (no collisions, no per-write coordination); add a random offset if codes must not be sequential.
- Reads: load balancer → app servers → Redis cache (hot codes, LRU) → database on a miss. The read path is stateless and scales horizontally.
- Clicks: the redirect handler publishes an event to a queue; a worker aggregates counts, so redirects never wait on analytics.
- Abuse: rate-limit creation per user or IP; check long URLs against a malware list.

### Trade-offs

|                 |                                                                                                                |
|-----------------|----------------------------------------------------------------------------------------------------------------|
| 301 vs 302      | 301 is cached by browsers (less load, but you lose click counts); 302 keeps every click visible.               |
| Counter vs hash | Counter blocks never collide; hashing the URL needs collision checks but gives the same code for the same URL. |

Building blocks used: load balancer, cache, database, sharding, queue, rate limiting.

## Chat app (one-to-one and groups)

### Functional requirements

- Send and receive messages in real time, one-to-one and in groups
- Message history across devices
- Delivered and read receipts, online status

### Non-functional

- Low latency for online users
- No lost messages; order preserved within a conversation
- Works when the receiver is offline (push notification, then sync)

### Estimates

Assumptions: dau = 50,000,000, msgs per user = 40, bytes per msg = 100, peak = 3.

|                             |          |
|-----------------------------|----------|
| Messages per day            | 2.0 G    |
| Average messages/s          | 23.1 K   |
| Peak messages/s (×3)        | 69.4 K   |
| New storage per day (bytes) | 200.0 GB |

### API

- WebSocket: send {conversation_id, client_msg_id, text} → ack {message_id, seq}
- WebSocket push: message, receipt and presence events
- GET /conversations/{id}/messages?before=seq&limit=50

### Data model

- messages(conversation_id PARTITION, seq CLUSTERING, sender_id, text, sent_at) in a wide-column store
- conversations and members in a relational DB; presence in Redis with expiry

### Design

- Clients keep a WebSocket to a gateway; a session registry (Redis) maps user → gateway so the message service can route to the right connection.
- The message service assigns a per-conversation sequence number, stores the message, then fans out to online members and queues push notifications for offline ones.
- Delivery is at-least-once; clients dedupe with client_msg_id and order by seq.
- Large groups: cap size or fan out through a queue so one message to 1,000 members does not block.

### Trade-offs

|                    |                                                                     |
|--------------------|---------------------------------------------------------------------|
| Fan-out on write   | Simple and fast to read; expensive for very large groups.           |
| Store-then-deliver | Never loses a message; adds a write before delivery (milliseconds). |

Building blocks used: load balancer, websocket, database, sharding, cache, queue.

## News feed

### Functional requirements

- Create posts
- Follow users
- See a feed of posts from people you follow, newest or ranked first

### Non-functional

- Feed loads fast (cached)
- Eventual consistency is fine: a post can take seconds to appear
- Very read-heavy

### Estimates

Assumptions: dau = 100,000,000, feed loads = 10, posts per user = 1, avg followers = 200.

|                                                |         |
|------------------------------------------------|---------|
| Feed reads per second                          | 11.6 K  |
| Posts per second                               | 1.2 K   |
| Feed inserts per second if fanned out on write | 231.5 K |

### API

- POST /posts {text, media_ids}
- GET /feed?cursor=…&limit=20
- POST /users/{id}/follow

### Data model

- posts(post_id PK, author_id, text, media_url, created_at)
- follows(follower_id, followee_id)
- feed cache: per-user list of recent post ids (Redis)

### Design

- Hybrid fan-out: for normal users, a worker pushes each new post id into followers' feed caches (fan-out on write); for accounts with millions of followers, merge their posts at read time (fan-out on read).
- Feed read: fetch post ids from the user's cache, then post bodies from a post cache, then rank.
- Media goes to object storage and is served through a CDN.
- Posting publishes to a queue, so the write returns quickly.

### Trade-offs

|                          |                                                                                                                      |
|--------------------------|----------------------------------------------------------------------------------------------------------------------|
| Fan-out on write vs read | Write: fast reads, heavy writes for popular authors. Read: cheap writes, slow reads. Hybrid uses each where it fits. |
| Ranking                  | Chronological is simple and predictable; ranked needs a scoring service and more data.                               |

Building blocks used: load balancer, cache, queue, database, sharding, object storage, cdn.

## Notification service

### Functional requirements

- Send push, SMS and email notifications for other services
- Respect user preferences and quiet hours
- Templates and per-channel retries

### Non-functional

- No duplicates for the same event; no notification lost
- Absorb spikes (sales, outages)
- Each channel's provider failure must not block the others

### Estimates

Assumptions: per day = 1,000,000,000, peak = 5.

|                           |        |
|---------------------------|--------|
| Average notifications/s   | 11.6 K |
| Peak notifications/s (×5) | 57.9 K |

### API

- POST /notifications {idempotency_key, user_id, template_id, data, channels, priority} → 202 Accepted
- GET /notifications/{id} → status per channel

### Data model

- requests(idempotency_key UNIQUE, user_id, template_id, status, created_at)
- preferences(user_id, channel, enabled, quiet_hours)
- templates(id, channel, body)

### Design

- API validates, dedupes on the idempotency key, checks preferences and rate limits per user, then writes to one queue per channel (and priority).
- Channel workers render templates and call providers (APNs/FCM, an SMS gateway, an email service) with retries and exponential backoff; failures after N tries go to a dead-letter queue.
- Separate queues per channel isolate failures: an SMS outage does not delay push.
- Delivery status events are stored and exposed for debugging.

### Trade-offs

|                        |                                                                                  |
|------------------------|----------------------------------------------------------------------------------|
| At-least-once delivery | Simpler and safer than exactly-once; needs idempotency keys to avoid duplicates. |
| Priority queues        | Urgent messages (OTPs) bypass bulk campaigns; more queues to run.                |

Building blocks used: load balancer, queue, database, rate limiting, monitoring.

## File storage and sync

### Functional requirements

- Upload, download and share files
- Sync changes across a user's devices
- Version history

### Non-functional

- Never lose a file (high durability)
- Large files resume after a network drop
- Save bandwidth: only changed parts are uploaded

### Estimates

Assumptions: dau = 10,000,000, uploads per user = 2, avg file mb = 1, chunk mb = 4.

|                                      |         |
|--------------------------------------|---------|
| Uploads per second                   | 231.5   |
| New data per day (bytes)             | 20.0 TB |
| New data per year (bytes)            | 7.3 PB  |
| Chunks for a 1 GB file (4 MB chunks) | 250.0   |

### API

- POST /files/{path}/uploads → {upload_id, missing_chunk_hashes}
- PUT pre-signed URL per chunk (directly to object storage)
- POST /uploads/{id}/commit → new version
- GET /changes?cursor=… (long poll) for sync

### Data model

- files(file_id, owner_id, path, latest_version)
- versions(file_id, version, chunk_hashes\[\], size, created_at)
- chunks stored in object storage by content hash (deduplicated)

### Design

- Clients split files into 4 MB chunks and hash them; the server answers which hashes it does not have, so unchanged chunks are never uploaded again.
- Chunks go straight to object storage with pre-signed URLs; the metadata service records the new version only after all chunks exist (commit).
- Other devices learn about changes through a change log they long-poll (or a notification), then download only missing chunks.
- Metadata in a relational database (sharded by owner); downloads through a CDN for shared links.

### Trade-offs

|            |                                                                                                            |
|------------|------------------------------------------------------------------------------------------------------------|
| Chunk size | Smaller chunks save bandwidth on edits but mean more metadata and requests.                                |
| Conflicts  | Two devices editing offline: keep both versions and let the user choose, rather than silently overwriting. |

Building blocks used: load balancer, object storage, database, sharding, cdn, queue.
