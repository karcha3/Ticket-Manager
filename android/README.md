# Ticket Manager for Android

Copyright (c) 2026 Karcha Studios. All rights reserved. See `LICENSE.txt`
(the same license covers the Windows app and this Android app).

A native Android (Kotlin, Jetpack Compose, Room) version of Ticket Manager.
Tickets are stored on the phone. The only permission the app requests is internet
access, used only when you choose "Sync with Google".

## Features
Add, edit, duplicate and delete tickets (with calendar and clock pickers for the
date and time) · search · a tab per venue · total
value (not counting cancelled or refunded) · export the current view as a CSV
file · import a CSV exported from this app or the desktop app (rows already in
the app are skipped) · give a ticket a code, show it as a QR code or Code 128
barcode, and scan it to check the ticket and mark it as used · light/dark mode
that follows the phone.

## Sync with the Windows app
Sync keeps the phone and the PC up to date. There are two ways:

**A. Sign in with Google (needs your own free Google Cloud credentials: see `GOOGLE-SETUP.md`).**
Tap **More → Google credentials** and enter your Client ID and secret, then **More → Sync with
Google**. Your browser opens so you can sign in to Google. Your tickets are kept in a hidden
app folder in your Google Drive. Do the same on the PC.

**B. A sync file (no Google setup).** The app connects to the internet only for option A.
1. Menu **More → Sync: create new sync file**, and save `ticket-manager-sync.json`
   in Google Drive.
2. On the PC, click **Sync** and choose that same file (from the Google Drive
   for desktop folder).
3. After that, tap **More → Sync now** (phone) or click **Sync** (PC) whenever you
   want to update. Sync is manual and merges both sides.

How it merges: every ticket has a hidden unique ID and a "last changed" time.
The most recently changed copy wins, and deletions sync too. Keep both devices'
clocks correct, and sync before editing on a second device. Deleted tickets are
kept in the sync file as small markers so that deletions can sync.

## Codes and scanning
- **Code** on a ticket card creates a code like `TM-1A2B3C4D5E6F` (saved with the
  ticket) and shows it as a QR code or a Code 128 barcode.
- In the ticket form you can instead tap **Scan a ticket's code into this field**
  to store the code from a real ticket.
- **Scan** (top bar) reads any code and looks it up in this phone's tickets:
  valid, already used, not valid, or not found. Valid tickets can be marked as used.
- The scanner is Google's code scanner, so it needs Google Play services. The app
  itself only asks for internet access, and only uses it for "Sync with Google".
- Checks only use the tickets stored on this phone. Codes made here are for your
  own bookkeeping and will not be accepted at a venue's entrance.

## Build the APK
1. Install [Android Studio](https://developer.android.com/studio) (current version).
2. **File → Open** and choose this folder. Wait for Gradle sync to finish.
   Accept any suggested Android SDK downloads.
3. Plug in a phone (USB debugging on) or start an emulator, then press **Run**.
4. To get an installable file: **Build → Build Bundle(s) / APK(s) → Build APK(s)**.
   It is created at `app/build/outputs/apk/debug/app-debug.apk`.

For the Play Store you need a signed release bundle (**Build → Generate Signed
App Bundle**) and must meet Google's current target-SDK requirement.

## Not yet tested
This project has not been compiled or run. If Android Studio offers to update
Gradle, the Android plugin or library versions, accepting is fine. The launcher
icon is a small 100 px copy of the desktop icon; replace it with
**Right-click `res` → New → Image Asset**.
