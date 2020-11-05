# from rest_framework import serializers
# from ner_dataset.models import TrainingSample


# class TrainingSampleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     input_data = serializers.CharField(required=True, allow_blank=False, max_length=2000)
#     golden_label = serializers.CharField(required=True, allow_blank=False, max_length=2000)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `TrainingData` instance, given the validated data.
#         """
#         return TrainingSample.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.input_data = validated_data.get('input_data', instance.input_data)
#         instance.golden_label = validated_data.get('golden_label', instance.golden_label)
#         instance.save()
#         return instance

# class TrainingSampleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TrainingSample
#         fields = ['id', 'input_data', 'golden_label']