from google.appengine.ext import ndb


class faces(ndb.Model):
    count = ndb.IntegerProperty()
    image_url = ndb.StringProperty()
    rand = ndb.IntegerProperty()


class mslife(ndb.Model):
    count = ndb.IntegerProperty()
    image_url = ndb.StringProperty()
    rand = ndb.IntegerProperty()


class beauty_images(ndb.Model):
    boob = ndb.BooleanProperty()
    count = ndb.IntegerProperty()
    image_url = ndb.StringProperty()
    rand = ndb.IntegerProperty()


class beauty(ndb.Model):
    rank = ndb.IntegerProperty()
    title = ndb.StringProperty()
    year = ndb.IntegerProperty()


class Image(ndb.Model):
    url = ndb.StringProperty()


class Dcard(ndb.Model):
    count = ndb.IntegerProperty()
    url = ndb.StringProperty()
    title = ndb.StringProperty()
    rand = ndb.IntegerProperty()
    rank = ndb.IntegerProperty()
    images = ndb.LocalStructuredProperty(Image, repeated=True)


class Reddit(ndb.Model):
    count = ndb.IntegerProperty()
    image_url = ndb.StringProperty()
    rand = ndb.IntegerProperty()
    rank = ndb.IntegerProperty()
    sub = ndb.StringProperty()
    title = ndb.StringProperty()


class TeaMenuItems(ndb.Model):
    content = ndb.StringProperty(repeated=True)


class TeaMenu(ndb.Model):
    title = ndb.StringProperty()
    names = ndb.StringProperty(repeated=True)
    items = ndb.LocalStructuredProperty(TeaMenuItems, repeated=True)
