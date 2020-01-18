from .base import *

# SECURITY WARNING: don't run with debug turned on in production
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret
with open(BACKEND_DIR + '/settings/production.key') as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['localhost']

# https://data-flair.training/blogs/django-caching/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Automatic compression with the caching behaviour provided by Django's ManifestStaticFilesStorage backend
# To use compression without filename hashing => 'whitenoise.storage.CompressedStaticFilesStorage'
# To use compression with filename hashing => 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Override Whitenoise's CompressedManifestStaticFilesStorage with support to exclude frontend's staticfiles
STATICFILES_STORAGE = 'conf.storage.CompressedManifestStaticFilesStorage'

# Exclude static files from whitenoise storage processing
WHITENOISE_EXCLUDE_PATHS = [
    r'^styles[\\/]{1}themes[\\/]{1}',
    r'^frontend[\\/]{1}images[\\/]{1}',
    r'^frontend[\\/]{1}media[\\/]{1}',
    r'^frontend[\\/]{1}fonts[\\/]{1}',
]

# Stores only files with hashed names in STATIC_ROOT.
# This setting is only effective if the WhiteNoise storage backend is being used.
WHITENOISE_KEEP_ONLY_HASHED_FILES = True

# Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
SESSION_COOKIE_SECURE = True

# Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
CSRF_COOKIE_SECURE = True

# If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict
# Transport Security.
#
# HTTP Strict Transport Security lets a web site inform the browser that it should never load the site using HTTP
# and should automatically convert all attempts to access the site using HTTP to HTTPS requests instead.
# It consists in one HTTP header, Strict-Transport-Security, sent back by the server with the resource.
#
# If you set the value of SECURE_HSTS_SECONDS, your web server will inform your client's browser the first time
# he visits your site to exclusively access your website over HTTPS in the future. This applies to the entire
# defined period. If for any reason you no longer provide access to your website over HTTPS the browser couldn't
# access your services anymore.
SECURE_HSTS_SECONDS = 86400  # 60 * 60 * 24 seconds (1 day)

# Without this, your site cannot be submitted to the browser preload list.
SECURE_HSTS_PRELOAD = True

# Without this, your site is potentially vulnerable to attack via an insecure connection to a subdomain.
# Only set this to True if you are certain that all subdomains of your domain should be served exclusively via SSL.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Unless your site should be available over both SSL and non-SSL connections,
# you may want to either set this setting True or configure a load balancer or
# reverse-proxy server to redirect all connections to HTTPS.
#
# If True, the SecurityMiddleware redirects all non-HTTPS requests to HTTPS.
#
# If turning this to True causes infinite redirects, it probably means your site is running behind a proxy
# and can’t tell which requests are secure and which are not. Your proxy likely sets a header to indicate
# secure requests; you can correct the problem by finding out what that header is and configuring
# the SECURE_PROXY_SSL_HEADER setting accordingly.
SECURE_SSL_REDIRECT = True

# Send a Referrer-Policy header. You should consider enabling this header to protect user privacy. If configured,
# the SecurityMiddleware sets the Referrer Policy header on all responses that do not already have it to the value provided.
#
# https://scotthelme.co.uk/a-new-security-header-referrer-policy/
#
# '': an empty value in the Referrer Policy header indicates that the site doesn't want to set a Referrer
# Policy here and the browser should fallback to a Referrer Policy defined via other mechanisms elsewhere. Issuing this
# policy will effectively have no impact but just confirms that the site has intentionally omitted it.
#
# 'no-referrer': instructs the browser to never send the referer header with requests that are made from your site.
# This also include links to pages on your own site.
#
# 'no-referrer-when-downgrade': instructs the browser to not send the referrer header when navigating from HTTPS to HTTP,
# but will always send the full URL in the referrer header when navigating from HTTP to any origin. It doesn't matter
# whether the source and destination are the same site or not, only the scheme.
#
# 'origin': instructs the browser to always set the referrer header to the origin from which the request was made.
# This will strip any path information from the referrer information.
#
# 'origin-when-cross-origin': instructs the browser to send the full URL to requests to the same origin but only send
# the origin when requests are cross-origin. Navigating from HTTPS to HTTP will disclose the secure URL or origin in
# the HTTP request.
#
# 'same-origin': instructs the browser to only set the referrer header on requests to the same origin. If the destination
# is another origin then no referrer information will be sent.
#
# 'strict-origin': similar to 'origin' above but will not allow the secure origin to be sent on a HTTP request, only HTTPS.
#
# 'strict-origin-when-cross-origin': similar to 'origin-when-cross-origin' but will not allow any information
# to be sent when a scheme downgrade happens (the user is navigating from HTTPS to HTTP).
#
# 'unsafe-url': instructs the browser to always send the full URL with any request to any origin.
#
# Recommendations
# ---------------
#
#  - 'strict-origin' or 'strict-origin-when-cross-origin' instead of 'origin' or 'origin-when-cross-origin'.
#    This will at least avoid leaking referrer data over an insecure connection.
#
#  - 'no-referrer-when-downgrade' can be used just to keep referrer data off HTTP connections (when nothing sensitive
#    appears in the URL for the site).
#
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

try:
    from .local import *
except ImportError:
    pass
