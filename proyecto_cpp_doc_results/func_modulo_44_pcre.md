# MODULE: pcre

## 1. PURPOSE
This module provides compatibility wrappers for PCRE (Perl-Compatible Regular Expressions) and PCRE2 libraries. It ensures that the code can use either library without modification, abstracting away the differences between the two.

## 2. CORE COMPONENTS
- `COMPAT_PCRE_COMPILE(pattern, pcreerror, pcreerroffset)`: Compiles a regular expression using either PCRE or PCRE2, depending on which is available.
- `COMPAT_PCRE_MATCH(regex, essid, length, match_data)`: Matches a regular expression against a string using either PCRE or PCRE2.
- `COMPAT_PCRE_PRINT_ERROR(pcreerroffset, pcreerr)`: Prints an error message when regular expression compilation fails.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- `stdio.h`: Calls `printf()` to print error messages.

## 4. INCOMING DEPENDENCIES (Used By)
- Any module or file that requires regular expression matching using either PCRE or PCRE2.