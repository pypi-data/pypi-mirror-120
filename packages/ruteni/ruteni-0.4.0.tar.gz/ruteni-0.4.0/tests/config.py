import tempfile

from ruteni import configuration
from ruteni.utils.jwkset import KeyCollection

TEST_DIR = tempfile.mkdtemp()
DATABASE_PATH = TEST_DIR + "/test.db"

CLIENT_ID = "client-id"
DOMAIN = "bar.fr"
USER_EMAIL = "username@" + DOMAIN
USER_NAME = "username"
USER_PASSWORD = "lWhgjgjgjHJy765"
USER_LOCALE = "fr-FR"

SESSION_SECRET_KEY = "secret-key"

key_collection = KeyCollection(TEST_DIR, True)
key_collection.generate()
key_collection.export(TEST_DIR + "/public_keys.json", TEST_DIR + "/private_keys.json")

configuration.set("RUTENI_AUTHENTICATION_PRIVATE_KEYS", TEST_DIR + "/private_keys.json")
configuration.set("RUTENI_DATABASE_URL", "sqlite:///" + DATABASE_PATH)
configuration.set("RUTENI_REGISTRATION_FROM_ADDRESS", "Bar Baz <bar@baz.fr>")
configuration.set("RUTENI_REGISTRATION_ABUSE_URL", "<abuse_url>")
configuration.set("RUTENI_SESSION_SECRET_KEY", SESSION_SECRET_KEY)
configuration.set("RUTENI_SITE_NAME", "Ruteni Test")
configuration.set("RUTENI_ENV", "development")
