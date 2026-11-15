# Cross-site scripting

## The bug
Cross-site scripting (XSS) lets an attacker run JavaScript in another user's browser, usually by getting unescaped input into a page.

## Types
Reflected XSS comes from the current request, stored XSS is saved on the server and shown to other users, and DOM-based XSS happens entirely in client-side JavaScript.

## The fix
Encode output for the context where it is placed (HTML, attribute, JavaScript or URL). Use a framework that escapes by default and add a Content Security Policy as a second layer.

## Cookies
Mark session cookies HttpOnly so scripts cannot read them, and Secure so they are only sent over HTTPS.
