Earlier in this conversation I gave you this input:

> Reminder emails for appointments (clinic booking service). Patients get a reminder 24h before their appointment and another 2h before. Don't send reminders for cancelled appointments. Patients can opt out of reminders. If the appointment was booked less than 24h ahead, skip the first reminder.

You replied:

FR-001: While an appointment has not been cancelled and the patient has not opted out of reminders and the appointment was booked at least 24 hours before the appointment start time, when the time reaches 24 hours before the appointment start time, the clinic booking service shall send a reminder email to the patient.

FR-002: While an appointment has not been cancelled and the patient has not opted out of reminders, when the time reaches 2 hours before the appointment start time, the clinic booking service shall send a reminder email to the patient.

Q-001: What must a reminder email contain (subject, body text, and appointment details)?

Q-002: How does a patient opt out of reminders?

Q-003: Does an opt-out cover both reminders and all appointments of that patient?

Q-004: What does the clinic booking service do when an appointment is booked less than 2 hours before its start time?

Q-005: What does the clinic booking service do when a reminder email fails to send or bounces?

Q-006: What happens to the reminders when an appointment is rescheduled to a new start time?

Q-007: Can a patient opt back in, and if so, does the clinic booking service send the reminders that are still due?


My answers:

Q-001: subject "Appointment reminder"; the body gives the appointment date, the start time, and the clinic name. Q-002: with an "Unsubscribe from reminders" link in each reminder email. Q-003: yes, both reminders and all appointments. Q-004: it sends no reminder. Q-005: it logs the failure and does not retry. Q-006: the reminders follow the new start time, and a reminder that was already sent is sent again for the new time. Q-007: yes, on the profile page; only reminders that are not yet due are sent.
