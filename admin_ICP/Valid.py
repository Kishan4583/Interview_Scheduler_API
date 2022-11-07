import datetime
import pytz
from .models import Interview_Info


class validators:
    def __init__(self, startTime, endTime, participants):
        self.startTime = startTime
        self.endTime = endTime
        self.participants = participants
        self.valid = True
        self.errorMessage = ""
        self.leastParticipantsAllowed = 2

    def isvalid(self):
        return self.valid

    def setvalid(self, value):
        self.valid = value

    def getErrorMessage(self):
        return self.errorMessage

    def appendErrorMessage(self, message):
        if self.errorMessage == "":
            self.errorMessage = message
        else:
            self.errorMessage = self.errorMessage + ', ' + message

    def validateOverlappings(self, oldDataId=-1):
        # checking overlapping inerviews
        for user in self.participants:
            scheduledInterviews = Interview_Info.objects.filter(
                participants=user)
            for interview in scheduledInterviews:
                if oldDataId != interview.id and self.checkOverlapping(interview) == False:
                    self.setvalid(False)
                    self.appendErrorMessage(
                        "User with userId = "+str(user.id)+" has overlapping Interviews")

    def checkOverlapping(self, slot):
        # checking overlaps
        if slot.startTime >= self.endTime or slot.endTime <= self.startTime:
            return True
        else:
            return False

    def validateCountofParticipants(self):
        # checking if there are less than 2 participants
        if len(self.participants) < self.leastParticipantsAllowed:
            self.setvalid(False)
            self.appendErrorMessage("There must be at least 2 users")

    def validateTime(self):
        # checks if the time mentioned is correct or not
        if self.startTime > self.endTime:
            self.setvalid(False)
            self.appendErrorMessage("Start Time can't be > End Time")

        # checks if interview is scheduled in the past time
        currentTime = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        if self.startTime < currentTime or self.endTime < currentTime:
            self.setvalid(False)
            self.appendErrorMessage(
                "Interviews in the past can't be scheduled")