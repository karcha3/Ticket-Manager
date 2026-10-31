# Changelog

All notable changes to Ticket Manager are listed here.

## 1.0 (2026)

First stable release.

### Windows and Linux app
- Add, edit, duplicate and delete tickets, with calendar and clock pickers
- Search, venue tabs, sortable columns, and a status bar with the total value
- Export CSV and **Import CSV** (rows already in the app are skipped)
- **Sync** between devices through a sync file in a cloud folder, or by signing in
  with Google (your own Google Cloud credentials, see `GOOGLE-SETUP.md`)
- Light and dark mode (fixed styling of dialogs, message boxes and the Duplicate button)
- Linux AppImage
- Windows installer with a license page

### Android app (new)
- Tickets, search, venue tabs, date and time pickers, CSV import and export
- Sync with the other apps
- Ticket codes: show a QR code or Code 128 barcode, scan a code to check a ticket and
  mark it as used

### Under the hood
- Each ticket now has a hidden unique id, a "last changed" time and a deleted flag so
  that sync can tell edits and deletions apart. Existing data is upgraded automatically.
