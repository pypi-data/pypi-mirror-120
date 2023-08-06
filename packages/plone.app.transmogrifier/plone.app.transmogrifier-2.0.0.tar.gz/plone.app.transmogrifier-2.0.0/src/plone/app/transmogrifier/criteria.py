# -*- coding: utf-8 -*-
from Acquisition import aq_base
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import defaultMatcher
from collective.transmogrifier.utils import traverse
from Products.ATContentTypes.interface import IATTopic
from zope.interface import implementer
from zope.interface import provider


@provider(ISectionBlueprint)
@implementer(ISection)
class CriterionAdder(object):
    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

        self.pathkey = defaultMatcher(options, "path-key", name, "path")
        self.criterionkey = defaultMatcher(options, "criterion-key", name, "criterion")
        self.fieldkey = defaultMatcher(options, "field-key", name, "field")

    def __iter__(self):
        for item in self.previous:
            pathkey = self.pathkey(*list(item.keys()))[0]
            if not pathkey:
                yield item
                continue

            criterionkey = self.criterionkey(*list(item.keys()))[0]
            if not criterionkey:
                yield item
                continue

            fieldkey = self.fieldkey(*list(item.keys()))[0]
            if not fieldkey:
                yield item
                continue

            path = item[pathkey]

            obj = traverse(self.context, str(path).lstrip("/"), None)
            if obj is None:  # path doesn't exist
                yield item
                continue

            criterion = item[criterionkey]
            field = item[fieldkey]

            if IATTopic.providedBy(obj):
                critid = "crit__%s_%s" % (field, criterion)
                if getattr(aq_base(obj), critid, None) is None:
                    obj.addCriterion(field, criterion)
                item[pathkey] = "%s/%s" % (path, critid)

            yield item
