*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using dns as an example for both UDP and TCP.
Variables          dns_construct.py
Library            robotframework_construct
Test Tags          mutation_reflector
*** Test Cases ***
leave the reflector on
    Reflect traffic between ports using 'TCP'
