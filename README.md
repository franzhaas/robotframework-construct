# robotframework-construct

## What is robotframework-construct?

[Robot Framework](https://robotframework.org) library powered by [construct](https://construct.readthedocs.io/en/latest/).

Declarative and symmetrical parser and builder for binary data.

Aiming for :rocket: speed, :white_check_mark: reliability and :microscope: visibility.

Ideally your binary data gets as accessible as numbers and strings are in robot-framework

### Use cases

 - Test your production construct specificatoin against a reference implementation of the same protocol
 - Test your production binary parser / generator against a construct implementation of your binary format.
 - Use your construct specification for your binary data 
   - to craft itentionally corrupted data
   - fuzz test your servers
 - Use your construct specification for your binary data to craft itentionally corrupted data
 - Beautifull and readable addon for accessing registers, both reading and writing.

## Relationships in the eco system

The number of dependancies is kept low there are no transient dependancies.

This is important as it is feasible to coordinate with just two projects. Construct is a well developed project which is not expected to massively changes soon. Robot-framework does make a major release every year, but these
are well managed and as relevant backwards incompatible changes are split between the API, the robotframework syntax, and the output files. There is an expectation that view incompatible changes will be affecting this project.

### construct (https://github.com/construct/construct)
All the parsing and generating capabilites come from construct. There is no code added to parsing/generating, The only thing added is code to interface construct to robot-framework. The way construct Construct objects are created remains unchainged.

Construct has no non optional dependancies.

### robot-framework (https://robotframework.org/)
This project interconnects construct with robot-framework. Only official api's are used but this project makes no sense without robot-framework

Robot-framework has no non optional dependcies.

### rammbock (https://github.com/MarketSquare/Rammbock)
Rammbock is an awesome project which was one of the reasons I personally started using robotframework in the first place.

Instead of working on rammbock the decission was made to integrate construct instead.

#### Reasoning
Rammbock and construct are both suffering on a shortage of engineering time. Construct is doing better than rammbock already and is catering to additional use cases which allows to cooperate with a larger pool of engineering time.

Construct is cooperating with kaitai touching additional comunities, like C#, Cpp etc..

Using construct allows to have a clear seperation between parsing/generating logic and interfacing
code.

## Limitations

In order to maintain reusability of the construct Constructs these need to be specified in python files. There are no plans to integrate the construct DSL into robotframework.

## Quality control measures

Examples and acceptance tests using robotframework are created. For the time being unit tests are not planned.

### Mutation testing
As this project consists only of interfacing code, it is important to catch user errors and create good error messages. Mutation testing forces to test all the code and to create all the error messages, suporting efforts to check that all possible problems yield helpfull error messages.
