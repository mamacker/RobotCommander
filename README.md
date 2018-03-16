<img height="200px" style="position:relative" src="https://d2z4f545rh9t62.cloudfront.net/robotcommander-alexa.png">

# RobotCommander
Simple wrappers on the RobotCommander.io json interface.  Install the skill from [here](https://www.amazon.com/dp/B07BCQH5J7/).

See the board here: https://RobotCommander.io

<img src="https://raw.githubusercontent.com/mamacker/RobotCommander/master/board.png" height="300"> <img src="https://raw.githubusercontent.com/mamacker/RobotCommander/master/robotcommanderhardware.jpg" height="300">

# RobotCommander.IO Skill
This is meant to be used with the "Robot Commander" Alexa Skill and a [Raspberry PI Sense Hat](https://www.raspberrypi.org/products/sense-hat/)

## The Skill:
https://www.amazon.com/dp/B07BCQH5J7/

To get started, try the Robot Commander Skill, then, get your Robot Commander ID by saying:
> "Alexa, ask Robot Commander for my ID"

or

If you are already in Robot Commander say:

> "What is my Commander ID"

Alexa will respond with a 6 character code.  Put that code in the ID slot of the source, and watch your robot's progress in real-time-IOT.

# Things you can say...
Once installed, tell your robot to go forward, left or right. The little blue dot will move with your commands.

# To start the script...
Edit: ./sense-hat/robotio-sense.py

Change the line:
>  ROBOT_COMMANDER_ID = 'qmda82'

Where <b>qmda82</b> is my ID, put yours in there.

The run the script:
> nohup python ./sense-hat/robotio-sense.py
