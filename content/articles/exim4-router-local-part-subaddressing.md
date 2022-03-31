title: Having `+facebook` Part in `johndoe+facebook@my-mta.net` Email Address
date: 2022-03-30 15:40
status: published
tags: Exim4
category: HOWTO
summary: Google offers you `johnd+XXXX@gmail.com`; Yahoo provides `johnd+XXXX@yahoo.com`; Why not you and your Exim4 mail server?  This guide will help deploy the email subaddressing feature for `local_part` of your email address.  
slug: exim4-router-local-part-subaddressing
lang: en
private: False

Would you like to be able to use different `+XXXX` part of those `johndoe+XXXX@mydomain.test` email subaddress scheme?  

So you got an Exim4 MTA up and running.  Bold enough to customize it?
Scared of tweaking Exim4 or Debian settings?  This article strives to make
this as painless as possible.

You want to give out fancy but DIFFERENT email addresses to 
everyone but use only one account to get them all? 

Fancy emails like:

    johndoe+facebook@my-isp.test
    johndoe-twitter@my-isp.test
    johndoe.instagram@my-isp.test
    johndoe_YxW89z1@my-isp.test    # for someone else

And receive all emails back into your `johndoe` account.  Yeah!

And still see your original `To: johndoe+facebook@my-isp.test`
in any of their reply email to you.

Notice that we can use '`+`', '`-`', '`_`', or '`.`' as the
separator?

Exim4 has an excellent support for subaddressing scheme.  More details here at [Comparison of Local Part in MTAs]({filename}mta-local-part-comparison.md)

How about that?

This article will show you the way, using the Debian split-file mode.
If you are unsure about what Debiam config mode that
your Exim4 mail server is using, check out [this article]({filename}exim4-config-check-which.md)

# Exim4 Config Files, Debian-way

Many of the HOWTOs and blogs frequently advocate mucking with 
the Debian-installed config files for Exim4.  I am saying 
"DO NOT DO THAT!".  

The sole reason for not mucking with Debian-provided 
settings is that the next time that you do a Debian 
package upgrade, you run a severe risk of losing all 
your custom settings (and your email server goes down ... 
probably at the next reboot).

Yeah, there is a way for you to co-exist without directly
changing most of the Debian stuff.

# Hurry, Details, Please

To implement this subaddressing scheme,
we need to clone two of the (Debian-provided)
Exim4 driver files.  The driver names are:

* `userforward` (router subdirectory)
* `local_user` (router subdirectory)

The exact names of those two driver files are both 
in `/etc/exim4/conf.d/router` subdirectory.

1.  `600_exim4-config_userforward`
2.  `900_exim4-config_local_user`

The prefix of those filenames, `600_*` and `900_*`, 
means that in directory lexical order, `600_*` will
get read and processed before the `900_*`.

Because this subaddressing scheme has a more 
restrictive matching criteria, our cloned files will 
be processed before their respective originals.

Let's clone those two files and rename them to 
their respective but slightly smaller numbers.


## Router Driver 590

We will choose the `590_` numeric sequence to be our 
cloned file for `600_exim-config_userforward`:

```bash
cd /etc/exim4/conf.d/router
cp -p 600_exim-config_userforward \
      590_router-custom-userforward-subaddressing
```

Edit the new `590_router-custom-userforward-subaddressing` 
file and cut-n-paste the following info:
```ini
#
# File: 590_router-custom-userforward-subaddressing
# Path: /etc/exim4/conf.d/router
# Title: User Forwarding with Sub-Addressing
# Description:
#
#   This file is a clone of 600_exim-config_userforward
#   that is provided by Debian exim4-config package.
#
#   Its router label has been renamed as 'userforward_subaddressing'
#
#   It is modified to pre-process the subaddressing scheme 
#   of the local_part of the email address:
#
#      username+subaddress@example.text
#
#   For details on its handling, see original 
#   file 600_exim-config_userforward
#
# References:
#   - https://forums.debian.net/viewtopic.php?p=286596

userforward_subaddressing:
  debug_print = "R: userforward_subaddressing for $local_part@$domain"
  driver = redirect
  domains = +local_domains
  check_local_user
  file = $home/.forward
  require_files = $local_part:$home/.forward

  local_part_suffix = -* : +* : _* : .*
  local_part_suffix_optional

  no_verify
  no_expn
  check_ancestor
  allow_filter
  forbid_smtp_code = true
  directory_transport = address_directory
  file_transport = address_file
  pipe_transport = address_pipe
  reply_transport = address_reply
  skip_syntax_errors
  syntax_errors_to = real-$local_part@$domain
  syntax_errors_text = \
    This is an automatically generated message. An error has\n\
    been found in your .forward file. Details of the error are\n\
    reported below. While this error persists, you will receive\n\
    a copy of this message for every message that is addressed\n\
    to you. If your .forward file is a filter file, or if it is\n\
    a non-filter file containing no valid forwarding addresses,\n\
    a copy of each incoming message will be put in your normal\n\
    mailbox. If a non-filter file contains at least one valid\n\
    forwarding address, forwarding to the valid addresses will\n\
    happen, and those will be the only deliveries that occur.
```

Save the file and exit the editor.


## Router Driver 890

For the second file, we will choose `890_` for our cloned file
from `900_exim-config_local_user`.

The second file is like one of the last router driver to perform
after all other routing drivers have been tried (and failed),
but just before its `900_` one.

```bash
cd /etc/exim4/conf.d/router
cp -p 900_exim-config_local_user \
      890_router-custom-local_user_subaddressing
```

Edit the new `890_router-custom-local_user_subaddressing`
to cut-n-paste the following content:
```ini
#
# File: 890_router-custom_local_user_subaddressing
# Path: /etc/exim4/router
# Title: Route for local user having subaddressing 
# Description:
#
#   This file is a clone of '900_exim-config_local_user' 
#   file that is provided by Debian exim4-config package.
#
#   It has been renamed as '890_*' to ensure being 
#   evoked before the '900_exim-config-local_user'.
#
#   Its router label also has been renamed as 
#   'local_user_subaddressing'.
#
#   It is modified to pre-process the adding of
#   subaddressing scheme of the local_part of 
#   the email address:
#
#      username+subaddress@example.text
#
#   For details on its handling, see the original file 
#   900_exim-config_local_user.
#

local_user_subaddressing:
  debug_print = "R: local_user_subaddressing for $local_part@$domain"
  driver = accept
  domains = +local_domains
  check_local_user

## BEGIN of subaddressing addendum

  local_part_suffix = -* : +* : _* : .*
  local_part_suffix_optional

## END of subaddressing addendum

  local_parts = ! root
  transport = LOCAL_DELIVERY
  cannot_route_message = Unknown user
```

Execute `update-exim4.conf` and restart/reload Exim4 daemon/service.

Largely protected from most future package upgrades.

Happy Times.


# Wait, More Details, Please!

Detailing the steps of each line in the 590 router driver, 
the router code reiterated here, sans comments:
```ini
userforward_subaddressing:
  debug_print = "R: userforward_subaddressing for $local_part@$domain"
  driver = redirect
  domains = +local_domains

  check_local_user
  file = $home/.forward
  require_files = $local_part:$home/.forward

  local_part_suffix = -* : +* : _* : .*
  local_part_suffix_optional

  no_verify
  no_expn
  check_ancestor
  allow_filter
  forbid_smtp_code = true

  directory_transport = address_directory
  file_transport = address_file
  pipe_transport = address_pipe
  reply_transport = address_reply

  skip_syntax_errors
  syntax_errors_to = real-$local_part@$domain
  syntax_errors_text = "<error message>"
```

# On The First Day ...

The name of the router driver ends with a colon '`:`' 
symbol: `userforward_subaddressing`.

Based on filename lexical ordering, this 
`userforward_subaddress` router driver gets process 
before its `userforward`.

```ini
userforward_subaddressing:
  debug_print = "R: userforward_subaddressing for $local_part@$domain"
  driver = redirect
  domains = +local_domains
```

`debug_print` only outputs when `-d`, `-v` or `-bt` option is given at the `exim4` CLI and only after checks for `domains`, `local_parts`, and `check_local_user` but before any other pre-conditions are tested.  `debug_print` can be declared
in `auth`, `router`, `transport` driver sections.

Unfortunately, there can only be exactly ONE `debug_print` per driver section.

`driver = redirect` means
