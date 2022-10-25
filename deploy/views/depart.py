from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from deploy import models
from deploy.utils.form import DepartModelForm
from deploy.utils.pagination import Pagination
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def depart_add(request):
    """ 添加部门 """
    if request.method == 'GET':
        # 用于获取数据库字段，并展示在页面上，因为我们的model_form中的fields = ['depart_name']，所以我们只展示部门名称这个字段
        form = DepartModelForm()
        # 将获取的字段展示到html页面上
        return render(request, 'depart_add.html', {'form': form})

    # 获取用户输入的部门信息(form表单)
    form = DepartModelForm(data=request.POST)
    # 打印用户输入的数据
    # print(form.data)
    if form.is_valid():
        # 打印校验合格的数据
        # print(form.cleaned_data)
        # 如果数据合法，则将获取到的数据全部保存到数据库中
        form.save()
        # return redirect('/depart/list/')
        return JsonResponse({"status": True})
        # return HttpResponse("添加成功")
    return JsonResponse({"status": False, 'error': form.errors})
    # return render(request, 'depart_add.html', {'form': form})
    # return HttpResponse("添加失败")


def depart_list(request):
    """ 部门列表 """
    # 从数据库中获取部门数据
    queryset = models.Department.objects.all()

    # 分页
    page_object = Pagination(request, queryset)
    form = DepartModelForm()

    context = {
        'form': form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    # 将部门数据返回给html页面进行展示
    return render(request, 'depart_list.html', context)


def depart_delete(request):
    """ 删除部门 """
    # 根据id获取页面上要删除的行信息
    uid = request.GET.get('uid')
    # 判断页面输入的行信息是否在数据库中存在
    exists = models.Department.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": "False", "error": "部门信息不存在"})
    models.Department.objects.filter(id=uid).delete()
    return JsonResponse({"status": "True"})


@csrf_exempt
def depart_edit(request):
    """ 编辑部门 """
    uid = request.GET.get('uid')
    row_obj = models.Department.objects.filter(id=uid).first()
    if not row_obj:
        return JsonResponse({"status": False, "error": "部门信息不存在"})
    form = DepartModelForm(data=request.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def depart_detail(request):
    """ 获取部门详细信息 用于编辑部门信息 """
    uid = request.GET.get('uid')
    row_dict = models.Department.objects.filter(id=uid).values('depart_name').first()
    if not row_dict:
        return JsonResponse({"status": False, "error": "部门信息不存在"})
    # 封装返回数据
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)
