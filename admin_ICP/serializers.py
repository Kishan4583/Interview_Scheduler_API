from .models import User_Info, Interview_Info
from rest_framework import serializers
from .Valid import validators


class InterviewDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview_Info
        fields = "__all__"

    def validate(self, attrs):
        self.startTimeData = attrs["startTime"]
        self.endTTimeData = attrs["endTime"]
        self.participantsData = attrs["participants"]

        validateObj = validators(
            self.startTimeData, self.endTTimeData, self.participantsData)
        validateObj.validateTime()
        validateObj.validateCountofParticipants()

        if validateObj.isvalid() == False:
            raise serializers.ValidationError(validateObj.getErrorMessage())

        return attrs

    def checkCreateoverlapping(self):
        validateObj = validators(
            self.startTimeData, self.endTTimeData, self.participantsData)
        validateObj.validateOverlappings()

        if validateObj.isvalid() == False:
            raise serializers.ValidationError(validateObj.getErrorMessage())
        return True

    def checkUpdateoverlappings(self, oldDataid):
        validateObj = validators(
            self.startTimeData, self.endTTimeData, self.participantsData)
        validateObj.validateOverlappings(oldDataid)

        if validateObj.isvalid() == False:
            raise serializers.ValidationError(validateObj.getErrorMessage())
        return True


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Info
        fields = "__all__"

    def validate(self, attrs):
        return attrs