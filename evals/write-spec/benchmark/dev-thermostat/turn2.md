Earlier in this conversation I gave you this input:

> Requirements for the thermostat controller: when the room temperature falls 0.5 °C below the setpoint, the thermostat controller switches the heating relay on. When the room temperature reaches the setpoint, it switches the heating relay off. While the window sensor reports an open window, the heating relay stays off. The user sets the setpoint with the dial, between 5 and 30 °C.

You replied:

FR-001: When the room temperature falls 0.5 °C below the setpoint, the thermostat controller shall switch the heating relay on.

FR-002: When the room temperature reaches the setpoint, the thermostat controller shall switch the heating relay off.

FR-003: While the window sensor reports an open window, the thermostat controller shall keep the heating relay off.

Q-001: Are 5 °C and 30 °C themselves valid setpoints?

Q-002: When the window sensor stops reporting an open window and the room temperature is 0.5 °C or more below the setpoint, does the thermostat controller switch the heating relay on at that moment?

Q-003: When the user sets a value with the dial, does the thermostat controller use that value as the setpoint at the moment the user sets it?

Q-004: What does the thermostat controller do when the dial gives a value outside the range of 5 to 30 °C?


My answers:

Q-001: yes, both are valid. Q-002: yes. Q-003: yes. Q-004: the dial cannot give a value outside that range.
