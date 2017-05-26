from happypanda.common import constants, message, exceptions, utils
from happypanda.server.core import db
from happypanda.server.interface import enums

def _get_image(item_type=enums.ItemType.Gallery.name,
              item_ids=[],
              size=enums.ImageSize.Medium.name,
              local=False,
              ctx=None):
    utils.require_context(ctx)

    item_type = enums.ItemType.get(item_type)
    size = enums.ImageSize.get(size)

    db_items = {
        enums.ItemType.Gallery : (db.Gallery, message.Gallery),
        enums.ItemType.Collection : (db.Collection, message.Collection),
        enums.ItemType.Grouping : (db.Grouping, message.DatabaseMessage),
        enums.ItemType.Page : (db.Page, message.Page),
        }

    db_item = db_items.get(item_type)

    content = {}

    s = constants.db_session()

    for i in item_ids:
        
        p_data, p_path = s.query(db.Profile.data, db.Profile.path).filter(
                db_item.profiles.any(
                    db.and_op(
                        db_item.id == i,
                        db.Profile.size == size.name
                        ))).one_or_none()
        if not p:
            raise NotImplementedError
        else:
            if local:
                content[i] = p_path
            else:
                content[i] = p_data


def get_image(item_type=enums.ItemType.Gallery.name,
              item_ids=[],
              size=enums.ImageSize.Medium.name,
              local=False,
              ctx=None):
    """
    Get cover image

    Params:
        - item_type -- ...
        - item_ids -- list of item ids
        - size -- ...
        - local -- replace image content with local path to image file

    Returns:
        a dict of id:content
    """
    return message.Identity("image", content)

def _get_item(item_type=enums.ItemType.Gallery):
    pass

def get_item(item_type=enums.ItemType.Gallery):
    pass

def _get_glists():
    s = constants.db_session()
    return s.query(db.GalleryList).all()


def get_glists():
    """
    Get a list of gallery lists

    Returns:
        a list of gallerylist objects
    """

    glists = message.List("gallerylist", message.GalleryList)
    [glists.append(message.GalleryList(x)) for x in _get_glists()]
    return glists

def _get_tags(taggable_id=0):
    pass


def get_tags(taggable_id=0):
    ""
    pass

def _get_count(item_type=enums.ItemType.Gallery.name):
    ""
       
    item_type = enums.ItemType.get(item_type)

    db_items = {
        enums.ItemType.Gallery : db.Gallery,
        enums.ItemType.Collection : db.Collection,
        enums.ItemType.Grouping : db.Grouping,
        }

    db_item = db_items.get(item_type)

    s = constants.db_session()
    return s.query(db_item).count()

def get_count(item_type=enums.ItemType.Gallery.name):
   """
   Get count of items in the database

   Params:
    - item_type -- type of db item (Gallery, Collection, Grouping)

   Returns
    {'count': int}
   """

   return message.Identity('count', {'count':_get_count(item_type)})
