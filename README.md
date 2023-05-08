# fedi-trivia
fedi trivia bot that may or may not work

uses cron currently to run, the following way:
- create_questions once every day
- parse once every 2 hours

there might be a third script coming, which would check for answers every minute, to reply whether they're correct or not (that way the "new correct answers" don't require actual pings). also, i should probably move the new question to the create_questions script.
