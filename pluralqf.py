import math
from itertools import combinations as combinations
import numpy as np
import sys
import ast

def connection_oriented_cluster_match(groups, contributions):
    # groups: a 2d array. groups[i] is a list of people in group i (assume every person has an index).
    # contributions: an array. contributions[i] is the amount agent i contributed to a project.

    agents = list(range(len(contributions)))

    if any(contributions[i] < 0 for i in agents):
        raise NotImplementedError("negative contributions not supported")

    # memberships[i] is the number of groups agent i is in
    memberships = [len([g for g in groups if i in g]) for i in agents]

    # friend_matrix[i][j] is the number of groups that agent i and j are both in
    friend_matrix = [[len([g for g in groups if i in g and j in g])  for i in agents] for j in agents]

    # build up the funding amount. First, add in everyone's contributions
    funding_amount = sum(contributions)

    def K(i, h):
        if sum([friend_matrix[i][j] for j in h]) > 0:
            return math.sqrt(contributions[i])
        return contributions[i]

    funding_amount += sum(2 * math.sqrt(sum(K(i,p[1])/memberships[i] for i in p[0])) * math.sqrt(sum(K(j,p[0])/memberships[j] for j in p[1])) for p in combinations(groups, 2))
    
    return funding_amount


def vanilla_cluster_match(groups, contributions):
    # groups: a 2d array. groups[i] is a list of people in group i (assume every person has an index).
    # contributions: an array. contributions[i] is the amount agent i contributed to a project.

    agents = list(range(len(contributions)))

    if any(contributions[i] < 0 for i in agents):
        raise NotImplementedError("negative contributions not supported")

    # memberships[i] is the number of groups agent i is in
    memberships = [len([g for g in groups if i in g]) for i in agents]

    return math.pow(sum(math.sqrt(sum(contributions[i]/memberships[i] for i in g)) for g in groups), 2)


def squared_cluster_match(groups, contributions):
    # groups: a 2d array. groups[i] is a list of people in group i (assume every person has an index).
    # contributions: an array. contributions[i] is the amount agent i contributed to a project.

    agents = list(range(len(contributions)))

    if any(contributions[i] < 0 for i in agents):
        raise NotImplementedError("negative contributions not supported")

    # memberships[i] is the number of groups agent i is in
    memberships = [len([g for g in groups if i in g]) for i in agents]

    return math.pow(sum(math.sqrt(sum(contributions[i]/math.pow(memberships[i],2) for i in g)) for g in groups), 2)


def offset_match(groups, contributions, add_singletons = True):
    # groups: a 2d array. groups[i] is a list of people in group i (assume every person has an index).
    # contributions: an array. contributions[i] is the amount agent i contributed to a project.
    
    # add_singletons is a boolean. if set to true, then as a pre-processing step we will add each agent to a singleton group (if they are not in such a group already).
    # this is useful because it guarantees that we wind up with a solvable system of equations.
    
    agents = list(range(len(contributions)))

    if any(contributions[i] < 0 for i in agents):
        raise NotImplementedError("negative contributions not supported")

    # make sure everyone is in a singleton group, if we are instructed to do so:
    if add_singletons:
        for i in agents:
            if not any(len(g) == 1 and g[0] == i for g in groups):
                groups.append([i])

    T = [set(x for x in range(len(groups)) if i in groups[x]) for i in agents]

    s = [[len(T[i].intersection(T[j]))/len(T[i]) for i in agents] for j in agents]

    coeffs = [[s[i][j] for i in agents] for j in agents]

    v = [1] * len(agents)

    # this will throw a LinAlgError if the equation is unsolvable, which can happen if add_singletons is set to False

    alpha = np.linalg.solve(coeffs, v)

    return math.pow(sum(math.sqrt(alpha[i] * contributions[i]) for i in agents), 2)


def pairwise_matching(groups, contributions, M=100):
        
    agents = list(range(len(contributions)))

    if any(contributions[i] < 0 for i in agents):
        raise NotImplementedError("negative contributions not supported")
    
    k = [[M / (M + math.sqrt(contributions[i] * contributions[j])) for i in agents] for j in agents]

    return sum(contributions) + sum(k[p[0]][p[1]] * math.sqrt(contributions[p[0]] * contributions[p[1]]) for p in combinations(agents,2))


fn_dict = {'vcm' : vanilla_cluster_match, 'scm' : squared_cluster_match, 'cocm': connection_oriented_cluster_match, 'om': offset_match, 'pm': pairwise_matching}


def usage_info():
    # print out usage info
    print('\nusage: python pluralqf.py <mechanism> <groups> <contributions> <extra options>')
    print('\nex: python pluralqf.py cocm "[[0, 1], [1, 2]]" "[10, 20, 0]"')

    fn_keywords = {x: fn_dict[x].__name__ for x in fn_dict.keys()}

    print('\nmechanisms are specified by the following keywords: ')
    for x in fn_dict.keys():
        print('\t', x, ':', fn_keywords[x])
    print('\n<groups> is a list of lists. each smaller list should contain the indices of the agents in that group')
    print('\n<contributions> is a list. each element is the contribution of the agent at that index')
    print('\ni.e. in the above example, agents 0 and 1 are in a group together, agents 1 and 2 are in another group together, agent 0 contributed 10, agent 1 contributed 20, and agent 2 contributed 0.')
    print('\n<extra options> is optional and only available for pairwise matching and offset match. For pairwise matching, enter an integer M. For offset match, enter True or False to preprocess with singleton groups.')
    exit()

try:
    f = fn_dict[sys.argv[1]]
except KeyError:
    usage_info()

try:
    groups = ast.literal_eval(sys.argv[2])
    contributions = ast.literal_eval(sys.argv[3])
except IndexError:
    usage_info()
except ValueError:
    usage_info()

if len(sys.argv) == 5:

    if sys.argv[1] == 'om' and sys.argv[4] in ['True','False']:
        singleton = eval(sys.argv[4])       
        if singleton == False:
            print('\n\nWARNING: this might throw an error\n\n')
        print(offset_match(groups, contributions, add_singletons=singleton))
        exit()


    if sys.argv[1] == 'pm':
        M_val = int(sys.argv[4])
        print(pairwise_matching(groups, contributions, M=M_val))
        exit()

    usage_info()
    exit()

if len(sys.argv) > 5:
    usage_info()

print(fn_dict[sys.argv[1]](groups, contributions))
