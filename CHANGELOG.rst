=========
Changelog
=========

v1.3 (2018-08-15)
=================

- Added ``cache`` and ``cache_timeout`` templatetag arguments to store rendered
  values in cache.
- Added ``data_response`` AppConfig method to globally override the template
  tag response.

v1.2 (2018-08-14)
=================

- Added support for Django 2.1 and Python 3.7.
- Added proper documentation.
- Added ``sri`` (Subresource Integrity) encoder to generate a sha256 for a
  given file.

v1.1 (2018-08-09)
=================

- Added support for custom data encoders to modify file content on the fly.
- Added ``data`` and ``base64`` encoders, both convert data into base64.

v1.0 (2018-04-29)
=================

- 🌟 Initial release.
