from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from mediathread.assetmgr.serializers import AssetSerializer
from mediathread.djangosherd.models import SherdNote


class SherdNoteReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = SherdNote
        fields = ('id', 'asset', 'is_global_annotation',
                  'range1', 'range2', 'annotation_data')

    asset = AssetSerializer(read_only=True)

    def to_internal_value(self, data):
        if not isinstance(data, int):
            msg = 'Incorrect type. Expected an int, but got {}'.format(
                type(data))
            raise ValidationError(msg)

        try:
            return SherdNote.objects.get(id=data)
        except SherdNote.DoesNotExist:
            msg = 'No SherdNote instance found with id {}'.format(data)
            raise ValidationError(msg)


class SherdNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SherdNote
        fields = (
            'id', 'title', 'asset',
            'author', 'tags', 'body',
            'is_global_annotation',
            'range1', 'range2', 'annotation_data'
        )

    asset = AssetSerializer(read_only=True)

    def to_internal_value(self, data):
        title = data.get('title')
        body = data.get('body')
        author = data.get('author')
        range1 = data.get('range1')
        range2 = data.get('range2')
        annotation_data = data.get('annotation_data')
        asset = data.get('asset')

        # Perform the data validation.
        if not title:
            raise serializers.ValidationError({
                'title': 'This field is required.'
            })

        if not asset:
            raise serializers.ValidationError({
                'asset_id': 'This field is required.'
            })

        if not author:
            raise serializers.ValidationError({
                'author': 'This field is required.'
            })

        if not range1:
            raise serializers.ValidationError({
                'range1': 'This field is required.'
            })

        if not range2:
            raise serializers.ValidationError({
                'range2': 'This field is required.'
            })

        range1_fl = float(range1)
        range2_fl = float(range2)
        if (range2_fl <= range1_fl):
            raise serializers.ValidationError({
                'range2': 'range2 must be greater than range1.'
            })

        return {
            'title': title,
            'body': body,
            'author': author,
            'range1': range1_fl,
            'range2': range2_fl,
            'annotation_data': annotation_data,
            'asset': asset,
        }

    def create(self, validated_data):
        return SherdNote.objects.create(**validated_data)
