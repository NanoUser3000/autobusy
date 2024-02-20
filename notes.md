## For the developers

### Notes about logging

_IMPORTANT_: **logging on level ERROR and above mandates
that there is a `'details'` key in `extra`.**

- Log things that shouldn't happen, and should be fixed or diagnosed
  on these levels (ERROR, EXCEPTION and CRITICAL).
- Log things that don't require developers attention
  on lower levels (DEBUG, INFO and WARNING).

Other:

- todo: if there are more details available elsewhere, note it in the log
