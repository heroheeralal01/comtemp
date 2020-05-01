# Temporal network community detection
Community detection in temporal networks using multi-layer technique

In this method the temporal graph is divied into layers according to their time stamps.
The timeline is divided into time steps that form a network layer of a period of time.


Since a node can be a member of communities of other time-step layers than the time-step which is assigned to it, to solve this a edge's existance in one layer is partially transfered to the layer of previous time-step (if it exists) and to the layer of next time-step (if it exists). 