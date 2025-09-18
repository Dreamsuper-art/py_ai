from celery import shared_task
import time
from .models import Task

@shared_task
def process_translation_or_summary(task_id):
    try:
        # 获取任务对象
        task = Task.objects.get(id=task_id)
        
        # 更新任务状态为处理中
        task.status = Task.STATUS_PROCESSING
        task.save()
        
        # 模拟AI处理过程（实际项目中这里会调用真实的AI服务）
        # 添加一些延迟来模拟处理时间
        time.sleep(3)
        
        # 根据任务类型执行相应的操作
        if task.task_type == Task.TYPE_CHINESE_TO_ENGLISH:
            result = f"Translation to English: {task.input_text}"
        elif task.task_type == Task.TYPE_ENGLISH_TO_CHINESE:
            result = f"翻译成中文: {task.input_text}"
        elif task.task_type == Task.TYPE_SUMMARIZE:
            result = f"文本总结: {task.input_text[:50]}..."
        
        # 更新任务结果和状态
        task.result = result
        task.status = Task.STATUS_COMPLETED
        task.save()
        
    except Exception as e:
        # 发生错误时更新任务状态为失败
        task.status = Task.STATUS_FAILED
        task.result = f"处理失败: {str(e)}"
        task.save()