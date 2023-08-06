ConnectionError: use this for generic 'connction is broke' errors
* python does this nativly for nearly eerything
* we arugmetn a couple of special case in the IO loop for compatibility

use timeouts and let errors propergate up for retry logic to kick in

use @retry and specify the exceptions and set suppress=True
    avoid the default catch all

#
@remote_spawn
@retry
#
retry inside the remote spawn so tid does not change and is trackable, may not
work other way around (remote_spawn inside retry) due to how objects are passed
around (you cant remote spawn multiple times.


# singlton and _only_local
Singlton on a funciton ensures only one thread for this funciton call ever
exists at a time, futher calls will queue up???

singlton on a class ensures only one entity ever exists??

singleton on a class with _only_local allows multiple local copies of the same 
objext?
