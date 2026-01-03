title: How to read an OpenSSL configuration file
date: 2021-11-18 11:00
modified: 2026-01-03T04:32
status: published
tags: OpenSSL, environment variables
category: research
slug: pki-openssl-reserved-words
summary: After 15 years of barely paying attention to this file, I've finally detailed the syntax of the `openssl.cnf` file.
lang: en
private: False

I’ve stared at `openssl.cnf` more times than I care to remember. After 15 years, I finally decided to fully understand its syntax and semantics—what everything really means and how it’s all connected.

If you're trying to grok an OpenSSL config file—parse it, absorb it, dissect it—here’s the streamlined method.

* What is `openssl.cnf`?
* Why understanding it matters: Cert requests, CA issuance, `s_server`, provider loading
* How OpenSSL parses it (INI + custom logic):

# Historical

`openssl.cnf` was designed by like-minded folks who also designed OIDs, SNMP MIBs, and ASN1 as well as X.509.

In this article, I will outline what or which actual keywords that the OpenSSL will be looking for when constructing a list of configurable values before creating your certificate-request, and other certificates.

# Step Back: External Influences


But before we go further into `openssl.cnf`, we have to consider who the external influencers can be when using the `openssl` binary: the shell environment variables.

I've identified the following shell environment names used by `openssl` 
(by scanning for `getenv()` functions and few other code review tricks)
and compiled a list of them in this [OpenSSL Environment Variables]({filename}openssl-envvars.md) article.

With that out of the way, we can now delve into OpenSSL configuration file 
syntax for all its simplicity.


## Why So Complicated?

I do believe that the OpenSSL configuration file syntax was 
originally designed to perform testing and fuzzing of its many settings; 
later, it became the de facto configuration for its various 
certificate creations.

So when you execute `openssl s_client` or `openssl s_server`, a whole new keyword set of OpenSSL configuration get used other than the default ones that we all are familiar with which is `/etc/ssl` (or `/etc/pki/tls` for RedHat).

# INI Format
The OpenSSL config file is formatted much like a classic INI file.

INI file is divided into:  

* section marker
* key-value assignment
* comment line

The INI specification is given [here](https://cloanto.com/specs/ini/).  
  

## Section Marker
Each section begins with a header.

A section groups the related configuration entries, such as default 
settings for certificate requests or CA behavior.

Section blocks are each declared in `[brackets]`:

```ini
[section_name]
```

Conventionally, section name are in lowerSnakeCase ("`a_label_here`") spelling.  This section naming convention is not enforced by `openssl` parser.

## Key-Value Pairs

Individual settings within each section follow the "`key = value`" format.

Inside a section, each line is a simple key–value assignment; each non-comment, non-section, non-period-starting line follows:

```ini
key = value
```


# OpenSSL Configuration File
But wait, there's more to the OpenSSL configuration file.

There are some additional differences between traditional INI format and `openssl.cnf`.:

OpenSSL configuration file is divided into:  

* section marker
* key-value
* pragma (special, like include statement to pull in another file)
* comment line: using `#` or `;`


Essentially, it's an INI-style configuration file, but with beefy enhancements.


## Key-Value
In INI file, the data type of value that gets assigned to a key is a string/integer.

For OpenSSL, changes are made to value to support multiple value types.

OpenSSL may interpret these string values as specific types based on context, keywords, or suffixes, not just a string/integer type.


### Value of a Key
You can obtain data from other previous defined keys using the `$key` syntax:

```ini
dir = /etc/ssl
private_key = $dir/private/ca.key
```

Here, `$dir` is replaced with `/etc/ssl`.


### Context-based Interpretation
In context, the value may be:

* integer
* section reference that points to a DN or during init (`[openssl_conf]`).
* string, user-promptable
* comma-separated list
* OID string
* file/directory path value

### Keyword-based Interpretation
In keyword-based interpretation, the value may be:


prompt
Controls prompting behavior (yes/no)
default_md
Message digest algorithm (e.g., sha256, sha512)
string_mask
Controls character filtering (e.g., utf8only)
encrypt_key
Boolean — encrypt the output key
policy
Section reference — used for CA validation rules
x509_extensions
Section reference — used to define cert extensions
dir
Directory — often used with $dir/ variable expansion
RANDFILE
Path to a seed file — used in randomness generation

### Suffix-Based Behavior
In suffix-based interpretation, the value may be:

OpenSSL recognizes specific suffixes on variable names that modify how the values behave, especially during certificate requests.
#### Prompting Behavior in DN Fields
Suffix
Behavior
_default
Default value shown during prompt
_value
Pre-fills and disables the prompt
_min
Enforces a minimum string length during user input
_max
Enforces a maximum string length

Example:
```ini
[req_distinguished_name]
CN = Common Name
CN_default = www.example.com
CN_value = example.com
CN_min = 5
CN_max = 64
```

#### Section Nesting / Grouping
Suffixes can also denote logical groupings (naming-convention only, not syntactically enforced by `openssl` parser):
Suffix
Meaning / Convention
_dir
Indicates a directory path (e.g., certs_dir)
_cert
Refers to certificate settings (e.g., usr_cert)
_ca
Refers to CA-specific sections (v3_ca)
_sect
Conventionally used in TLS provider sections

### String recap
Beyond standard INI for key value and accepting just an ordinary string type, OpenSSL adds:

* Section references via values
* Shell environment variables via "`$ENV::VAR`"
* Includes using `.include` directives (for building out even more)
* Special metadata via `.pragma` directives (for more crazy stuff)

And OpenSSL value in key-value assignments may be:

  * simple data (like "`sha256`" or "`/etc/ssl`")
  * section name
  * another key name, using "`$<variable>`"
  * list of key or section name, comma-separated
  * key name can be used to reference a section name, thus including a group even more key-values if such key name is used as value.
  * environment variables reference from its current shell session are accessible for assignments into a key (e.g., "`$ENV::HOME`")


## Sections

### `[default]` section

A special "`[default]`" section is optional, but all key-values that occur from the beginning of the file to before the very first section marker NOT marked by a "`[default]`" name are default values.


### Distinguished Name ([req_distinguished_name])


Used in the `[ req_distinguished_name ]` section when creating certificate requests:

```ini
[ req_distinguished_name ]
C = Country Name (2 letter)
ST = State or Province Name
L = Locality Name
O = Organization Name
CN = Common Name
```

Keys (C, ST, L, O, CN) correspond to DN attributes.

Values are used as prompts or defaults during CSR generation.


### Request Configuration ([req], [*_req])

Settings for openssl req:

    default_bits, default_md, prompt, distinguished_name, req_extensions, encrypt_rsa_key, string_mask

### Certificate Authority ([ca], [*_ca])

For openssl ca:

    dir, certs, new_certs_dir, database, serial, default_days, policy, private_key, x509_extensions

### X.509 Extensions ([v3_ca], [usr_cert], [ocsp_cert])

Certificate behaviors:

basicConstraints = CA:TRUE
keyUsage = digitalSignature, keyCertSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer

### Custom OIDs ([new_oids])

Add numeric OIDs with aliases:

myPolicy = 1.2.3.4.5


### TLS / Network Sections ([tls], [credentials], etc.)

Used by openssl s_client/s_server:

    Define cipher suites, trusted certs, providers.

### OpenSSL Initialization ([openssl_conf], etc.)

Loads providers & applies global config:

```ini
providers = provider_sect, activate = 1
```

Keywords used within `openssl_conf`

* `providers`
* `default`
* `activate`

#### `providers`
You define and activate providers in the OpenSSL config file using a section like:

```ini
openssl_conf = openssl_init

[openssl_init]
providers = provider_sect

[provider_sect]
default = default_sect
fips = fips_sect

[default_sect]
activate = 1

[fips_sect]
activate = 1
```

`providers` points to a section where each key (like default or fips) corresponds to a provider config.

Each provider section (e.g., `[default_sect]`) has activate = 1 to enable it.

#### `default`

Once again, `default` is not a reserved word.  Can be used as a section name ("`[default]`") or keyword used in "provider" context.

In OpenSSL 3.x:

```ini
[openssl_init]
providers = provider_sect

[provider_sect]
default = default_sect

[default_sect]
activate = 1
```

Here, default is just the name of a provider — not a reserved keyword.

It maps to a section [default_sect] where you configure whether to activate that provider.

The default provider contains:

Standard crypto like AES, SHA-256, RSA, etc.

It's built into OpenSSL 3 by default.
    
#### `activate`
In OpenSSL 3.x configuration files, when you declare a provider (e.g., `default`, `fips`, `legacy`), you must use:

```ini
activate = 1
```

This tells OpenSSL to activate (load and enable) the provider at runtime.

Example:

```ini
[openssl_init]
providers = provider_sect

[provider_sect]
default = default_provider
fips = fips_provider

[default_provider]
activate = 1

[fips_provider]
activate = 1
```

This configuration will load both the default and fips providers.

Without "`activate = 1`", the section is defined but not used — the provider will not be loaded.
    
    
### Sect section

The `openssl s_client` command evokes the `[sect]` section.

Section name under `sect` and `*_sect` are:

  - `provider_sect`
  - `ssl_sect`
  - `server_sect` is used by `openssl s_server`
  - `test_sect`

`_sect` is a conventional suffix and has no special behavior in `openssl`.



## Meta keywords
This section covers things that are not related to key-value.

### Comments

You can place comments on their own line or after configuration values.

Lines can be commented out with `#` or `;`.

#### Full-line comment
```ini
# first comment line
; Another comment style
key = value  # Inline comments also work
```

#### Inline comment
For inline comment syntax, it is all about placing comments at the end of that line without interfering with its assignment value.

Examples:

```ini
[ req ]
distinguished_name = req_distinguished_name  # Inline comment is OK
```

#### Important Caveats

No unquoted # inside values:
If your value contains a `#` and it's not quoted, OpenSSL will treat everything after `#` as a comment.

Problematic:
```ini
some_value = abc#123   # OpenSSL treats "#123" as a comment
```
Correct:
```ini
some_value = "abc#123"  # Now # is treated as part of the value
```

The comment begins at the first unquoted `#`, even if there’s a space before it.

No support for "`//`" or "`;`" as comments like in some INI formats.

### Directives

Anything that starts with a 'period' symbol on its line is an `openssl` parser directive.

Directives tweak parser behavior.


#### Include

To modularize configurations, you can include external files:

A working example of an include statement is:

```ini
.include=conf-includes
.include conf-includes
.include [.conf-includes]
```

This directive allows you to spread configurations across multiple files.

OpenSSL convention is to use "`.include conf-includes`". Others are for legacy support (OpenSSL <v1.2).

Purpose: Defines the base directory for .include when relative paths are used.

Default: Off (relative paths resolved relative to current working directory or `OPENSSL_CONF_INCLUDE`).

Example usage:

```ini
.include = /etc/ssl/extra
```

Makes `.include xyz.cnf` refer to `/etc/ssl/extra/xyz.cnf` file.


#### Pragmas

In OpenSSL's openssl.cnf, the `.pragma` directive controls how the parser handles specific behaviors. 


```ini
.pragma abspath = on        # require absolute .include paths
.pragma dollarid = true     # literal $ in key/value names
.pragma includedir = /libs  # prefix relative paths (obsolete)
```

##### `abspath`

`.pragma abspath` determines whether included file paths must be absolute.

Default: `Off` (relative paths are allowed).

Example usage:

```ini
.pragma abspath = on
```

Forces `.include` directives to use absolute paths, rejecting relative ones.

##### `dollarid`

`.pragma dollarid` controls `$` usage in identifiers.

Default: Off (leading `$` marks a variable reference, e.g., `$var` expands).

When On: `$` is treated literally; variables must be in `${...}` or `$(...)`.

Example sage:

```ini
.pragma dollarid = true
```

Ensures `foo$bar` is literal, not a variable reference.  
  


HISTORICAL: `dollarid` pragma was introduced so that other operating systems who use '`$`' in its shell variable names can use OpenSSL (e.g., DEC Vax VMS, can also use "`SYS$DISK`" ) since 2017.


##### `includedir`

Before OpenSSL v1.1.1, it used to be `.pragma includedir`, now we use `.include` instead.


## Summary Table



OpenSSL config files use an extended INI format

# OpenSSL-Specific Features

## Context: Shell vs Config Interplay

The shell environment can influence behavior via variables such as:

    OPENSSL_CONF, OPENSSL_ENGINES, CTLOG_FILE,
    HTTP_PROXY, NO_PROXY, SSL_CERT_DIR, etc.

These environment variable take effect before parsing `openssl.cnf` and define paths, modules, proxies, logging, etc.





## Value Suffixes and Conventions

`_default`, `_min`, `_max`, `_value` guide prompt behavior

Suffix `_dir` is a naming convention—commonly points to directory paths
(e.g., `new_certs_dir`, `crl_dir`)

These aren’t enforced syntactically, but widely understood by OpenSSL workflows.

## Meta Keywords (Pragmas & Includes)

`.include <file>`: Load another config file

`.pragma <name> [=] <value>`: Adjust parser behavior

Supported pragma names are:

* `abspath`: force absolute include paths
* `dollarid`: treat `$` as literal

* `includedir`: set base for relative includes


## Summary


Variables (`key = value`) can point to data, sections, or environment variables

Supports environment overrides, includes, section nesting, and parser directives

Structured into defined sections with expected keywords for CA, CSR, TLS, etc.

## Sample Minimal Configuration

```ini
[ ca ]
dir = /etc/ssl/myCA
new_certs_dir = $dir/newcerts
default_days = 365
private_key = $dir/private/cakey.pem

[ req ]
default_bits = 2048
default_md = sha256
distinguished_name = req_distinguished_name
req_extensions = v3_req

[ req_distinguished_name ]
C = Country Name (2 letter)
ST = State or Province
L = Locality Name
O = Organization Name
CN = Common Name

[ v3_ca ]
basicConstraints = CA:TRUE
keyUsage = digitalSignature, keyCertSign

[ new_oids ]
myPolicy = 1.2.3.4.5
```


# Sections & Their Keyword Roles



### Starting Section

`openssl_conf` key may be used by OpenSSL to tell `openssl` which section to start with, firstly.

`openssl_conf` key is optionally defined but only from within the "`[default]`" section.

`openssl_conf` is often user-defined to `openssl_init` section.

```ini
# Inside somefile.cnf
openssl_conf = openssl_init  # You must define this key

[openssl_init]
ssl_conf = ssl_module
```

`OPENSSL_CONF` environment variable always overrides any user-defined `openssl_conf` key.


## Sections and Their Keywords
| Section | Typical Keys |
|-----|-----|
| `[req]`/`[*_req]` | `default_bits`, `default_md`, `distinguished_name`, `prompt`, `req_extensions` |
| `[req_distinguished_name]` | `C`, `ST`, `L`, `O`, `CN`, with `_default`, `_min`, `_max` suffixes |
| `[ca]`/`[*_ca]` | `dir`, `certs`, `new_certs_dir`, `default_days`, `policy`, `private_key`, plus ENV vars |
| `[v3_ca]`, `[usr_cert]` | `basicConstraints`, `keyUsage`, `subjectKeyIdentifier`, etc. |
| `[new_oids]` | Custom OID mappings e.g. `myCustomOID = 1.2.3.4.6` |
| `[openssl_conf]`, etc. | Loader directives for providers, initialization |
| `[tls]`, `[credentials]`, `[verification]` (for `s_client`, etc.)	TLS-specific behavior for network commands |

NOTE: Shell-influenced keys like `distinguished_name` = `req_distinguished_name` are essential cross-references.


    
## Section Selectors

`openssl` CLI provides a way to select a specific policy at command line.

A way to add a selectable policy is to pass `-policy <name>` at 
the command line interface and the section `[ policy_<name> ]` will 
then be included.

## Reserve Section Names

There are section names that are reserved.

The section names that the openssl parse will be looking for are:

| Section Name | Purpose / Usage |
|----|----|
| `[openssl_init]` | Initialization section — used to configure OpenSSLs internal library initialization (introduced in OpenSSL 3.0) |
| `[ca]` | Default CA configuration section |
| `[req]` | Certificate request configuration section |
| `[req_distinguished_name]` | Distinguished Name (DN) fields for CSR prompt |
| `[v3_ca]` | Extensions section for CA certificates |
| `[v3_req]` | Extensions section for certificate requests (CSRs) |
| `[alt_names]` | Section defining Subject Alternative Names (SAN) |
| `[policy_match]` or `[policy_anything]` | Certificate issuance policy section for CA |
| `[oid_section]` or `[oid]` | Section defining custom Object Identifiers |
| `[crl_dist_points]` | Extensions for CRL distribution points |
| `[ca_dn]` | Distinguished Name for the CA (less common) |

Do not use those section name unless you intend to have `openssl` parser behave specially on them.

# Specific Section Features
Most prominent of the reserved keywords that OpenSSL MUST expect
is the assignment of the `distinguished_name` to another section of your own
choosing (commonly `req_distinguished_name`).


## Recognized Suffixes

Sometimes, the `openssl` program will leverage suffixes to give a variable name
some additional qualifiers and restrictions.

Suffixes that are `openssl`-recognized are:

  - `*_value` - useful for NOT prompting the user for its value
  - `*_default` - Appears during prompts as a default value during `prompt=no`
  - `*_max` - Restrict length of field to this number of characters.
  - `*_min` - Ensures that a minimum number of characters are typed in

## Built-In Section Names


For certificate creations, the built-in section names are (parenthesis-enclosed are its corresponding environment variable):

  - `[ ca ]`  (`BASE_SECTION`), required
  - `[ req ]`, required
  - `[ providers ]`, optional

Only for TLS network connections, the built-in section names in `openssl.cnf` configuration file that are being used are:

  - `[ connection ]`, optional
  - `[ tls ]`, optional
  - `[ credentials ]`, optional
  - `[ verification ]`, optional
  - `[ commands ]`, optional
  - `[ enrollment ]`, optional

For more details, see [OpenSSL config by section names]({filename}openssl-conf-by-section.md).

## X.509 Extensions

Within extensions sections (e.g., `[ v3_ca ]`, `[ usr_cert ]`), each key is an extension name and its value defines how it behaves:

```ini
[ v3_ca ]
basicConstraints = CA:TRUE
keyUsage = digitalSignature, keyCertSign
```

Extension Names: Such as basicConstraints, keyUsage.

Values: Configuration directives specific to each extension.

## X.509 & OID Integration

    X.509 settings live under [v3_...] sections, defining extensions for cert usage.

    OIDs let you inject custom object identifiers for policies, extensions, or attributes.

## Request section

The `openssl req` command evokes the `[req]` section along with 
any pre-section value settings in `openssl.cnf`

Keywords that are used under `[req]` and `[*_req]` sections are:

  - `attributes`
  - `countryName` or `C`
  - `countryName_default`
  - `countryName_min`
  - `countryName_max`
  - `default_bits`
  - `default_keyfile`
  - `default_md`
  - `distinguished_name`
  - `encrypt_rsa_key`
  - `prompt = no`
  - `string_mask`
  - `x509_extensions`

During `openssl req` request certificate creation, one of the commonly used
keywords are:

  - `req_extensions`
  - `x509_extensions`  # aka V3 extension

Some keywords under `*_extensions` are:

  - `countryName` (or `C`)
  - `organizationName` (or `O`)
  - `commonName` (or `CN`)

## Base CA section

The `openssl ca` command evokes the `[ca]` section.

`ENV_DEFAULT_CA` is the environment variable name that defines internally the
`default_ca` label.

Keywords under `ca` and `*_ca` are:

  - `cert_opt` - Holds the name, often to `ca_default` (`ENV_CERTOPT`)
  - `certificate` - file specification to a PEM-format file; used in `-spkac` and `-gencrl`. (`ENV_CERTIFICATE`)
  - `copy_extensions` (`ENV_EXTCOPY`)
  - `crl_extensions` (`ENV_CRLEXT`)
  - `crlnumber` - positive integer for CRL serial number (`ENV_CRLNUMBER`)
  - `database` - filespec of a text file holding its current serial number (`ENV_DATABASE`)
  - `default_crl_hours` - positive integer of how long to certify revocations (`ENV_DEFAULT_CRL_HOURS`)
  - `default_crl_days` - positive integer of how long to certify revocations (`ENV_DEFAULT_CRL_DAYS`)
  - `default_days` - positive integer of how long to certify for (`ENV_DEFAULT_DAYS`)
  - `default_enddate` - positive integer of when NOT to certify for (`ENV_DEFAULT_ENDDATE`)
  - `default_md` - `default` is compiler-option (`ENV_DEFAULT_MD`)
  - `default_email_in_dn` - `default` is compiler-option (`ENV_DEFAULT_EMAIL_DN`)
  - `default_startdate` - positive integer of when to certify for (`ENV_DEFAULT_STARTDATE`)
  - `msie_hack` (`ENV_MSIE_HACK`)
  - `name_opt` (`ENV_NAMEOPT`)
  - `new_certs_dir` - dirspec of new certificates; used by `openssl new` (`ENV_NEW_CERTS_DIR`)
  - `oid_file` - filespec to OIDs
  - `policy` - The CA policy section to support - CLI '-policy' option (`ENV_POLICY`)
  - `preserve` - Keep passed DN ordering (`ENV_PRESERVE`)
  - `private_key` - filespec of new key; used by `openssl new` (`ENV_PRIVATE_KEY`)
  - `rand_serial`  (`ENV_RAND_SERIAL`)
  - `serial`  (`ENV_SERIAL`)
  - `unique_subject`  (`ENV_UNIQUE_SUBJECT`)
  - `x509_extensions` - points to the next section for extensions (`ENV_EXTENSIONS`)

  - `certs` - dirspec of where certificates go into
  - `crl_dir` - dirspec of where CRL go into
  - `dir` - parent directory of this CA
  - `name_opt` - Holds the name, often to `ca_default`

## Certification section

The certification section may include:

  - `usr_cert`
  - `ocsp_cert`
  - `dh_cert`

Keywords under `*_cert` are:

  - `basicConstraints`
  - `keyUsage`
  - `subjectKeyIdentifier`
  - `authorityKeyIdentifier`

Keywords under `*_ca` are:

  - `basicConstraints`
  - `keyUsage`
  - `subjectKeyIdentifier`
  - `authorityKeyIdentifier`

# Suffixes

Key name may have a certain suffix to denote special behavior by `openssl` parser.  

Many of those certain suffix are found only in certain sections. 

Otherwise, key name with those suffix will be treated just as a special notation for you (and not a behavioral) by `openssl` parser.

Certain suffixes are only found within `[req]`, `[ca]` and `[oid_section]` and are treated as such by `openssl` parser.

Using suffixes outside `[req]`, `[ca]`, and `[oid_section]` are treated just like normal key name, so avoid using the special suffix unless needed.

Suffixes that are expected and processed differently by `openssl` parser are detailed below:

## Recognized Suffixes

These are not truly suffix as it is part of the key's name.

It is just a naming convention.

| " Suffix" | Function |
|-----|-----|
| `_default` | Shown as default during prompts |
| `_value` | Sets value without prompting |
| `_min` | Minimum string length allowed during prompt |
| `_max` | Maximum string length allowed during prompt |
| `_dir` | Conventional suffix for directories (e.g., certs_dir, private_dir) |
| `_file` | Used to denote file paths (e.g., certificate_file) |


## Suffix Conventions & Prompt-Control

    _default, _min, _max, _value: control CLI prompt behavior, defaults, and validations.

    _dir: usually a filesystem path (e.g., new_certs_dir, crl_dir).

## Numeric Suffixes for DN and SAN entries

Used in sections like `[ req_distinguished_name ]`, `[ alt_names ]`, and similar.

Example:

```ini
[ req_distinguished_name ]
commonName                 = Example Corp
organizationName           = Example Org
organizationalUnitName.0   = Research
organizationalUnitName.1   = Security
```

These suffixes (`.0`, `.1`, etc.) allow repetition of fields like OU (`organizationalUnitName`) which would otherwise overwrite each other.

Also applies to:

```ini
subjectAltName → DNS.1, DNS.2, IP.1  # , etc.

email.0, RID.1, URI.0, dirName.0, otherName.1  # in SAN blocks.
```


## `[req]` section suffixes

The `[req]` section is only used by `openssl req` command.

Used for CSR prompt configuration with interactive input.

Valid suffixes recognized only within the "`[req]`" section (and referenced subsections) by `openssl` parser are:

| Suffix | Meaning | Special Parser Behavior? | Notes |
|-----|-----|-----|-----|
| `_default` | Default value shown in prompt | Yes | Used if user hits Enter |
| `_prompt` | Customizes prompt message | Yes | Overrides default message |
| `_value` | Directly supplies value, no prompt | Yes | Overrides prompt even if `prompt = yes` |
| `_min` | Minimum length of input | Yes | Validates user input |
| `_max` | Maximum length of input | Yes | Validates user input |
| `.0`, `.1` | Multiple entries (e.g. `OU.0`, `OU.1`) | Yes | Repeat DN fields |

Only these suffixes are valid here. All others are ignored or treated literally.

These control the user-interface field behavior in the `openssl req` CLI command.


## `[ca]` section suffixes

`_optional`, `_supplied`, `_match` suffixes are used in Certificate Policies.

These suffixes are found in policy sections, like `[policy_anything]`, `[policy_match]`, etc., and are used to define how each Distinguished Name (DN) field should be handled when issuing a certificate.

Not in found in `[req]` section.

Used in `[policy_*]` sections — referenced by the `[ca]`section.

Meaning of Policy Suffixes:

| Suffix | Found In | Purpose |
|-----|-----|-----|
| `_match` | `[policy_*]` | The value in the request must match the value in the issuing cert |
| `_supplied` | `[policy_*]` |  The field must be present in the CSR |
| `_optional` | `[policy_*]` | The field may or may not be present in the CSR |

These are not suffixes of the field name (like `commonName_optional`), but instead values assigned to DN field keys in policy sections, such as:

```ini
commonName = supplied
```

These keywords are values, not suffixes of the field name — so technically, `_optional` and `_supplied` are not suffixes, even though they're suffix-like.

### `_default` suffix

Used to provide default values for fields in req-based certificate requests.

```ini
[ req_distinguished_name ]
countryName                     = Country Name (2 letter code)
countryName_default             = US
countryName_min                 = 2
countryName_max                 = 2
```

If an enter key was pressed at `countryName` prompt, a value of `US` is supplied instead.

### `_min`/`_max` suffix

Used to enforce string length limits for certificate request fields in sections having `req` section or sections with `req_` prefix or `_req` suffix that got referenced by this `req` section.

### `_prompt` suffix
The "`_prompt`" suffix is used to customize the prompt message shown to the user during interactive certificate request (CSR) generation with the `openssl req` command.

Where is _prompt Used?

Only meaningful in the Distinguished Name (DN) sections used by `openssl req`, typically in:

```ini
[req_distinguished_name]
```
Or any other section referenced by `distinguished_name` = ... in the `[req]` section.

If you have a DN field like `commonName`, you can specify a custom prompt by adding `commonName_prompt`.

Example:
```ini
[req]
prompt = yes
distinguished_name = req_distinguished_name

[req_distinguished_name]
commonName = Common Name (e.g., your website's domain)
commonName_prompt = Please enter the domain name for your certificate
commonName_default = example.com
```

When you run:

```bash
openssl req -new -config openssl.cnf
```

The prompt will show:

```
Please enter the domain name for your certificate [example.com]:
```
Important Details

The base field name is the DN attribute, like `commonName`, `organizationName`, `countryName`, etc.

The `_prompt` suffix overrides the default prompt text for that attribute.

Requires `prompt = yes` in the `[req]` section for the prompts to be shown.

If `prompt = no`, the CSR generation uses values from the config file and does not prompt the user.

The prompt supports interactive input, making CSR creation more user-friendly.

Supported Fields for `_prompt` typically works with any DN field in `[req_distinguished_name]`, such as:


* `countryName`
* `stateOrProvinceName`
* `localityName`
* `organizationName`
* `organizationalUnitName`
* `commonName`
* `emailAddress`


| Base Field | Prompt Key | Purpose |
|-----|-----|-----|
| `commonName` | `commonName_prompt` | Custom prompt text for Common Name |
| `organizationName` | `organizationName_prompt` | Custom prompt for Org Name |
| `countryName` | `countryName_prompt` | Custom prompt for Country Code  |

Why Use _prompt?

Makes CSR creation more intuitive for users by providing clear instructions.

Helpful when automating certificate requests with interactive scripts.

Supports multilingual or custom prompt text.
    
## `[oid_section]` suffixes

### `_oid_section` or `_oid_file` Suffixes

While not strictly suffixes on keys, OpenSSL looks for specific section references like:

```ini
oid_section = my_oids

[my_oids]
myCustomOID = 1.2.3.4.5.6
```

Here, the name `oid_section` is a reserved key, and the section name `my_oids` maps to custom OIDs.

## `[policy_*]` section suffixes

Policy section is only used by `openssl ca` command.

Used to enforce policies for cert issuance.

| Value (not suffix) | Meaning | Special Parser Behavior? |Notes |
|----|----|----|----|
| `match` | CSR field must match issuer | Yes | For DN fields |
| `supplied` | Field must be present in CSR | Yes | |	
| `optional` | Field may be omitted | Yes	 | |

These are values, not suffixes. But they are specially interpreted by the `openssl ca` command.


## `[v3_ca]`, `[v3_req]`, `[usr_cert]` section suffixes

Used to define X.509 certificate extensions.

| Suffix | Meaning | Special Parser Behavior? | Notes |
| `_file` | Read value from external file | Yes | Used in `CPS.1_file`, `userNotice.1_file`, etc. |
| `.0`, `.1` | Repeated values (e.g., SAN, policies) | Yes | Common in `subjectAltName`, `CPS`, etc. |

These are interpreted by the certificate generation engine (not the parser alone).

## `[openssl_init]` section suffixes

There are suffixes for this new OpenSSL 3.0+ initialization section.

| Suffix | Special Parser Behavior? | Notes |
|----|----|----|
| `_providers` | No | Naming convention only (e.g., `activate = 1` inside a provider section) |
| `_config` | No | Not special — regular key |
| `_env` | No | Not related to `env:` syntax |

Global or General

| Prefix/Suffix | Context / Meaning | Special Parser Behavior? | Notes |
|----|----|----|----|
| `env:` (prefix) | Value from environment variable | Yes | r.g. `key = env:MY_KEY` |
| `oid:` (prefix) | Use explicit OID | Yes | e.g. `keyUsage = oid:1.2.3.4` |
| `.include` | Include another config file | Yes | Line-level directive |
| `.pragma` | Set parser pragma | Yes | e.g. `.pragma allow_unsafe = 1` |


## `_value` suffix

The `_value` suffix is used to supply a DN field value non-interactively, even if `prompt = yes` is set. It's useful for:

* Pre-setting values while keeping prompts enabled
* Avoiding the need for `_default` and suppressing prompt overrides

* Where `_value` is recognized, only in DN-related sections, such as:

```ini
[req_distinguished_name] — most common
```

* Any section referred to by `distinguished_name = ...` inside `[req]`

* Other DN-like sections (e.g., for `dirName` in SAN)

## `_dir` suffix - Load Directory Path

Used primarily in CA-related contexts, where OpenSSL expects a directory of certificates, CRLs, or related material.

In `[ca]` section and related CA config, dir-like fields such as:

```ini
[ca_default]
dir              = /etc/ssl/ca
certs_dir        = $dir/certs
crl_dir          = $dir/crl
new_certs_dir    = $dir/newcerts
```

While not exactly a suffix, you'll often see _dir-style variables. These are not special parser constructs — they're just conventional names used by OpenSSL CA tools.

Not Used in [req_distinguished_name]

`_file` and `_dir` have no meaning in DN prompt sections.

Elsewhere, these suffixes will be treated as literal key names and ignored or misused.






## _file Suffix — Load File Contents as Value

This is used to tell OpenSSL to read the content of a file and treat that as the value for the key.
📍 Recognized In:

* Extension sections (`[v3_req]`, `[v3_ca]`, etc.)
* Certificate policies
* OCSP responses

Anywhere values are expected to be X.509 textual or binary blobs

Example:
```ini
[usr_cert]
subjectAltName = @alt_names
certificatePolicies = policyInformation_file

[alt_names]
DNS.0 = example.com

[policyInformation_file]
policyIdentifier = 1.3.6.1.4.1.11129.2.5.1
CPS.1_file = /etc/ssl/cps-uri.txt
```
`CPS.1_file` is the content of /etc/ssl/cps-uri.txt, is read and embedded in the certificate.

You might see this used with `CPS`, `userNotice`, `ia5org`, and other X.509 attributes.



## Not Recognized as Special Suffixes


There are additional suffixes that are not internally processed nor syntactically enforced but are used as a general convention for clarity, such as:


* `_providers`
* `_certificate`
* `_key`
* `_config`
* `_env`
* `_file`
* `_dir`

They may be valid as arbitrary key names, but they have no built-in parsing behavior.  They're just a regular key name.  No directory nor files will be accessed nor read into.

These suffixes have no special meaning to the OpenSSL config parser (unless used in app-specific contexts).  In short, if they had those suffixes, they are just a regular key name:

So, while not syntactically enforced, it's a semantic convention that functions as a reserved suffix in behavior and naming consistency.





# Environment Variables

`ENV` is a prefix qualifier that is used to take a shell environment value from its current shell session and use it within its configuration file.

You will see something like:

```ini
    ca_dir = $ENV::HOME/ca
```


Which is to assign a value of `$HOME/ca` to `ca_dir`.

Before parsing config, openssl may commonly read the following environment variables from its current shell session (as found in `/usr/lib/ssl/openssl.cnf`).:

OPENSSL_CONF, OPENSSL_ENGINES, CTLOG_FILE,
HTTP_PROXY, NO_PROXY, SSL_CERT_DIR, RANDFILE, OPENSSL_MODULES,
QLOGDIR, SSLKEYLOGFILE, OPENSSL_ia32cap, …

These adjust paths, engine loading, network behavior, and tracing.



## Shell Environment Variables Used by OpenSSL
## Path & Executable Overrides

 - `CTLOG_FILE` – Specifies an alternate Certificate Transparency log list.

 - `OPENSSL` – Path to the openssl executable (used by scripts like rehash and CA.pl).

 - `OPENSSL_CONF` – Override default config file and include directory. 
 - `OPENSSL_CONF_INCLUDE` – Override default config file and include directory. (effective only on Windows platforms.)
 - `OPENSSL_CONFIG` – Specifically for CA.pl’s req/ca commands: e.g., -config /path/to.cnf.
 - `OPENSSL_ENGINES` – Directory to load dynamic crypto engines from.
 - `OPENSSL_MODULES` – Directory to load provider modules (OpenSSL 3.x feature).

## Debugging & Tracing

 - `OPENSSL_MALLOC_FD` – Built-in debugging for simulating malloc failures.
 - `OPENSSL_MALLOC_FAILURES` – Built-in debugging for simulating malloc failures.
 - `OPENSSL_TRACE` – Enable tracing of internal operations like TLS, providers, engine tables (comma-separated list of trace categories).

## Certificate & RAND Configuration

 - `RANDFILE` – Path to seed file for RNG.
 - `SSL_CERT_DIR` – Default CA bundle directory for SSL connections.
 - `SSL_CERT_FILE` – Default CA bundle file for SSL connections.
 - `CN` - Often used for `commonName`
 - `HOME` - Used in directory variables
 

## Networking / Proxy

OpenSSL (as of version 3.x) looks for proxy settings in the 
following order when making HTTP/HTTPS connections:

 -  `NO_PROXY` – If the destination matches any host/domain in this comma-separated list, OpenSSL won’t use a proxy—even if `HTTP_PROXY` or `HTTPS_PROXY` are set.
 -  `HTTP_PROXY` – Used for plain HTTP (http://) if `HTTPS_PROXY` is absent or not relevant.
 -  `HTTPS_PROXY` – Used for HTTPS only. Takes precedence over `HTTP_PROXY` when the URL scheme is https://.
 
Notably, OpenSSL checks exactly these uppercase of the 
above environment variable names for its proxy 
(it doesn’t look for lowercase variants like `https_proxy`), and in 
this order of precedence.

### Summary of Lookup Order for Proxy

| Scheme | Lookup Sequence                           |
|--------|-------------------------------------------|
| HTTPS  | `NO_PROXY` → `HTTPS_PROXY` → `HTTP_PROXY` |
| HTTP	 | `NO_PROXY` → `HTTP_PROXY`                 |



OpenSSL enforces case sensitivity (uppercase only).

Variables are checked in descending order of precedence.

 - `TSGET` – Arguments for the tsget timestamp-fetch subcommand.

## QUIC & TLS Logging

 - `QLOGDIR` – Where QUIC qlog output is stored.
 - `OSSL_QFILTER` – Controls which QUIC events get logged.
 - `SSLKEYLOGFILE`– Enables TLS session key logging (with build-time support via enable-sslkeylog).


## CPU Architecture

 - `OPENSSL_ia32cap` - Control use of IA32-specific chipset algorithms and instruction sets.
 - `OPENSSL_sparcv9cap` - Control use of Sparc9-specific chipset algorithms and instruction sets.
 - `OPENSSL_ppccap` - Control use of PowerPC-specific chipset algorithms and instruction sets.
 - `OPENSSL_armcap` - Control use of ARM-specific chipset algorithms and instruction sets.
 - `OPENSSL_s390xcap` - Control use of IBM-S390-specific chipset algorithms and instruction sets.
 - `OPENSSL_riscvcap` - Control use of RISC-V-specific chipset algorithms and instruction sets.


## Platform-Specific

 - `OPENSSL_WIN32_UTF8` – (Windows only) Forces UI strings and CLI args to use UTF-8 encoding when set.


## Miscellaneous Environment Variables

The test suite also uses the following shell environment names as well:

  - `ADD_DEPENDS_DEBUG`, util/add-depends.pl
  - `CT_DIR`
  - `CERTS_DIR`
  - `DEBUG`, util/fix-deprecation.pl
  - `EXE_SHELL`
  - `FIPSKEY`
  - `NO_FIPS`
  - `NO_LEGACY`
  - `OPENSSL_CMP_CONF`
  - `PATH` used during compiling/linking/building
  - `SSL_CERT_DIR` used during compiling/linking/building
  - `VERBOSE`
  - `V`



# USAGE

The above enabled me to create parseable CA blocks for my 
test network having many CA certificates.  

And I wrote all the complicated parts in bash SHELL scripts.  

You can find them here [github.com/egberts/tls-ca-manage](https://github.com/egberts/tls-ca-manage).

To incorporate these into automation, my bash-based 
[`tools—tls‑ca‑manage`](https://github.com/egberts/tls%E2%80%91ca%E2%80%91manage) 
on GitHub -- parse, fold, and apply custom logic over 
`openssl.cnf` across a hierarchy of CA files.



## Quick Usage Recap
Task	Section/Directive
Creating a CSR	[req], [req_distinguished_name]
Signing with a CA	[ca], [policy_*], [v3_ca]
X.509 Extension Handling	[usr_cert], [v3_ca], etc.
Environment Substitution	$ENV::HOME, $ENV::CN
OID Definitions	[new_oids]
Auto-loading Providers	[openssl_conf], [providers]
Including Extra Config Files	.include conf.d/extra.cnf

If you'd like, I can render this as a Markdown table-based cheat sheet, suitable for printing or GitHub README embedding. Want that next?


# Putting It All Together

```ini
.pragma abspath = on
.pragma dollarid = true
.pragma includedir = /etc/ssl/includes

[ ca ]
dir = $ENV::HOME/ca
new_certs_dir = $dir/newcerts
default_days = 365
policy = policy_loose
private_key = $dir/private/ca.key
x509_extensions = v3_ca

[ policy_loose ]
countryName = optional
stateOrProvinceName = optional
organizationalUnitName = supplied
commonName = supplied

[ req ]
default_bits = 2048
default_md = sha256
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[ req_distinguished_name ]
C = Country (2 letters)
ST = State or Province
L = Locality
O = Organization
CN = Common Name

[ v3_ca ]
basicConstraints = CA:TRUE
keyUsage = digitalSignature, keyCertSign
subjectKeyIdentifier = hash

[ new_oids ]
egcert = 1.2.3.4.5.6.7.8
```

TL;DR

INI core: sections + key=value + comments + includes

OpenSSL power-ups: section chaining, ENV var injection, pragmas, prompting rules, suffixes

Structured sections map to OpenSSL commands (req, ca, s_client, etc.) and X.509 behaviors

Extendable: add new OIDs, tweak parser, modularize config

For production use, I wrap this approach in tls‑ca‑manage — my bash toolkit for building CA hierarchies from clean, transparent config.


## Default Settings

OpenSSL makes uses of default settings by assigning a section name to one of the
following keywords:

  - `attributes`
  - `default_policy` - if requester did not use a `-policy` CLI option
  - `policy` - always use the policy's section name that is assigned to it
  ## Security & ENV

WARNING: The environment isn’t consulted when `openssl` runs set-uid or 
set-gid binaries, as a security precaution.

To use advanced features like tracing, dynamic engines, or legacy 
providers in OpenSSL 3.x, you may need to compile with options 
like enable-trace or configure provider loading.

Always verify which variables are supported in your installed 
OpenSSL version by executing:  

```bash
openssl version -a
```

## OpenSSL test suite


- `ssl_conf` varname is used by OpenSSL test suite.
- `testapp` varname is used by OpenSSL test suite.
- `config_diagnostics` varname is used by OpenSSL test suite.


```iniT
BITS               "default_bits"
KEYFILE            "default_keyfile"
PROMPT             "prompt"
DISTINGUISHED_NAME "distinguished_name"
ATTRIBUTES         "attributes"
STRING_MASK        "string_mask"
```


### `_dir` Suffix
In OpenSSL config files, `*_dir` is a conventionally reserved suffix 
used to define directory paths for CA operations, cert storage, 
CRLs, and more.

It is not enforced as a strict suffix rule by OpenSSL in the same 
way `_default` or `_value` are for prompting behavior. 
However, OpenSSL tools look for and expect specific keys ending in 
`_dir` in many standard workflows.

The base directory of the CA structure:

```ini
dir = /etc/ssl/myCA
```

Used later to build paths:

```ini
certificate     = $dir/cacert.pem
private_key     = $dir/private/cakey.pem
new_certs_dir   = $dir/newcerts
```



### `new_certs_dir` Usage

Where OpenSSL stores newly issued certificates:

```ini
new_certs_dir = $dir/newcerts
```



### `crl_dir` Usage

Directory for Certificate Revocation Lists:

```ini
crl_dir = $dir/crl
```



### `certs`, `private`, `certs_dir` Usage

Used as well for directory structuring:

```ini
certs = $dir/certs
private = $dir/private
```


# Esoteric Things (Appendix)

## Naming Conventions
| Convention | Description |
|-----|-----|
| `[ca]`, `[req]` | Required section names for openssl ca and openssl | req
| `*_cert` | Sections defining certificate extension sets (e.g., usr_cert) |
| `*_ca` | Sections defining CA behaviors (e.g., intermediate_ca) |
| `*_sect` | Used for TLS-related sections (e.g., ssl_sect, provider_sect) |
| `new_oids` | Used to define custom Object Identifier aliases |
| `openssl_conf` |Used to bootstrap OpenSSL startup via OPENSSL_CONF env var |

## Pragmas Table

| Pragma Directive | Purpose	| Default | Example Usage |
|-----|-----|-----|-----|
| `.pragma abspath` | Require `.include` to use absolute paths| `Off` | `.pragma abspath = on` |
| `.pragma dollarid`	| Treat `$` as literal unless in `${...}` or `$(...)` | `Off` | `.pragma dollarid = true` |
| `.pragma includedir` | Define base directory for resolving relative `.include paths` | `Off` | `.pragma includedir = /conf.d` |

| Element Type | Syntax | Description |
|-----|-----|-----|
|Section header | `[section_name]` | Groups key–value settings |
|Key–value assignment | `key = value` | sets a parameter |
|Variable reference | `$key` | Substitutes earlier values |
| DN field | `CN = Common Name` | Used in certificate requests |
| X.509 extension | `basicConstraints = CA:TRUE` | Defines cert extensions |
| OID alias | `alias = OID-number` | Custom OID mapping |
|Comment | '# ...` or `; ...` | Annotations or disabled lines |
|Include directive | `.include path/to/file` | Inserts another file |
|Pragma directive | `.pragma path/to/file` | Inserts another file |
|Pragma `abspath` | `.pragma on` or `.pragma off` | Restrict .include to absolute paths |
|Pragma `dollarid` | `.pragma dollarid on` or `.pragma dollarid off` | Literal `$` in names; use `${}`/`$()` for variables |
| Pragma `includedir` `.pragma includedir path/to/dir` | Prefixes relative `.include` paths if `OPENSSL_CONF_INCLUDE` is unset |
