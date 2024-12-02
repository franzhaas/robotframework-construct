*** Settings ***
Documentation        This is a simple example for a robot file using robotframework-construct demonstrating accessing real HW (a usb keyboard on linux)
Library              robotframework_construct
Library              Dialogs
Variables            hid_keyboard.py
Default Tags         hardware
Suite Setup          Open HID Files

*** Variables ***
${HID_FILE}           /dev/hidraw0

*** Test Cases ***
Demonstrate USB HID read/write using a USB keyboard as an example
    Log to console          ${\n}Press left alt and hold please
    ${LeftAltPressed}=      Parse '${IFILE}' using construct '${HIDReportIn}'
    Element 'modifiers.left_alt' in '${LeftAltPressed}' should be equal to '${True}'
    Log to console          ${\n}Press and hold right shift please
    ${LeftAltPressed}=      Parse '${IFILE}' using construct '${HIDReportIn}'
    Element 'modifiers.right_shift' in '${LeftAltPressed}' should be equal to '${True}'
    Write binary data generated from '${HIDReportOutEmpty}' using construct '${HIDReportOut}' to '${OFILE}'
    Log To Console          ${\n}The three leds should be off now
    Sleep     1
    Modify the element located at 'modifiers.SCROLL_LOCK' of '${HIDReportOutEmpty}' to '${True}'
    Write binary data generated from '${HIDReportOutEmpty}' using construct '${HIDReportOut}' to '${OFILE}'
    Log To Console          ${\n}The scroll lock led should be on now
    Sleep                   time_=1
    Modify the element located at 'modifiers.SCROLL_LOCK' of '${HIDReportOutEmpty}' to '${False}'
    Modify the element located at 'modifiers.CAPS_LOCK' of '${HIDReportOutEmpty}' to '${True}'
    Write binary data generated from '${HIDReportOutEmpty}' using construct '${HIDReportOut}' to '${OFILE}'
    Call Method             ${OFILE}   flush
    Log To Console          ${\n}The caps lock led should be on now

*** Keywords ***
Open HID Files
    ${IFILE}=               Open '${HID_FILE}' for reading binary data with buffering disabled
    ${OFILE}=               Open '${HID_FILE}' for writing binary data
