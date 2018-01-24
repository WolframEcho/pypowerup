from magicbot import StateMachine, state
from components.lifter import Lifter
from components.intake import Intake
from automations.intake import Intake

class LifterAutomation(StateMachine):
    lifter: Lifter
    