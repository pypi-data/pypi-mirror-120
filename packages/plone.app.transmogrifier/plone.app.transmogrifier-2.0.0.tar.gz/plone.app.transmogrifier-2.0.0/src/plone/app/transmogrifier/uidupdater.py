# -*- coding: utf-8 -*-
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import defaultKeys
from collective.transmogrifier.utils import Matcher
from collective.transmogrifier.utils import traverse
from plone.uuid.interfaces import IAttributeUUID
from plone.uuid.interfaces import IMutableUUID
from zope.interface import implementer
from zope.interface import provider


try:
    from Products.Archetypes.config import UUID_ATTR
    from Products.Archetypes.interfaces import IReferenceable

    HAS_AT = True
except ImportError:
    HAS_AT = False


@provider(ISectionBlueprint)
@implementer(ISection)
class UIDUpdaterSection(object):
    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

        if "path-key" in options:
            pathkeys = options["path-key"].splitlines()
        else:
            pathkeys = defaultKeys(options["blueprint"], name, "path")
        self.pathkey = Matcher(*pathkeys)

        if "uid-key" in options:
            uidkeys = options["uid-key"].splitlines()
        else:
            uidkeys = defaultKeys(options["blueprint"], name, "uid")
        self.uidkey = Matcher(*uidkeys)

    def __iter__(self):

        for item in self.previous:

            pathkey = self.pathkey(*list(item.keys()))[0]
            uidkey = self.uidkey(*list(item.keys()))[0]

            if not pathkey or not uidkey:  # not enough info
                yield item
                continue

            path = item[pathkey]
            uid = item[uidkey]

            obj = traverse(self.context, str(path).lstrip("/"), None)
            if obj is None:  # path doesn't exist
                yield item
                continue

            if HAS_AT and IReferenceable.providedBy(obj):
                oldUID = obj.UID()
                if oldUID != uid:
                    if not oldUID:
                        setattr(obj, UUID_ATTR, uid)
                    else:
                        obj._setUID(uid)

            if IAttributeUUID.providedBy(obj):
                mutable_uuid = IMutableUUID(obj)
                old_uid = mutable_uuid.get()
                if old_uid != uid:
                    mutable_uuid.set(uid)

            yield item
