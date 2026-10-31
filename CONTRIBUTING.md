# Contributing

Ticket Manager is proprietary software (see `LICENSE.txt`); the source is published for
viewing. Because of that:

- **Bug reports and ideas are welcome.** Open an issue using the templates.
- **Pull requests are not accepted** unless we agreed on it first in an issue. Code you
  send without agreement may be closed without review.
- By sending a bug report or idea, you allow it to be used to improve the app, with no
  payment or credit owed.

## Before you report a bug
- Check you are on the latest release.
- Remove personal details (names on tickets, Google credentials) from anything you paste.
- For sync problems, say which method you use (sync file or Google).

## Working on the code (maintainer)
```
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
python -m unittest discover -s tests -v                # tests need no GUI
```
