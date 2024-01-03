from itertools import chain, combinations
import multiprocessing as mp
from collections import defaultdict

def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))

def getSupport(testSet, itemSetList):
    count = 0
    testSet = set(testSet)
    for itemSet in itemSetList:
        if testSet.issubset(itemSet):
            count += 1
    return count

def calculate_confidence(args):
    itemSet, itemSetSup, minConf, supportCache, detailed_result = args
    subsets = powerset(itemSet)
    if detailed_result:
        rules = []
    else:
        rules = 0
    for s in subsets:
        def has_dpercent(s):
                for idx, x in enumerate(s):
                    if x.startswith('%') and x.endswith('%'):
                        return idx
        # if %% in s, rule[%%] = %%
        idx = has_dpercent(s)
        if idx is not None:
            rules[(s[idx],)] = (set((s[idx],)), 1.0)
            continue
        if len(s) > 0:
            confidence = float(itemSetSup / supportCache.get(s, 0))
            if confidence >= minConf:
                if detailed_result:
                    rules.append([set(s), set(set(itemSet).difference(s)), confidence])
                else:
                    rules += 1
    return rules

def caluculate_association_rule_parallel(freqItemSet, minConf, detailed_result=False):
    supportCache = {tuple(itemSet): support for itemSet, support in freqItemSet}

    pool = mp.Pool(mp.cpu_count())  # 使用 CPU 核心數量的進程池

    args_list = [(itemSet, itemSetSup, minConf, supportCache, detailed_result) for itemSet, itemSetSup in freqItemSet]
    results = pool.map(calculate_confidence, args_list)

    pool.close()
    pool.join()

    if detailed_result:
        rules = []
        for result in results:
            rules.extend(result)
        rules = (rules, len(rules))
    else:
        rules = sum(results)

    return rules

def caluculate_association_rule(freqItemSet, minConf, detailed_result=False):
    supportCache = {tuple(itemSet): support for itemSet, support in freqItemSet}
    if detailed_result:
        rules = defaultdict()
    else:
        rules = 0
    for itemSet, itemSetSup in freqItemSet:
        subsets = powerset(itemSet)
        for s in subsets:
            # there is %% in s
            def has_dpercent(s):
                for idx, x in enumerate(s):
                    if x.startswith('%') and x.endswith('%'):
                        return idx
            idx = has_dpercent(s)
            
            if idx is not None:
                rules[(s[idx],)] = (list((s[idx],)), 1.0)
                continue
            if len(s) > 0:
                try:
                    confidence = float(itemSetSup / supportCache.get(s, 0))
                    if confidence >= minConf:
                        if detailed_result:
                            temp = list(set(itemSet).difference(s))
                            idx = None
                            idx = has_dpercent(temp)
                            if idx is not None:
                                temp = (temp[idx],)
                                rules[s] =  (list(temp), confidence)
                        else:
                            rules += 1
                except:
                    continue
    if detailed_result:
        rules = (rules, len(rules))

    return rules