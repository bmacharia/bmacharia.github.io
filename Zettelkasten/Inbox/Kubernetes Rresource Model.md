



Off on a tangent here. I will be talking about _Level-triggered_ and _edge-triggered_


## Edge Triggered

edge triggered things happen when some stimulus change

level triggered things happen when some stimulus crossed a threshold

It is clear to me that we are talking about `stimuli`


Edge triggered is about a change caused buy some stimulus

level triggered things happen when the said  stimulus crosses some level/threshold


So what does all this triggering have to do with software


Simple programs are level triggered, they are dependent on inputs, and for the most part those inputs do not change, during the execution of the program

In kubernetes controllers are level based triggered


In kubernetes the most important signals are desired state and actual state.


Kubernetes is a level triggered system, level triggered systems react tot he state of the system, the state of the system is being monitored continuously
