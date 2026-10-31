# Sign in with Google: setup guide

Copyright (c) 2026 Karcha Studios. All rights reserved.

Ticket Manager can sync your tickets between your PC and your Android phone through your
own Google Drive. For this you create your **own free Google Cloud credentials** once and
enter them in the app. Nothing goes through us, and nobody else's account is involved.
(If this is too much work, you can sync with a sync file instead, with no Google setup.)

What the app can do with it: it gets access to one hidden "app data" folder in your Drive
(the `drive.appdata` permission). It cannot see any of your other files.

Setup takes about 10 minutes and is done once. Use the **same Google account** on every
device you want to sync.

## 1. Create a project
1. Open https://console.cloud.google.com and sign in with your Google account.
2. Create a new project, for example "Ticket Manager".

## 2. Turn on the Google Drive API
**APIs & Services → Library**, search for **Google Drive API**, and click **Enable**.

## 3. Set up the consent screen
Open **Google Auth Platform** (older name: **APIs & Services → OAuth consent screen**).
1. App name: Ticket Manager. Choose your email as the support and contact address.
2. Audience: **External**.
3. **Data access** (scopes): add `https://www.googleapis.com/auth/drive.appdata`.
4. **Audience → Test users**: add your own Google account.
5. Then click **Publish app** (move it to "In production"). If you skip this, Google forces
   you to sign in again **every 7 days**. Publishing your own app for yourself needs no review
   for this permission.
   If Google shows "hasn't verified this app", that is your own app: choose **Advanced**, then
   continue.

## 4. Create the credentials
1. **Clients** (or **APIs & Services → Credentials**) → **Create client**.
2. Application type: **Desktop app**. This exact type is required (also for Android).
3. Name it anything and click **Create**.
4. Copy the **Client ID** (ends with `.apps.googleusercontent.com`) and the **Client secret**.

## 5. Enter them in the app
- **Windows / Linux:** right-click the **Sync** button → **Google credentials…**, paste both, Save.
- **Android:** **More → Google credentials**, paste both, Save.

Do this on each device (the same two values everywhere).

## 6. Sign in and sync
- **Windows / Linux:** click **Sync** → **Sign in with Google**. Your web browser opens: sign in to
  Google and allow access. The app finishes by itself. If no browser opens, use **Open the page** or
  **Copy link** in the app window.
- **Android:** **More → Sync with Google**. Your browser opens; sign in, allow, then switch back to
  the app. It finishes by itself.
- After the first time, click **Sync** (PC) or **More → Sync with Google** (phone) whenever
  you want to update. Sync is manual and the newest edit wins, so keep your devices' clocks
  correct.

## Good to know
- **Keep the secret private.** It is stored on your device in the app's private folder, not
  encrypted. Do not post it online or put it in a repository.
- **Your data:** tickets live in a hidden folder in your Drive. To delete it: Google Drive on
  the web → **Settings → Manage apps → Ticket Manager → Delete hidden app data**. You can
  also remove the app's access at https://myaccount.google.com/permissions, or use
  **Sign out of Google** in the app.
- **Changing credentials** signs you out, and you sign in again.

## Troubleshooting
| Message | What to do |
| --- | --- |
| "Google did not accept the Client ID or secret" | Check you copied both exactly, and that the client type is **Desktop app**. |
| "Google Drive error 403" | The Google Drive API is not enabled in your project (step 2). |
| "Access blocked" or "not a test user" | Add your account under Test users (step 3), or publish the app. |
| "Your Google sign-in expired" | Sign in again. This happens every 7 days if the app was never published (step 3). |
| "Google did not return a sign-in token" | Remove Ticket Manager at myaccount.google.com/permissions, then sign in again. |
