# Testing

EpicMan Server strives to ensure it has adequate testing to reasonably prevent
most issues hitting released code. This does not apply 100% unit test coverage
as a goal but having comprehensive coverage of areas of code that have been
identified as problematic.

Multiple testing techniques are used to uncover issues during development as
detailed below and more are constantly being added as time goes by.

# Tools Used
EpicServer limits itself to minimal 3rd party dependencies in both running,
deployment and testing and for the libraries that are chosen complexity in
usage and the solution itself are high on the list of metrics used for
selection. Due to this the testing framework consists of the following 3rd
party libraries:

* [pytest](https://pypi.org/project/pytest/)
* [fuzzing](https://pypi.org/project/fuzzing/)
* [flake8](https://pypi.org/project/flake8/)
* [mypy](https://pypi.org/project/mypy/)
* [pyright](https://pypi.org/project/pyright/)
* [bandit](https://pypi.org/project/bandit/)

The following are deprecated and in the process of being removed:

* [Tox](https://pypi.org/project/tox/)

Tox is currently slated for removal due to how frequently it would rebuild
environments, massively adding to testing overhead for local test suite runs
and the duplication of logic already encoded in the Makefile for building
virtual environments.

Refer to the [Makefile Documentation](/makefile/) for information on how to 
run the test suite.

# Unit Testing
Many parts of EpicMan Server are already tested via unit testing and focus on
a function at a time. This is not intended to provide complete coverage due
to the difficulties in testing some components (eg the main loop), With further
coverage for these cases coming from the extra classes of testing as detailed
below.

# Fuzzing
Fuzzing is done as part of several existing test suites to ensure that data
unaccounted for at the beginning of the design does not cause a crash of the
system. Fizzing is done at 3 different levels that correspond to areas where
the server may encounter arbitrary user provided input. These include:

* CLI arguments
* User Provided Application
* Network traffic

Of these 3 the last one presents the largest attack surface while the effects
of the other two are less critical (and normally provided by the user
themselves), The two in the safer category are fuzzed for both security and
ensuring better user feedback on errors.

# Bug and Security Testing
As bugs are found and classified test case that manifest these need to be
written up and placed in ```/tests/bugs``` with an ID corresponding to their
identity. This is intended to ensure that bugs do not reoccur later down the
line and ensure there is adequate information about the original issue.

We use [bandit](https://pypi.org/project/bandit/) for security auditing and 
publish these as part of the documentation. to run a manual check use the 
```make bandit``` command. See the [Security Reports](/bandit/) page for the 
summary of identified issues.

# Smoke Testing
Smoke testing exercises the entire pipeline by running small example apps that
perform tasks. These should behave like standard apps and ensure coverage of
the most commonly used parts of the code.

Smoke tests are also used as a way to explore new concepts in the stack from
both an expression (how an approach is written) and a technical front to help
keep feature development grounded in actual use cases.

# Examples Testing
All the Examples used are tested as part of the deployment pipeline. These
Tests are additionally used as [Smoke](#smoke-testing) as they are useful
for stressing the server end to end beyond just providing useful examples.

These are currently located in ```/tests/examples``` and ```/tests/smoke```.

# Type Checking
We are currently using [mypy](https://pypi.org/project/mypy/) and 
[pyright](https://pypi.org/project/pyright/) for type checking for as long as 
they do not come into conflict. So far it has proven useful to get 2 checks on 
the code base due to each having their own strength.

These can be invoked via ```make tests``` or via invoking ```make``` with the 
type checker you want as an argument.

Due to the large amount of dependencies these packages have they are installed 
into separate virtual environments to prevent these dependencies bleeding into 
development of EpicMan Server by accident.

# Static Analysis
We are currently looking into adding another type checker 
[pyre-check](https://pypi.org/project/pyre-check/) Due to its type checking 
and static analysis features. The Taint analysis can be useful in ensuring all 
incoming data from untrusted sources has been fully checked and cannot escape 
into other code without verification and sanitation.

if you have any experience in this area then feel free to reach out.
