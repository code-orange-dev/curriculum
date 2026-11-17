# Module 04: Running Your Own Relay

| | |
|---|---|
| **Duration** | 2 hours |
| **Level** | Intermediate (comfortable in a terminal; no Go experience needed) |
| **You build** | A custom relay in about 70 lines of Go with [khatru](https://github.com/fiatjaf/khatru), with your own write rules, then a path to run a relay in production with Docker and TLS |
| **Main NIPs** | [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md), [NIP-11](https://github.com/nostr-protocol/nips/blob/master/11.md), [NIP-42](https://github.com/nostr-protocol/nips/blob/master/42.md), [NIP-65](https://github.com/nostr-protocol/nips/blob/master/65.md) |

[Back to the workshop series](../../README.md)

---

## What participants build

1. A throwaway local relay in one command (`nak serve`) to see what a relay does.
2. **Their own relay** written with khatru: persistent storage, a NIP-11 info document, rate limits, a list of allowed event kinds and a members-only write list.
3. A plan for running a relay for real: Docker, a domain, TLS with a reverse proxy, and a look at two popular open-source relays ([strfry](https://github.com/hoytech/strfry) and [nostr-rs-relay](https://github.com/scsibug/nostr-rs-relay)).

## Prerequisites

- A laptop with a terminal.
- [Go](https://go.dev/dl/) 1.24 or newer, for the khatru relay.
- The [`nak`](https://github.com/fiatjaf/nak) CLI: download from its [releases page](https://github.com/fiatjaf/nak/releases) or run `go install github.com/fiatjaf/nak@latest`.
- `curl`.
- Optional: [Docker](https://docs.docker.com), for the production section.
- Optional: a cheap VPS and a domain name if you want to put a relay online after the workshop.

## Safety rules

- Use throwaway keys for testing. Never paste a real `nsec` into a terminal on a shared screen.
- A public relay with open writes will attract spam within days. Start with restricted writes.
- If you run a public relay, you host other people's content. Think about moderation and the law where your server is before you open it up.

## Learning goals

After this module, participants can:

- Explain exactly what a relay does and does not do (it stores, filters and forwards; it never edits events).
- Serve a NIP-11 information document and read other relays' documents.
- Write relay policies: which kinds, which authors, how fast, how big.
- Choose between building a custom relay (khatru) and running an off-the-shelf one (strfry, nostr-rs-relay).
- Put a relay behind TLS so clients can use `wss://`.

## Facilitator run sheet

| Time | Block | Notes |
|---|---|---|
| 0:00 | Welcome and safety | 10 min. Ask who has used a VPS or Docker before. |
| 0:10 | What a relay does | 15 min. Relays as dumb pipes with opinions. NIP-11 on screen. The relay landscape: general, paid, community, personal, specialised. |
| 0:25 | Step 1: a relay in one command | 10 min. `nak serve`, publish and query. |
| 0:35 | Steps 2 to 4: build a khatru relay | 35 min. Go module setup takes a few minutes the first time. Start the download early. |
| 1:10 | Step 5: test the policies with a partner | 15 min. Partners try to write to each other's relays over the LAN. |
| 1:25 | Step 6: production path | 15 min. Docker, Caddy, strfry and nostr-rs-relay. Demo, do not make everyone deploy. |
| 1:40 | Vibe coding extension | 10 min. |
| 1:50 | Discussion and wrap-up | 10 min. |

**Total: 2 hours.**

Facilitator prep: run `go get` for khatru once on your machine and on the venue network, since the first download pulls many modules. Have a pre-built binary of the relay for people whose Go install fails. Check that the venue Wi-Fi lets laptops reach each other (some guest networks isolate clients). If not, use a phone hotspot for Step 5.

---

## What a relay does

- Accepts WebSocket connections.
- On `["EVENT", ...]`: checks the id and signature, applies its own policies, stores the event, answers `["OK", id, true|false, "message"]`, and forwards the event to anyone subscribed with a matching filter.
- On `["REQ", ...]`: runs the filter against storage, sends matches, sends `EOSE`, then streams new matches.
- Serves a NIP-11 JSON document over plain HTTP when asked with `Accept: application/nostr+json`.
- Optionally asks clients to authenticate with NIP-42 `AUTH`.

A relay cannot forge or edit events, because they are signed. It **can** refuse, delete, delay or hide them. That is why users publish to several relays, and why NIP-65 relay lists (kind 10002) tell others where to find you.

---

## Hands-on guide

### Step 1: A relay in one command

```bash
nak serve
```

It prints `relay running at ws://localhost:10547`. In a second terminal:

```bash
nak event -c "hello, local relay" ws://localhost:10547
nak req -k 1 -l 5 ws://localhost:10547
curl -H 'Accept: application/nostr+json' http://localhost:10547
```

`nak serve` keeps everything in memory and forgets it when you stop it. It is perfect for testing clients. Point the Module 02 client at it by setting `RELAYS = ['ws://localhost:10547']`.

### Step 2: Start a khatru project

khatru is a Go framework for writing relays. You decide how events are stored and which ones are accepted.

```bash
mkdir my-relay && cd my-relay
go mod init my-relay
go get github.com/fiatjaf/khatru@v0.19.1
```

### Step 3: Write the relay

Create `main.go`:

```go
// main.go
package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/fiatjaf/eventstore/badger"
	"github.com/fiatjaf/khatru"
	"github.com/fiatjaf/khatru/policies"
	"github.com/nbd-wtf/go-nostr"
)

func main() {
	relay := khatru.NewRelay()

	// NIP-11 information document
	relay.Info.Name = "workshop relay"
	relay.Info.Description = "a small relay built in a Nostr workshop"
	relay.Info.PubKey = os.Getenv("ADMIN_PUBKEY") // hex, optional

	// Storage: Badger is a pure Go key-value database, saved in ./data
	db := badger.BadgerBackend{Path: "./data"}
	if err := db.Init(); err != nil {
		log.Fatal(err)
	}
	relay.StoreEvent = append(relay.StoreEvent, db.SaveEvent)
	relay.QueryEvents = append(relay.QueryEvents, db.QueryEvents)
	relay.CountEvents = append(relay.CountEvents, db.CountEvents)
	relay.DeleteEvent = append(relay.DeleteEvent, db.DeleteEvent)
	relay.ReplaceEvent = append(relay.ReplaceEvent, db.ReplaceEvent)

	// Basic protection: rate limits and no giant filters
	policies.ApplySaneDefaults(relay)

	// Our own rules for who can write what
	allowed := map[string]bool{}
	for _, pk := range strings.Split(os.Getenv("ALLOWED_PUBKEYS"), ",") {
		if pk != "" {
			allowed[pk] = true
		}
	}
	relay.RejectEvent = append(relay.RejectEvent,
		policies.PreventTimestampsInTheFuture(5*time.Minute),
		policies.RestrictToSpecifiedKinds(false, 0, 1, 3, 5, 7, 10002),
		func(ctx context.Context, event *nostr.Event) (bool, string) {
			if len(allowed) > 0 && !allowed[event.PubKey] {
				return true, "blocked: this relay only accepts events from its members"
			}
			return false, ""
		},
	)

	// Log what comes in so we can watch the relay work
	relay.OnEventSaved = append(relay.OnEventSaved, func(ctx context.Context, event *nostr.Event) {
		log.Printf("saved kind %d from %s...", event.Kind, event.PubKey[:8])
	})

	// A plain web page for browsers that are not asking for NIP-11
	relay.Router().HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "This is a Nostr relay. Connect with a Nostr client using ws:// or wss://")
	})

	fmt.Println("relay running on ws://localhost:3334")
	log.Fatal(http.ListenAndServe(":3334", relay))
}
```

Read it top to bottom together. Each `relay.Something = append(...)` adds a hook. khatru calls every hook in the list, so you can stack many small rules.

### Step 4: Run it

```bash
go mod tidy
go run .
```

The first run downloads dependencies and compiles, so give it a minute. Then, in another terminal:

```bash
curl -H 'Accept: application/nostr+json' http://localhost:3334
curl http://localhost:3334
nak event -c "first note on my own relay" ws://localhost:3334
nak req -k 1 -l 5 ws://localhost:3334
```

Stop the relay with Ctrl+C and start it again. Run the `nak req` again: the note is still there, stored in `./data`.

### Step 5: Lock it down and test with a partner

Make a member key and restart the relay so only that key can write:

```bash
SK=$(nak key generate)
PK=$(nak key public $SK)
ALLOWED_PUBKEYS=$PK go run .
```

Now try three writes:

```bash
nak event --sec $SK -c "member note" ws://localhost:3334          # accepted
nak event -c "stranger note" ws://localhost:3334                   # blocked: members only
nak event --sec $SK -k 30023 -c "long article" ws://localhost:3334 # blocked: kind not allowed
```

Partner exercise: find your laptop's LAN address (`ip addr` on Linux, `ipconfig getifaddr en0` on macOS, `ipconfig` on Windows). Give it to your partner. They publish to `ws://<your-ip>:3334`. Add their pubkey to `ALLOWED_PUBKEYS` (comma separated) and try again. Watch your relay's log.

### Step 6: Running a relay for real

You need three things: a server that stays on, a domain name, and TLS so clients can connect with `wss://`.

**Option A: deploy your khatru relay with Docker.** Add a `Dockerfile` next to `main.go`:

```dockerfile
FROM golang:1.25 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /relay .

FROM gcr.io/distroless/static-debian12
WORKDIR /app
COPY --from=build /relay /app/relay
EXPOSE 3334
CMD ["/app/relay"]
```

```bash
docker build -t my-relay .
docker run -d --name my-relay -p 3334:3334 -v "$(pwd)/data:/app/data" -e ALLOWED_PUBKEYS=<hex,hex> my-relay
```

**Option B: nostr-rs-relay (Rust, SQLite).** A mature general-purpose relay configured with a `config.toml` file. Its README documents a Docker build roughly like this:

```bash
git clone https://github.com/scsibug/nostr-rs-relay.git
cd nostr-rs-relay
docker build --pull -t nostr-rs-relay .
mkdir data
docker run -it -p 7000:8080 \
  --mount src=$(pwd)/config.toml,target=/usr/src/app/config.toml,type=bind \
  --mount src=$(pwd)/data,target=/usr/src/app/db,type=bind \
  nostr-rs-relay
```

Edit `config.toml` to set the `[info]` section (name, description, your pubkey) and, to restrict writes, the `pubkey_whitelist` under `[authorization]`. Check the README for the current paths and options before you deploy, since they can change between versions.

**Option C: strfry (C++, LMDB).** Very fast, used by many large public relays, with a plugin system for write policies and built-in sync between relays. It is built from source. On Debian or Ubuntu the steps in its README look like this:

```bash
sudo apt install -y git g++ make libssl-dev zlib1g-dev liblmdb-dev libflatbuffers-dev libsecp256k1-dev libzstd-dev
git clone https://github.com/hoytech/strfry && cd strfry
git submodule update --init
make setup-golpe
make -j4
mkdir -p strfry-db
./strfry relay
```

The default `strfry.conf` listens on `127.0.0.1:7777`. Follow the README if the dependency list has changed.

**TLS with a reverse proxy.** Point a domain (for example `relay.example.com`) at your server. Then [Caddy](https://caddyserver.com) gets a certificate automatically and proxies WebSockets with no extra config. A complete `Caddyfile`:

```
relay.example.com {
    reverse_proxy localhost:3334
}
```

Run `caddy run` in the folder with the `Caddyfile` (or install it as a service). Clients can now use `wss://relay.example.com`. Check it with:

```bash
nak relay wss://relay.example.com
```

**Tell people about it.** Add your relay to your NIP-65 relay list (kind 10002) so clients know to read you there:

```bash
nak event --sec $SK -k 10002 -c '' -t r=wss://relay.example.com -t r=wss://nos.lol wss://relay.example.com wss://nos.lol
```

---

## Vibe coding prompts

Paste `main.go` with the prompt.

1. "Add NIP-42 AUTH to my khatru relay: anyone can read, but only authenticated members can write. Use `khatru.GetAuthed(ctx)` and reject with an `auth-required:` message."
2. "Make a 'paid relay': keep a list of allowed pubkeys in a JSON file, and add an HTTP endpoint that adds a pubkey to the list. Explain how I would connect this to a Lightning payment later."
3. "Add a `RejectFilter` policy that blocks queries asking for more than 500 events, and a per-pubkey rate limit for writes."
4. "Make my relay a 'topic relay': only accept kind 1 notes that contain the hashtag `#bitcoin` in a `t` tag, but accept kind 0 profiles from anyone who has posted at least one accepted note."
5. "Add a simple HTML page at `/` that shows the 20 most recent notes on my relay, rendered safely."
6. "Write a strfry write-policy plugin in JavaScript that only accepts events from pubkeys listed in `members.txt`."

Ask the AI to explain each policy it adds, then test it with `nak event` before you trust it.

## Discussion questions

1. Relays are "dumb" by design. What problems would appear if relays started talking to each other to sync everything?
2. Who pays for relays today? What business models make sense (paid write access, community donations, bundled with a product)?
3. Our relay blocks unknown pubkeys. Is that censorship? How is a relay rule different from a platform ban?
4. What should a relay operator do with illegal content? What can they do, given they cannot edit events?
5. When does it make sense to write a custom relay (khatru) instead of running strfry or nostr-rs-relay?

## Common problems and fixes

| Problem | Fix |
|---|---|
| `go: command not found` or very old Go | Install Go 1.24 or newer from [go.dev/dl](https://go.dev/dl/). Open a new terminal afterwards. |
| `go get` is very slow | The first download pulls many modules. Start it early. On a slow network, share a pre-built binary. |
| `missing go.sum entry` | Run `go mod tidy`, then `go run .` again. |
| `address already in use` | Something else uses port 3334 (maybe an old copy of your relay). Stop it, or change the port in `ListenAndServe`. |
| Partner cannot connect over LAN | Check the IP address, check your firewall allows port 3334, and check the Wi-Fi does not isolate clients. Use a phone hotspot if it does. |
| Writes start failing with `rate-limited` | `ApplySaneDefaults` limits writes per IP. Many people behind one IP (or one laptop running a test loop) hit it fast. Remove it while testing, or tune the limits. |
| Badger error about a lock on `./data` | Another copy of the relay is running in the same folder. Stop it first. |
| `wss://` works locally but not on the server | Check DNS points to the server, ports 80 and 443 are open (Caddy needs both for certificates), and the relay is listening on the port you proxy to. |
| Container cannot write to the data folder | The image may run as a non-root user. Fix ownership or permissions of the host folder you mount. |

## Resources

- [NIP-01: Basic protocol](https://github.com/nostr-protocol/nips/blob/master/01.md) (messages a relay must handle)
- [NIP-11: Relay information document](https://github.com/nostr-protocol/nips/blob/master/11.md)
- [NIP-42: Authentication of clients to relays](https://github.com/nostr-protocol/nips/blob/master/42.md)
- [NIP-65: Relay list metadata](https://github.com/nostr-protocol/nips/blob/master/65.md) (kind 10002)
- [khatru](https://github.com/fiatjaf/khatru) (Go relay framework) and its [package docs](https://pkg.go.dev/github.com/fiatjaf/khatru)
- [strfry](https://github.com/hoytech/strfry) (C++ relay)
- [nostr-rs-relay](https://github.com/scsibug/nostr-rs-relay) (Rust relay)
- [nak](https://github.com/fiatjaf/nak) (CLI, includes `nak serve`)
- [Caddy](https://caddyserver.com) (web server with automatic TLS)

Previous: [Module 03](../03-zaps-and-nwc/README.md) | Next: [Module 05: Nostr for Identity and Authentication](../05-identity-and-auth/README.md)
