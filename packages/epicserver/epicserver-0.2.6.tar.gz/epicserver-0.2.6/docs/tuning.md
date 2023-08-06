## Tunning
kernel tunning to this effect. efforts have been made to select high performing
interfaces with an eye to keeping end to end latency down due to its 'chatty'
nature

Some kernel tunning can be applied and is detailed in the [TUNING] file in the
root of this repository, a word of caution or those researching this subject
online. Many guides associate 'performance' with 'messages/s' which may come
at the detriment of low latency tunning. in many cases the messaging rate of
this app will not push a system to its limits and as such this is a poor
metric to evaluate tuning on. tools are provided in the tools directory to
assist with benchmarking changes
