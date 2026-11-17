SYSTEM DESIGN · CASE STUDIES II

# Five more designs worked end to end

An API gateway with rate limiting, ride matching, e-commerce checkout and inventory, search autocomplete, and video upload and streaming (none repeated from the first case-studies pack), each following the approach on the System Design one-pager: requirements → estimates → API → data model → design → trade-offs, with a diagram. Every estimate is computed from the stated assumptions, so you can change an assumption and redo the maths the same way.

**In the interview.** Spend 5 minutes on requirements and estimates, 10 on the API, data and high-level diagram, 15 on one or two deep dives the interviewer picks, and the rest on trade-offs and failure cases. Freshers are mostly judged on clear reasoning, not on knowing every tool. See the [system design](knowledge-base/design.md#high-level-system-design-hld) Knowledge Base page.

|                                               |
|-----------------------------------------------|
| [API gateway with rate limiting](#api-gateway-with-rate-limiting)     |
| [Ride matching (Uber-style)](#ride-matching-uber-style)         |
| [E-commerce checkout and inventory](#e-commerce-checkout-and-inventory) |
| [Search autocomplete](#search-autocomplete)               |
| [Video upload and streaming](#video-upload-and-streaming)        |

## API gateway with rate limiting

### Functional requirements

- Route each request to the right backend service by path
- Authenticate requests (verify a JWT once, at the edge)
- Enforce per-client rate limits across all gateway instances
- Log every request for audit and debugging

### Non-functional

- Adds only a few milliseconds of latency
- Highly available: no single gateway instance is critical
- Limits hold even when a client's requests hit different instances

### Estimates

Assumptions: avg rps = 20,000, peak = 3, clients = 1,000,000, counter bytes = 64, log bytes = 500.

|                                                  |          |
|--------------------------------------------------|----------|
| Requests per day                                 | 1.7 G    |
| Peak requests/s                                  | 60.0 K   |
| Rate-limit counter ops/s at peak (1 per request) | 60.0 K   |
| Counter memory for all clients (bytes)           | 64.0 MB  |
| Request logs per day (bytes)                     | 864.0 GB |

### API

- ANY /api/{service}/… → proxied to that service
- 429 Too Many Requests + Retry-After when a client is over its limit
- 401 when the token is missing or invalid

### Data model

- routes(prefix PK, service, timeout_ms) in a config store, cached in every gateway
- Redis: rl:{client}:{window} → count, with a TTL of one window
- Logs streamed to a queue, then to storage and a search index

### Design

- Stateless gateway instances behind a load balancer; each loads the route table into memory and refreshes it on change.
- Rate limiting with a shared Redis: INCR the client's counter for the current window and set its TTL; over the limit → 429. A sliding window (two windows weighted) avoids bursts at window edges.
- Authentication at the edge: verify the JWT signature and expiry once, then pass the user id to services in a trusted header.
- If Redis is down, fail open with a local per-instance limit (keeps the API up) or fail closed for sensitive endpoints; decide per route.

### Trade-offs

|                           |                                                                                                                                         |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Fixed vs sliding window   | Fixed windows are one counter but allow double bursts at the edge; sliding windows or token buckets are smoother at slightly more cost. |
| Central vs local counters | Central Redis is accurate but adds a network hop; local counters are free but let a client exceed the limit by the number of instances. |

Building blocks used: load balancer, rate limiting, cache, monitoring, queue.

## Ride matching (Uber-style)

### Functional requirements

- Riders request a ride from a pickup point
- Match the nearest available driver; driver accepts or declines
- Track the driver's live location and ETA
- Trip lifecycle: requested → matched → in progress → completed

### Non-functional

- Match within a few seconds
- Location updates every few seconds from every online driver
- A driver is never assigned to two riders at once

### Estimates

Assumptions: drivers = 1,000,000, update secs = 4, update bytes = 100, rides per day = 20,000,000, peak = 3.

|                           |         |
|---------------------------|---------|
| Location updates/s        | 250.0 K |
| Location ingest (bytes/s) | 25.0 MB |
| Average ride requests/s   | 231.5   |
| Peak ride requests/s      | 694.4   |

### API

- POST /rides {pickup, drop} → {ride_id}
- WS /drivers/{id}/location ← {lat, lng} every 4 s
- POST /rides/{id}/accept (driver)
- GET /rides/{id} → status, driver, ETA

### Data model

- Driver locations in memory, indexed by geohash cell (Redis GEO or an in-memory grid); not in the main database
- rides(ride_id PK, rider_id, driver_id, status, pickup, drop, times) in a relational DB
- Location history to a queue → cheap storage for analytics

### Design

- Drivers keep a WebSocket open and stream locations to location servers, which update the geo index (sharded by city or geohash prefix).
- Matching: query the geo index for available drivers in the pickup cell and its neighbours, rank by ETA, offer to the best; on decline or timeout, offer to the next.
- Assignment must be atomic: set the driver's status from available to busy with a conditional write (compare-and-set), so two matchers cannot claim one driver.
- Trip state lives in the rides table; status changes are published to a queue for notifications, billing and analytics.

### Trade-offs

|                        |                                                                                                                              |
|------------------------|------------------------------------------------------------------------------------------------------------------------------|
| Geohash vs quadtree    | Geohash cells are simple and shard well but uneven in dense areas; a quadtree adapts to density but is harder to distribute. |
| Push vs pull locations | Pushing every 4 s is fresh but costly; adapt the interval to speed and trip state.                                           |

Building blocks used: load balancer, websocket, cache, database, sharding, queue.

## E-commerce checkout and inventory

### Functional requirements

- Cart, checkout and payment
- Reserve stock at checkout; release it if payment fails or times out
- Order confirmation and history

### Non-functional

- Never oversell, even in a flash sale
- Charge a customer at most once per order, even with retries
- Catalog reads can be slightly stale; stock counts cannot

### Estimates

Assumptions: orders per day = 2,000,000, items per order = 3, peak = 10.

|                          |         |
|--------------------------|---------|
| Average orders/s         | 23.1    |
| Peak orders/s (sale ×10) | 231.5   |
| Peak stock decrements/s  | 694.4   |
| Orders per year          | 730.0 M |

### API

- POST /cart/items {sku, qty}
- POST /checkout {cart_id, Idempotency-Key} → {order_id, status: pending}
- POST /payments/webhook (from the payment provider)
- GET /orders/{id}

### Data model

- stock(sku PK, available, reserved) in a relational DB (strong consistency)
- orders(order_id PK, user_id, status, total, idempotency_key UNIQUE)
- reservations(order_id, sku, qty, expires_at)
- Catalog in a cache and search index (read-heavy, can lag)

### Design

- Reserve with one conditional update: UPDATE stock SET available = available − q, reserved = reserved + q WHERE sku = ? AND available ≥ q; zero rows updated means out of stock. No read-then-write race.
- Idempotency: the client sends an Idempotency-Key; a UNIQUE constraint makes a retried checkout return the same order instead of creating a second one.
- Payment is asynchronous: order 'pending' until the provider's webhook; a saga confirms the reservation on success or releases it on failure; a sweeper releases expired reservations.
- Outbox pattern: write the order and an 'order created' event in one transaction; a relay publishes events to the queue so they are never lost.

### Trade-offs

|                                       |                                                                                                                                                |
|---------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| Reserve at add-to-cart vs at checkout | Cart reservations hold stock hostage; checkout reservations risk 'sold out' at the last step. Most shops reserve at checkout with a short TTL. |
| One database vs per-service databases | One database makes transactions easy; per-service databases need sagas and idempotent steps.                                                   |

Building blocks used: load balancer, database, queue, cache, rate limiting.

## Search autocomplete

### Functional requirements

- Show the top suggestions for the prefix the user has typed
- Suggestions reflect popular queries and update daily
- Filter offensive suggestions

### Non-functional

- Under about 100 ms per keystroke
- Very read-heavy and highly available
- Tolerates suggestions being a day old

### Estimates

Assumptions: dau = 100,000,000, searches per user = 5, requests per search = 4, peak = 3, unique queries = 1,000,000,000, bytes per query = 30.

|                                     |         |
|-------------------------------------|---------|
| Suggestion requests per day         | 2.0 G   |
| Average requests/s                  | 23.1 K  |
| Peak requests/s                     | 69.4 K  |
| Raw query text to aggregate (bytes) | 30.0 GB |

### API

- GET /suggest?q={prefix}&limit=10 → \[suggestions\] (cacheable)

### Data model

- Trie (or prefix → top-k table) with the top 10 completions stored at every node, built offline
- Query logs → daily aggregation job → new trie snapshot
- Sharded by prefix range; replicated for reads

### Design

- Clients debounce keystrokes (about 4 requests per search instead of one per character) and cache results in the browser.
- Serving: requests go through a CDN and cache, then to suggestion servers holding the trie in memory; each lookup is O(prefix length) because top-k is precomputed per node.
- Building: a daily batch job counts queries from the logs, drops rare and blocked queries, builds new trie snapshots and swaps them in atomically.
- Freshness for trending topics: a small real-time layer adds recent spikes on top of the daily snapshot.

### Trade-offs

|                                           |                                                                                                                                             |
|-------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Precomputed top-k vs search at query time | Precomputing makes reads O(prefix) but uses more memory and needs rebuilds; searching the subtree at query time is slow for short prefixes. |
| Daily vs real-time updates                | Daily is simple and stable; real-time catches trends but complicates consistency and abuse filtering.                                       |

Building blocks used: cdn, cache, sharding, queue, database, load balancer.

## Video upload and streaming

### Functional requirements

- Upload a video; process it into several resolutions
- Stream with adaptive quality (the player switches resolution with bandwidth)
- Title, thumbnail and view counts

### Non-functional

- Smooth playback worldwide
- Uploads are never lost; processing can take minutes
- Storage and bandwidth cost is the main constraint

### Estimates

Assumptions: uploads per day = 500,000, upload mb = 300, rendition factor = 1.5, views per day = 100,000,000, watch secs = 300, mbps = 3.

|                                         |          |
|-----------------------------------------|----------|
| New raw video per day (bytes)           | 150.0 TB |
| Stored per day incl. renditions (bytes) | 375.0 TB |
| Streaming egress per day (bytes)        | 11.2 PB  |
| Average egress (bits/s)                 | 1.0 T    |

### API

- POST /videos → {video_id, upload_url} (pre-signed, direct to object storage)
- GET /videos/{id}/manifest.m3u8 (HLS) → segment URLs on the CDN
- POST /videos/{id}/views (batched)

### Data model

- Object storage: originals and renditions as small segments (a few seconds each)
- videos(video_id PK, owner, title, status, renditions, created_at)
- View counts aggregated from a queue, not written per view

### Design

- Clients upload straight to object storage with a pre-signed URL (resumable, multipart), so app servers never carry video bytes.
- Upload complete → event on a queue → transcoding workers produce several resolutions as HLS/DASH segments plus a manifest; status 'ready' when done.
- Playback: the player fetches the manifest and segments from a CDN close to the user and switches quality per segment based on measured bandwidth.
- Views and likes are counted asynchronously; popular videos stay hot in the CDN, old ones move to cheaper storage tiers.

### Trade-offs

|                                   |                                                                                                                               |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| Transcode everything vs on demand | Pre-transcoding all resolutions costs storage for videos nobody watches; on-demand saves storage but delays the first viewer. |
| Segment length                    | Short segments adapt faster and start sooner; long ones are more efficient for the CDN and encoder.                           |

Building blocks used: cdn, object storage, queue, database, load balancer, cache.
