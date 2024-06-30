from truealgebra.core.rules import JustOne
from truealgebra.core.naturalrules import NaturalRule
import truealgebra.core.expression as e 

class EqnRule(NaturalRule):
    varstring=" forall(ex0, ex1, ex2, ex3) "

eqnmul = EqnRule(
    pattern = "  (ex0 = ex1) * (ex2 = ex3)  ",
    outcome = "  ex0 * ex2 = ex1 * ex3  "
)

eqnmul0 = EqnRule(
    pattern = "  ex0 * (ex1 = ex2)  ",
    outcome = "  ex0 * ex1 = ex0 * ex2  "
)

eqnmul1 = EqnRule(
    pattern = "  (ex0 = ex1) * ex2  ",
    outcome = "  ex0 * ex2 = ex1 * ex2  "
)

eqnadd = EqnRule(
    pattern = "  (ex0 = ex1) + (ex2 = ex3)  ",
    outcome = "  ex0 + ex2 = ex1 + ex3  "
)

eqnadd0 = EqnRule(
    pattern = "  ex0 + (ex1 = ex2)  ",
    outcome = "  ex0 + ex1 = ex0 + ex2  "
)

eqnadd1 = EqnRule(
    pattern = "  (ex0 = ex1) + ex2  ",
    outcome = "  ex0 + ex2 = ex1 + ex2  "
)

eqnpow0 = EqnRule(
    pattern = "  (ex0 = ex1) ** (ex2 = ex3)  ",
    outcome = "  ex0 ** ex2 = ex1 ** ex3  "
)

eqnpow1 = EqnRule(
    pattern = "  (ex0 = ex1) ** ex2  ",
    outcome = "  ex0 ** ex2 = ex1 ** ex2  "
)

eqnpow2 = EqnRule(
    pattern = "  ex0 ** (ex1 = ex2)  ",
    outcome = "  ex0 ** ex1 = ex0 ** ex2  "
)

eqndiv0 = EqnRule(
    pattern = "  (ex0 = ex1) / (ex2 = ex3)  ",
    outcome = "  ex0 / ex2 = ex1 / ex3  "
)

eqndiv1 = EqnRule(
    pattern = "  (ex0 = ex1) / ex2  ",
    outcome = "  ex0 / ex2 = ex1 / ex2  "
)

eqndiv2 = EqnRule(
    pattern = "  ex0 / (ex1 = ex2)  ",
    outcome = "  ex0 / ex1 = ex0 / ex2  "
)

eqnsub0 = EqnRule(
    pattern = "  (ex0 = ex1) - (ex2 = ex3)  ",
    outcome = "  ex0 - ex2 = ex1 - ex3  "
)

eqnsub1 = EqnRule(
    pattern = "  (ex0 = ex1) - ex2  ",
    outcome = "  ex0 - ex2 = ex1 - ex2  "
)

eqnsub2 = EqnRule(
    pattern = "  ex0 - (ex1 = ex2)  ",
    outcome = "  ex0 - ex1 = ex0 - ex2  "
)

eqnneg = EqnRule(
    pattern = "  -(ex0 = ex1)  ",
    outcome = "  -ex0 = -ex1  "
)

eqnsqrt = EqnRule(
    pattern = "  sqrt(ex0 = ex1)  ",
    outcome = "  sqrt(ex0) = sqrt(ex1)  "
)


eqnmath = JustOne(
    eqnsub0, eqnsub1, eqnsub2, eqnpow0, eqnpow1, eqnpow2,
    eqndiv0, eqndiv1, eqndiv2, eqnneg, eqnsqrt, eqnmul, eqnadd,
    eqnadd0, eqnadd1, eqnmul0, eqnmul1,
)

eqnflip = EqnRule(
    pattern = " ex0 = ex1 ",
    outcome = " ex1 = ex0 "
)
