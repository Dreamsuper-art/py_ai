from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    # 任务状态
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = (
        (STATUS_PENDING, '待处理'),
        (STATUS_PROCESSING, '处理中'),
        (STATUS_COMPLETED, '已完成'),
        (STATUS_FAILED, '失败'),
    )
    
    # 任务类型
    TYPE_CHINESE_TO_ENGLISH = 'chinese_to_english'
    TYPE_ENGLISH_TO_CHINESE = 'english_to_chinese'
    TYPE_SUMMARIZE = 'summarize'
    TYPE_CHOICES = (
        (TYPE_CHINESE_TO_ENGLISH, '中文转英文'),
        (TYPE_ENGLISH_TO_CHINESE, '英文转中文'),
        (TYPE_SUMMARIZE, '文本总结'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    input_text = models.TextField()
    result = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.task_type} - {self.status} - {self.id}"