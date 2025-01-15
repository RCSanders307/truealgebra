from abc import ABC, abstractmethod


class TranslateChild(ABC):
    def __init__(self, parent): 
# If parent isn't there Make an error
        self.parent = parent

    @abstractmethod
    def predicate(self, obj):
        pass

    @abstractmethod
    def body(self, obj):
        pass


class TranslateParent:
    def __init__(self, *child_classes, **kwargs):
        self.children = list()
        for child_class in child_classes:
            if issubclass(child_class, TranslateChild):
                self.children.append(child_class(parent=self))
            # else: raise error??

    def apply_children(self, obj):
        for child in self.children:
            if child.predicate(obj):
                return child.body(obj)
        return None

    def __call__(self, obj):
        childout = self.apply_children(obj)
        if childout is None:
            return obj
        else:
            return childout

