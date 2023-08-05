# -*- coding: utf-8 -*-

"""
Implements the free biclosed monoidal category.
"""

from discopy import messages, monoidal, rigid
from discopy.cat import AxiomError
from discopy.monoidal import BinaryBoxConstructor
from discopy.utils import factory_name, from_tree


class Ty(monoidal.Ty):
    """
    Objects in a free biclosed monoidal category.
    Generated by the following grammar:

        ty ::= Ty(name) | ty @ ty | ty >> ty | ty << ty

    Examples
    --------
    >>> x, y = Ty('x'), Ty('y')
    >>> print(y << x >> y)
    ((y << x) >> y)
    >>> print((y << x >> y) @ x)
    ((y << x) >> y) @ x
    """
    @staticmethod
    def upgrade(old):
        if len(old) == 1 and isinstance(old[0], (Over, Under)):
            return old[0]
        return Ty(*old.objects)

    def __init__(self, *objects, left=None, right=None):
        self.left, self.right = left, right
        super().__init__(*objects)

    def __lshift__(self, other):
        return Over(self, other)

    def __rshift__(self, other):
        return Under(self, other)


class BinaryTyConstructor:
    """ Ty constructor with left and right as input. """
    def __init__(self, left, right):
        self.left, self.right = left, right

    def to_tree(self):
        return {
            'factory': factory_name(self),
            'left': self.left.to_tree(),
            'right': self.right.to_tree()}

    @classmethod
    def from_tree(cls, tree):
        return cls(*map(from_tree, (tree['left'], tree['right'])))


class Over(BinaryTyConstructor, Ty):
    """ Forward slash types. """
    def __init__(self, left=None, right=None):
        Ty.__init__(self, self)
        BinaryTyConstructor.__init__(self, left, right)

    def __repr__(self):
        return "Over({}, {})".format(repr(self.left), repr(self.right))

    def __str__(self):
        return "({} << {})".format(self.left, self.right)

    def __eq__(self, other):
        if not isinstance(other, Over):
            return False
        return self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash(repr(self))


class Under(BinaryTyConstructor, Ty):
    """ Backward slash types. """
    def __init__(self, left=None, right=None):
        Ty.__init__(self, self)
        BinaryTyConstructor.__init__(self, left, right)

    def __repr__(self):
        return "Under({}, {})".format(repr(self.left), repr(self.right))

    def __str__(self):
        return "({} >> {})".format(self.left, self.right)

    def __eq__(self, other):
        if not isinstance(other, Under):
            return False
        return self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash(repr(self))


@monoidal.Diagram.subclass
class Diagram(monoidal.Diagram):
    """ Diagrams in a biclosed monoidal category. """
    @staticmethod
    def fa(left, right):
        """ Forward application. """
        return FA(left << right)

    @staticmethod
    def ba(left, right):
        """ Backward application. """
        return BA(left >> right)

    @staticmethod
    def fc(left, middle, right):
        """ Forward composition. """
        return FC(left << middle, middle << right)

    @staticmethod
    def bc(left, middle, right):
        """ Backward composition. """
        return BC(left >> middle, middle >> right)

    @staticmethod
    def fx(left, middle, right):
        """ Forward crossed composition. """
        return FX(left << middle, right >> middle)

    @staticmethod
    def bx(left, middle, right):
        """ Backward crossed composition. """
        return BX(middle << left, middle >> right)

    @staticmethod
    def curry(diagram, n_wires=1, left=False):
        """ Diagram currying. """
        return Curry(diagram, n_wires, left)


class Id(monoidal.Id, Diagram):
    """ Identity diagram in a biclosed monoidal category. """


Diagram.id = Id


class Box(monoidal.Box, Diagram):
    """ Boxes in a biclosed monoidal category. """


class Curry(Box):
    """
    Curried diagram.

    Parameters
    ----------
    diagram : :class:`Diagram`
        to curry.
    n_wires : int, optional
        Number :code:`<= len(diagram.dom)` of wires to curry,
        default is :code:`1`.
    left : bool, optional
        Whether to curry to the left, default is :code:`False`.
    """
    def __init__(self, diagram, n_wires=1, left=False):
        if left:
            dom = diagram.dom[n_wires:]
            cod = diagram.dom[:n_wires] >> diagram.cod
        else:
            dom = diagram.dom[:-n_wires]
            cod = diagram.cod << diagram.dom[-n_wires or len(diagram.dom):]
        name = "Curry({}{}{})".format(
            diagram, ", n_wires={}".format(n_wires) if n_wires != 1 else "",
            ", left=True" if left else "")
        self.diagram, self.n_wires, self.left = diagram, n_wires, left
        super().__init__(name, dom, cod)


def unaryBoxConstructor(attr):
    class Constructor:
        @classmethod
        def from_tree(cls, tree):
            return cls(from_tree(tree[attr]))

        def to_tree(self):
            return {
                'factory': factory_name(self),
                attr: getattr(self, attr).to_tree()}
    return Constructor


class FA(unaryBoxConstructor("over"), Box):
    """ Forward application box. """
    def __init__(self, over):
        if not isinstance(over, Over):
            raise TypeError(messages.type_err(Over, over))
        self.over = over
        dom, cod = over @ over.right, over.left
        super().__init__("FA{}".format(over), dom, cod)

    def __repr__(self):
        return "FA({})".format(repr(self.dom[:1]))


class BA(unaryBoxConstructor("under"), Box):
    """ Backward application box. """
    def __init__(self, under):
        if not isinstance(under, Under):
            raise TypeError(Under, under)
        self.under = under
        dom, cod = under.left @ under, under.right
        super().__init__("BA{}".format(under), dom, cod)

    def __repr__(self):
        return "BA({})".format(repr(self.dom[1:]))


class FC(BinaryBoxConstructor, Box):
    """ Forward composition box. """
    def __init__(self, left, right):
        if not isinstance(left, Over):
            raise TypeError(messages.type_err(Over, left))
        if not isinstance(right, Over):
            raise TypeError(messages.type_err(Over, right))
        if left.right != right.left:
            raise TypeError(messages.does_not_compose(left, right))
        name = "FC({}, {})".format(left, right)
        dom, cod = left @ right, left.left << right.right
        Box.__init__(self, name, dom, cod)
        BinaryBoxConstructor.__init__(self, left, right)


class BC(BinaryBoxConstructor, Box):
    """ Backward composition box. """
    def __init__(self, left, right):
        if not isinstance(left, Under):
            raise TypeError(messages.type_err(Under, left))
        if not isinstance(right, Under):
            raise TypeError(messages.type_err(Under, right))
        if left.right != right.left:
            raise TypeError(messages.does_not_compose(left, right))
        name = "BC({}, {})".format(left, right)
        dom, cod = left @ right, left.left >> right.right
        Box.__init__(self, name, dom, cod)
        BinaryBoxConstructor.__init__(self, left, right)


class FX(BinaryBoxConstructor, Box):
    """ Forward crossed composition box. """
    def __init__(self, left, right):
        if not isinstance(left, Over):
            raise TypeError(messages.type_err(Over, left))
        if not isinstance(right, Under):
            raise TypeError(messages.type_err(Over, right))
        if left.right != right.right:
            raise TypeError(messages.does_not_compose(left, right))
        name = "FX({}, {})".format(left, right)
        dom, cod = left @ right, right.left >> left.left
        Box.__init__(self, name, dom, cod)
        BinaryBoxConstructor.__init__(self, left, right)


class BX(BinaryBoxConstructor, Box):
    """ Backward crossed composition box. """
    def __init__(self, left, right):
        if not isinstance(left, Over):
            raise TypeError(messages.type_err(Under, left))
        if not isinstance(right, Under):
            raise TypeError(messages.type_err(Under, right))
        if left.left != right.left:
            raise TypeError(messages.does_not_compose(left, right))
        name = "BX({}, {})".format(left, right)
        dom, cod = left @ right, right.right << left.right
        Box.__init__(self, name, dom, cod)
        BinaryBoxConstructor.__init__(self, left, right)


class Functor(monoidal.Functor):
    """
    Functors into biclosed monoidal categories.

    Examples
    --------
    >>> from discopy import rigid
    >>> x, y = Ty('x'), Ty('y')
    >>> F = Functor(
    ...     ob={x: x, y: y}, ar={},
    ...     ob_factory=rigid.Ty,
    ...     ar_factory=rigid.Diagram)
    >>> print(F(y >> x << y))
    y.r @ x @ y.l
    >>> assert F((y >> x) << y) == F(y >> (x << y))
    """
    def __init__(self, ob, ar, ob_factory=Ty, ar_factory=Diagram):
        super().__init__(ob, ar, ob_factory, ar_factory)

    def __call__(self, diagram):
        if isinstance(diagram, Over):
            return self(diagram.left) << self(diagram.right)
        if isinstance(diagram, Under):
            return self(diagram.left) >> self(diagram.right)
        if isinstance(diagram, Ty) and len(diagram) > 1:
            return self.ob_factory.tensor(*[
                self(diagram[i: i + 1]) for i in range(len(diagram))])
        if isinstance(diagram, Curry):
            n_wires = len(self(getattr(
                diagram.cod, 'left' if diagram.left else 'right')))
            return self.ar_factory.curry(
                self(diagram.diagram), n_wires, diagram.left)
        for cls, method in [(FA, 'fa'), (BA, 'ba')]:
            if isinstance(diagram, cls):
                return getattr(self.ar_factory, method)(
                    self(diagram.dom[:1]), self(diagram.dom[1:]))
        for cls, method in [(FC, 'fc'), (BC, 'bc')]:
            if isinstance(diagram, cls):
                left, right = diagram.dom[:1].left, diagram.dom[1:].right
                middle = diagram.dom[:1].right
                return getattr(self.ar_factory, method)(
                    self(left), self(middle), self(right))
        if isinstance(diagram, FX):
            left, right = diagram.dom[:1].left, diagram.dom[1:].left
            middle = diagram.dom[:1].right
            return getattr(self.ar_factory, 'fx')(
                self(left), self(middle), self(right))
        if isinstance(diagram, BX):
            left, right = diagram.dom[:1].right, diagram.dom[1:].right
            middle = diagram.dom[:1].left
            return getattr(self.ar_factory, 'bx')(
                self(left), self(middle), self(right))
        return super().__call__(diagram)


biclosed2rigid_ob = Functor(
    ob=lambda x: rigid.Ty(x[0].name), ar={}, ob_factory=rigid.Ty)


biclosed2rigid = Functor(
    ob=biclosed2rigid_ob,
    ar=lambda f: rigid.Box(
        f.name, biclosed2rigid_ob(f.dom), biclosed2rigid_ob(f.cod)),
    ob_factory=rigid.Ty, ar_factory=rigid.Diagram)
