import math
import scipy.stats as stats
import Tools

### @Author Tomasz Szczepanski
###
### Class for finding a transformation function for a specified dataset that produses a set as close to the normal distribution as possible.
###
### Degree of normality is determined by the Shapiro test.
### Functions avaliable: no transformation, natural logarithm, log10, squareroot
###
### Can be visualized by EnormsDashboard.py

class BestTransform:
    def same(i_x):
        return i_x

    def sqrt(i_x):
        return math.sqrt(i_x)

    def log(i_x):
        if i_x == 0:
            return math.log(0.01)
        return math.log(i_x)

    def log10(i_x):
        if i_x == 0:
            return math.log10(0.01)
        return math.log10(i_x)

    def sqrtReverse(i_x):
        return math.pow(i_x, 2)

    def logReverse(i_x):
        return math.pow(math.e, i_x)

    def log10Reverse(i_x):
        return math.pow(10, i_x)

    # contains touples of the transformation function, its display name and its reverse function
    functions = (
        (same, "original", same),
        (sqrt, "sqrt", sqrtReverse),
        (log, "ln", logReverse),
        (log10, "log10", log10Reverse)
    )

    def transform(array, function):
        array_new = []
        for item in array:
            array_new.append(function(item))
        return array_new

    def getBestTransformedSet(self):
        return self.a_set_transformed[self.i_best_set_index]

    def getBestTransformedSetLabel(self):
        return self.functions[self.i_best_set_index][1]

    def getReverseTransformVal(self, i_x):
        i_counter = 0
        while i_counter < len(self.a_set_transformed[self.i_best_set_index]):
            if self.a_set_transformed[self.i_best_set_index][i_counter] == i_x:
                return self.a_set[i_counter]
            i_counter += 1
        return False

    def getReverseTransformValCompute(self, i_x):
        return self.functions[self.i_best_set_index][2](i_x)

    def getStatsFromBestTransformedSet(self):
        return Tools.get_statistics(self.a_set_transformed[self.i_best_set_index])

    def __init__(self, a_set, s_transformation=None):
        self.a_set = a_set
        self.a_set_transformed = []
        self.a_shapiro_tests = []
        self.i_best_set_index = 0
        i_index = 0
        if s_transformation is None:
            for f in self.functions:
                self.a_set_transformed.append(BestTransform.transform(self.a_set, f[0]))
            for a_set in self.a_set_transformed:
                self.a_shapiro_tests.append(stats.shapiro(self.a_set_transformed[i_index]))
                if self.a_shapiro_tests[len(self.a_shapiro_tests)-1].pvalue > self.a_shapiro_tests[self.i_best_set_index].pvalue:
                    self.i_best_set_index = i_index
                i_index += 1
        else:
            for f in self.functions:
                if f[1] == s_transformation:
                    a = BestTransform.transform(self.a_set, f[0])
                    self.a_set_transformed.append(a)
                    self.a_shapiro_tests.append(stats.shapiro(a))
                    self.i_best_set_index = i_index
                else:
                    self.a_set_transformed.append(None)
                    self.a_shapiro_tests.append(None)
                i_index += 1