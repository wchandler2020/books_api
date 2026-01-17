from rest_framework import serializers
from datetime import datetime
from typing import List, Optional

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    author = serializers.CharField()
    year = serializers.IntegerField()
    tags = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )

    def validate_year(self, value):
        current_year = datetime.now().year
        if value < 1400 or value > current_year:
            raise serializers.ValidationError(f'Years should be between 1400 and {current_year}')
        return value


