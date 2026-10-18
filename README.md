# Ticket Manager

**A Windows app for keeping track of the event tickets you hold.**
Record who each ticket is for, the event, the seat, the date, the price and
the status, all in one searchable table.

Website: https://karcha3.github.io/ticketmanager ([Privacy](https://karcha3.github.io/ticketmanager/privacy.html) · [Terms](https://karcha3.github.io/ticketmanager/terms.html))

## Download

| File | What it is |
| --- | --- |
| [**TicketManager-Setup-1.0.exe**](https://github.com/karcha3/Ticket-Manager/releases/latest/download/TicketManager-Setup-1.0.exe) | The full installer (recommended). Setup wizard, Start menu shortcut, optional desktop shortcut and uninstaller. |
| [TicketManager-Portable-1.0.exe](https://github.com/karcha3/Ticket-Manager/releases/latest/download/TicketManager-Portable-1.0.exe) | Portable version (not the full installation). Just run it, no install needed. |

Requires Windows 10 or 11 (64-bit).

## Features

- Add, edit, duplicate and delete tickets
- Fields for first and last name, venue type, ticket type, venue or event,
  location, date, time, seat or section, price, status and notes
- Calendar and clock pickers for dates and times
- A tab for each venue, created automatically as you add tickets
- Live search across all fields
- Click a column header to sort, and double-click a row to edit it
- Export to CSV (exports what you currently see, including your search and
  the active venue tab)
- Light and dark mode, remembered between launches
- The status bar shows your ticket count and the total price of your tickets,
  not counting cancelled or refunded ones

## Your data

Tickets are stored locally on your PC in `%APPDATA%\TicketManager`. Nothing
is uploaded. Uninstalling or updating the app does not delete your tickets.
Use **Export CSV** to make a backup.

## Good to know

- Windows SmartScreen may show a "Windows protected your PC" warning the
  first time you run the app. Click **More info**, then **Run anyway**.
- The first launch of the portable version can be slow, because it unpacks
  itself each time it starts.

## Building from source (for the owner)

Requires Windows and Python 3.12 (64-bit) with "Add python.exe to PATH"
ticked. To build the installer you also need
[Inno Setup 6.3 or newer](https://jrsoftware.org/isdl.php).

1. Put the project files in one folder (the `.ui` files go in a `ui` folder).
2. Double-click `build_windows.bat`.
3. The exe is created at `dist\TicketManager.exe`, and the installer at
   `installer_output\TicketManager-Setup-1.0.exe`.

To run from source instead: `pip install -r requirements.txt`, then
`python main.py`. To change the version, edit `MyAppVersion` at the top of
`installer\TicketManager.iss`. Do not change `AppId`.

### Project layout

```
main.py             entry point
main_window.py      main window logic (tabs, table, search, export)
ticket_dialog.py    add/edit ticket dialog
database.py         SQLite storage and CSV export
styles.py           light and dark themes
pickers.py          calendar and clock popups
resources.py        file paths (source and built exe)
ui/                 Qt Designer layouts
assets/             app icons
installer/          Inno Setup installer script
```

## License

Copyright (c) 2026 Karcha Studios. All rights reserved. See
[LICENSE.txt](LICENSE.txt). The source is visible for viewing only; copying,
modifying and redistributing it is not permitted.
