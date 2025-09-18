from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import FunctionExecuteSerializer
from .models import Task
from .tasks import process_translation_or_summary

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_functions(request):
    """获取所有功能列表"""
    functions = [
        {"id": "chinese_to_english", "name": "中文转英文", "description": "将中文文本翻译成英文"},
        {"id": "english_to_chinese", "name": "英文转中文", "description": "将英文文本翻译成中文"},
        {"id": "summarize", "name": "文本总结", "description": "对长文本进行摘要总结"}
    ]
    
    return Response({"functions": functions})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def execute_function(request):
    """提交异步任务"""
    serializer = FunctionExecuteSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    function_type = data['function_type']
    text = data['text']
    
    # 创建任务记录
    task = Task.objects.create(
        user=request.user,
        task_type=function_type,
        input_text=text,
        status=Task.STATUS_PENDING
    )
    
    # 异步提交任务到Celery
    process_translation_or_summary.delay(task.id)
    
    # 返回任务ID，供客户端轮询使用
    return Response({
        "task_id": str(task.id),
        "status": "pending",
        "message": "任务已提交，请轮询获取结果"
    }, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_status(request, task_id):
    """查询任务状态和结果"""
    try:
        # 确保用户只能查询自己的任务
        task = Task.objects.get(id=task_id, user=request.user)
        
        # 构建响应数据
        response_data = {
            "task_id": str(task.id),
            "status": task.status,
            "task_type": task.task_type,
            "created_at": task.created_at,
            "updated_at": task.updated_at
        }
        
        # 如果任务已完成，包含结果
        if task.status == Task.STATUS_COMPLETED:
            response_data["result"] = task.result
        # 如果任务失败，包含错误信息
        elif task.status == Task.STATUS_FAILED:
            response_data["error"] = task.result
        
        return Response(response_data)
        
    except Task.DoesNotExist:
        return Response(
            {"error": "任务不存在或您无权访问此任务"},
            status=status.HTTP_404_NOT_FOUND
        )
