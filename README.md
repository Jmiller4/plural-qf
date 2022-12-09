# plural-qf
Plural Quadratic Funding Mechanisms, written in python.

usage: `python pluralqf.py <mechanism> <groups> <contributions> <extra options>`

ex: `python pluralqf.py cocm "[[0, 1], [1, 2]]" "[10, 20, 0]"`

mechanisms are specified by the following keywords:
- `vcm` : vanilla cluster match
- `scm` : squared cluster match
- `cocm` : connection oriented cluster match
- `om` : offset match
- `pm` : pairwise matching

`<groups>` is a list of lists. each smaller list should contain the indices of the agents in that group.

`<contributions>` is a list. each element is the contribution of the agent at that index.

i.e. in the above example, agents 0 and 1 are in a group together, agents 1 and 2 are in another group together, agent 0 contributed 10, agent 1 contributed 20, and agent 2 contributed 0.

`<extra options>` is optional and only available for pairwise matching and offset match. For pairwise matching, enter an integer M. For offset match, enter True or False to preprocess with singleton groups or not.
