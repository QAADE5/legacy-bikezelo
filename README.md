# bikezelo ~ TechMart Pipeline Monitor

A lightweight dashboard that watches the TechMart orders feed, validates every record against data quality rules, and forecasts pipeline throughput.

---

## Setup

```bash
git clone https://github.com/QAADE5/legacy-bikezelo.git
cd legacy-bikezelo
pip install -r requirements.txt
python setup_db.py
```

## Configuration

All settings live in `config.yaml` in the project root - copy `config.example.yaml` to get started. See the comments in that file for each option.

`setup_db.py` creates an empty `data/orders.db`. Running it again deletes the database and starts fresh - all data is synthetic.

## Running

Open two terminals.

```bash
python simulate.py    # terminal 1 - writes a new order every 2 seconds
python app.py         # terminal 2 - starts the dashboard
```

Then open [http://localhost:5000](http://localhost:5000)

---

## What it does

`simulate.py` stands in for the upstream orders feed. Most rows are valid, but roughly 1 in 8 is bad - a missing customer, a negative amount, an unknown status code or a malformed timestamp. Occasionally an incident spike sends a burst of 4-8 bad rows in a row. The database keeps the most recent 500 rows.

The dashboard has two panels:

- **Live feed** - rows appear as they arrive (white), then turn green (passed), amber (warning) or red (failed) when the next validation sweep runs.
- **Pipeline stats** - total rows, passed, warnings, errors, error rate against the SLA, and a forecast of rows per hour.

Validation runs every 10 seconds against the whole table using Great Expectations.

## Rules

Rules live in `rules.py`:

- `get_failures()` - FAIL rules, rows turn red
- `get_warnings()` - WARNING rules, rows turn amber

| Rule | Column | Type |
|------|--------|------|
| Must not be null | `customer_id` | Fail |
| Between 0 and 999.99 | `order_amount` | Fail |
| One of NEW, PAID, SHIPPED, REFUNDED | `status` | Fail |
| Length 4-12 | `customer_id` | Fail |
| Matches `YYYY-MM-DDTHH:MM:SS` | `timestamp` | Warning |

`rules.py` is reloaded on every validation sweep, so a saved change applies without restarting the app. If `rules.py` has an error, the dashboard shows it rather than passing every row.

## Tests

```bash
pytest tests/
```

The tests cover the forecast and the `/data/rows` endpoint. They don't need the simulator or the app to be running.

---

## Project structure

```
legacy-bikezelo/
├── app.py            # Flask app - dashboard and validation
├── rules.py          # Great Expectations rules
├── simulate.py       # Simulated orders feed
├── setup_db.py       # Creates data/orders.db
├── requirements.txt
├── templates/
│   └── index.html    # Dashboard
└── tests/
    └── test_app.py
```

---

*Last reviewed: March 2026 - Dave M*

Training repository - see [SECURITY.md](SECURITY.md).
