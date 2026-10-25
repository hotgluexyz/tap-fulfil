# tap-fulfil

A [Singer](https://www.singer.io/) tap that extracts data from **Fulfil**. It is built with [hotglue-singer-sdk](https://github.com/hotgluexyz/HotglueSingerSDK) and speaks the standard Singer message protocol on stdout, so you can pair it with any compatible target.

## Features

- **REST**-style HTTP streams (see `client.py` / `streams.py`).
- **Personal access token** authentication via the `X-API-KEY` header.
- Configurable **`api_url`** and optional **`start_date`** (see [Configuration](#configuration)).
- Full-table streams that explicitly request only the fields used by the mapping.

### Streams

| Stream | Endpoint / notes | Primary key |
| ------ | ---------------- | ----------- |
| `accounts` | `GET /model/account` | `id` |
| `contacts` | `GET /model/contact` | `id` |
| `currencies` | `GET /model/currency` | `id` |
| `invoices` | Posted or approved supplier invoices from `GET /model/invoice` | `id` |
| `invoice_lines` | Lines belonging to the streamed supplier invoices from `GET /model/invoice_line` | `id` |

The API is paginated with `page` and `per_page`; the tap requests 100 records
per page and stops when a page contains fewer records.

## Requirements

- Python **3.10+** (see `requires-python` in `pyproject.toml`).

## Installation

1. **Clone** this repository and `cd` into the project directory.
2. **Create `config.json`** in the project root with your credentials and settings (see [Configuration](#configuration) for the fields and an example).
3. **Create a virtual environment** and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows, use `.venv\Scripts\activate` instead of `source .venv/bin/activate`.

4. **Install the package** in editable mode:

```bash
pip install -e .
```

5. **Run the tap** (with the venv still activated):

```bash
tap-fulfil --help
```

## Configuration

| Setting | Type | Required | Default | Description |
| ------- | ---- | -------- | ------- | ----------- |
| `start_date` | string (datetime) | no | `2000-01-01T00:00:00Z` | Earliest record date to sync. |
| `api_url` / `base_url` | string | no | `https://dev.fulfil.io/api/v2` | Base URL for the API. `base_url` is used by the Hotglue connector; `api_url` remains supported for local runs. |
| `access_key` | string | yes | — | Fulfil personal access token. |

Run `tap-fulfil --about` (or `tap-fulfil --about --format=markdown`) for the authoritative schema for your installed version.

### Example `config.json`

```json
{
  "start_date": "2000-01-01T00:00:00Z",
  "api_url": "https://dev.fulfil.io/api/v2",
  "access_key": "YOUR_ACCESS_KEY"
}
```

Do not commit real credentials. Prefer environment variables or a secrets manager in production.

### Environment-based config

You can load settings from the process environment using `--config=ENV` (the SDK merges env into config). Env names follow the tap’s setting keys (see `tap-fulfil --about`).

## Usage

With your virtual environment **activated** and `config.json` in place:

Discover stream catalog:

```bash
tap-fulfil --config config.json --discover > catalog.json
```

Run a sync (with optional state):

```bash
tap-fulfil --config config.json --catalog catalog.json --state state.json
```

Pipe to any Singer target:

```bash
tap-fulfil --config config.json --catalog catalog.json | target-jsonl
```

Inspect built-in settings and stream metadata:

```bash
tap-fulfil --about
```

## API / documentation

The default development API host is `https://dev.fulfil.io/api/v2`. API model
endpoints used by this tap are `/model/account`, `/model/contact`,
`/model/currency`, `/model/invoice`, and `/model/invoice_line`.


## License
Apache 2.0 — see `LICENSE` and `pyproject.toml`.
