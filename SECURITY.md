# Security policy

## Supported versions
Only the latest release (1.0) receives security fixes.

## Reporting a problem
Please **do not** open a public issue for a security problem.
Use GitHub's private reporting instead: open the **Security** tab of this repository and
choose **Report a vulnerability**. Include what you found, the steps to reproduce it, and the
app and version you used. Please do not include real tickets, Google credentials or tokens.

You will get a reply as soon as the maintainer can. Please give a reasonable time to fix the
problem before telling anyone else.

## Things worth knowing
- Tickets are stored locally. Nothing is uploaded unless you turn on sync.
- With Google sync, your own Google Client ID, secret and sign-in token are stored in the
  app's data folder (readable only by your user on Linux) and, on Android, in the app's private
  storage. They are not encrypted. Keep your Client secret private, and never commit it.
