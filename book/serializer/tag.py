from rest_framework import serializers


class TagSerializer(serializers.Serializer):
    """Helper serializer for the Tag field of the Book document."""

    title = serializers.CharField()

    class Meta:
        """Meta options."""

        fields = ('title',)
        read_only_fields = ('title',)
