from typing import List

from rb.core.lang import Lang
from rb.complexity.measure_function import MeasureFunction
from rb.core.text_element_type import TextElementType
from rb.complexity.measure_function import MeasureFunction
from rb.core.pos import POS as PosEum

# create all indices
# dependencies need to be putted in function because otherwise circular dependencies happens
def create(lang: Lang) -> List["ComplexityIndex"]:
    from rb.complexity.cohesion.adj_cohesion import AdjCohesion
    indices = [AdjCohesion(lang=lang, reduce_depth=TextElementType.SENT.value, reduce_function=MeasureFunction.AVG)]
    #indices = [DepIndex(lang, dep, TextElementType.BLOCK, MeasureFunction.AVG) for dep in DepEnum]
    #indices += [DepIndex(lang, dep, TextElementType.BLOCK, MeasureFunction.STDEV) for dep in DepEnum]
    return indices