from rest_framework import serializers

class FunctionExecuteSerializer(serializers.Serializer):
    function_type = serializers.ChoiceField(choices=[
        ('chinese_to_english', '中文转英文'),
        ('english_to_chinese', '英文转中文'),
        ('summarize', '文本总结')
    ])
    text = serializers.CharField()
