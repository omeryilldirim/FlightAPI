from rest_framework import serializers
from .models import (
    Passenger,
    Flight,
    Reservation,
)

# -----------------------------------------------
# ---------------- FixSerializer ----------------
# -----------------------------------------------
class FixSerializer(serializers.ModelSerializer):
    
    created = serializers.StringRelatedField()
    created_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        validated_data['created_id'] = self.context['request'].user
        return super().create(validated_data)


# -----------------------------------------------
# -------------- Passenger Serializer -----------
# -----------------------------------------------
class PassengerSerializer(FixSerializer):

    gender_text = serializers.SerializerMethodField()

    class Meta:
        model = Passenger
        fields = '__all__'

    def get_gender_text(self, obj):
        return obj.get_gender_display()

# -----------------------------------------------
# --------------- Flight Serializer -------------
# -----------------------------------------------
class FlightSerializer(FixSerializer):

    departure_text = serializers.SerializerMethodField() # return from get_departure_text method
    arrival = serializers.SerializerMethodField() # return from get_arrival method 

    class Meta:
        model = Flight
        fields = ('id', 
                'flight_number', 
                'airline', 
                'departure', 
                'departure_text', 
                'departure_date', 
                'arrival', 
                'arrival_date', 
                'created', 
                'created_id', 
                'created_time', 
                'updated_time', 
                'get_airline_display' # dont need SerializerMethodField
        )

    def get_departure_text(self, obj):
        return obj.get_departure_display()
    
    def get_arrival(self, obj):
        return obj.get_arrival_display()

# -----------------------------------------------
# ----------- Reservation Serializer ------------
# -----------------------------------------------
class ReservationSerializer(FixSerializer):

    # flight = serializers.StringRelatedField() ## only __str__ data
    flight = FlightSerializer(read_only=True) ## complete data
    passenger = PassengerSerializer(many=True, read_only=True)

    flight_id = serializers.IntegerField(write_only=True)
    passenger_ids = serializers.ListField(write_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'

    def create(self, validated_data):
        validated_data["passenger"] = validated_data.pop('passenger_ids')
        return super().create(validated_data)
