Earlier in this conversation I gave you this input:

> Smart lock firmware:
> 
> The lock unlocks when a registered phone is within 2 metres and the user taps the handle. It locks again automatically after 30 seconds if the door is closed. Low battery: warn the user at 20%. If the battery is flat the mechanical key still works.

You replied:

Q-001: From which point on the lock is the distance to the registered phone measured?

Q-002: Is a registered phone at exactly 2 metres from the lock within range?

Q-003: Which event starts the 30-second auto-lock period: the door unlocking, or the door closing?

Q-004: What does the smart lock firmware do when the 30 seconds end and the door is open?

Q-005: Which output does the smart lock firmware use to warn the user about low battery?

Q-006: At which battery level does the low-battery warning start: exactly 20%, or below 20%?

Q-007: Is the mechanical key requirement a behaviour of the smart lock firmware, or of another named system?

Q-008: What does the smart lock firmware do when the user taps the handle and no registered phone is within range?


My answers:

Q-001: from the Bluetooth antenna of the lock. Q-002: yes. Q-003: the door unlocking. Q-004: it waits, and locks when the door closes. Q-005: the LED on the lock blinks red, and the firmware sends a push notification to each registered phone. Q-006: at 20% or below; the warning is given once each time the level falls to 20%. Q-007: it is not a firmware behaviour; leave it out. Q-008: nothing; the lock stays locked.
