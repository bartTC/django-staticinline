# Changelog

## v1.6 (2024-11-19)

- Python 3.13 compatibility and tests.
- Drop support for Django <= 4.1.
- Drop support for Python 3.8.

## v1.5 (2024-08-11)

- Django 5.0, 5.1 compatibility and tests.
- Python 3.12 compatibility and tests.
- Type annotations.
- Switch from pipenv to Poetry.

## v1.4 (2023-04-29)

- Django 3.2 to 4.2 compatibility and tests.
- Python 3.8 to 3.11 compatibility and tests.

## v1.3 (2018-08-15)

- Added `cache` and `cache_timeout` templatetag arguments to store rendered
  values in cache.
- Added `data_response` AppConfig method to globally override the template
  tag response.

## v1.2 (2018-08-14)

- Added support for Django 2.1 and Python 3.7.
- Added proper documentation.
- Added `sri` (Subresource Integrity) encoder to generate a sha256 for a
  given file.

## v1.1 (2018-08-09)

- Added support for custom data encoders to modify file content on the fly.
- Added `data` and `base64` encoders, both convert data into base64.

## v1.0 (2018-04-29)

- 🌟 Initial release.
