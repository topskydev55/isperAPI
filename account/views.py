#!/usr/bin/python
# -*- coding=utf-8 -*-

import json
import logging

import xlrd
import xlwt

from course.models import CourseClassStudent, CourseClass
from django.db.models import Q
from django.shortcuts import redirect
from django.utils.http import urlquote

from account.service import user_info
from django.contrib import auth
from django.http import HttpResponse
from account.models import Tuser, TCompany, TClass
from experiment.models import Experiment
from team.models import TeamMember
from utils import code, const, query, easemob, tools
from utils.request_auth import auth_check
from django.contrib.sessions.models import Session
from django.utils import timezone

logger = logging.getLogger(__name__)


# 用户名查询
def api_account_query(request):
    try:
        username = request.GET.get("username", None)  # 用户名

        user = Tuser.objects.filter(username=username, del_flag=0).first()
        if user:
            # 用户所属的类型列表
            resp = code.get_msg(code.SUCCESS)
            resp['d'] = {'is_director': user.director, 'is_manage': user.manage, 'is_admin': user.is_admin}

        else:
            resp = code.get_msg(code.USER_NOT_EXIST)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_query Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 用户列表
def api_account_users(request):
    resp = auth_check(request, "GET")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        search = request.GET.get("search", None)  # 搜索关键字
        course_id = request.GET.get("course_id", None)  # 课堂id
        user_type = request.GET.get("type", 1)  # 用户类型
        page = int(request.GET.get("page", 1))  # 页码
        size = int(request.GET.get("size", const.ROW_SIZE))  # 页面条数

        sql = '''SELECT t.id,t.`name`,t.username,t.nickname,t.type,t.qq,t.gender,c.`name` class_name
        from t_user t LEFT JOIN t_class c ON t.tclass_id=c.id'''
        count_sql = '''SELECT count(1) from t_user t LEFT JOIN t_class c ON t.tclass_id=c.id'''
        where_sql = ' WHERE t.del_flag=0 and t.is_active=1 and t.is_superuser=0'

        if search:
            where_sql += ' and (t.`name` like \'%' + search + '%\' or t.username like \'%' + search + \
                         '%\' or c.`name` like \'%' + search + '%\')'

        # 三期 - 如果存在课堂id，则根据课堂删选用户
        if course_id:
            inner_join_sql = ''' inner join ( select distinct course_class_id, student_id 
            from t_course_class_student ) r on t.id = r.student_id'''
            sql += inner_join_sql
            count_sql += inner_join_sql
            where_sql += ' and r.course_class_id = ' + course_id
            pass

        # if user_type:
        #     where_sql += ' and t.type=%s ' % user_type
        sql += where_sql
        count_sql += where_sql
        sql += ' order by username'
        logger.info(sql)
        data = query.pagination_page(sql, ['id', 'name', 'username', 'nickname', 'type', 'qq', 'gender', 'class_name'],
                                     count_sql, int(page), int(size))
        resp = code.get_msg(code.SUCCESS)
        resp['d'] = data
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_users Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 用户退出
def api_account_logout(request):
    resp = auth_check(request, "POST")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        auth.logout(request)
        resp = code.get_msg(code.SUCCESS)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_logout Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


def logout_all(user):
    session_obj_list = Session.objects.filter(expire_date__gt=timezone.now())
    for session_obj in session_obj_list:
        user_id = session_obj.get_decoded().get("_auth_user_id")
        # logger.info(type(user_id))
        if user_id:
            if int(user_id) == user.pk:
                session_obj.delete()


# 用户登录
def api_account_login(request):
    try:
        username = request.POST.get("username", None)  # 用户名
        password = request.POST.get("password", None)  # 密码
        login_type = int(request.POST.get("login_type", 1))  # 登录身份

        # 参数验证
        if username is None or password is None:
            resp = code.get_msg(code.PARAMETER_ERROR)
        else:
            user_temp = Tuser.objects.filter(username=username, del_flag=0).first()
            if not user_temp:
                resp = code.get_msg(code.USER_NOT_EXIST)
                return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

            user = auth.authenticate(username=username, password=password)
            if user:
                # todo 登出相同账号其它登录用户
                logout_all(user)
                if login_type == 1 or (login_type == 2 and user.director) or (login_type == 3 and user.manage) or (
                        login_type == 4 and user.is_admin):
                    auth.login(request, user)
                    # 三期 保存用户的登录类型， 后面有用, 无力吐槽
                    request.session['login_type'] = login_type
                    resp = code.get_msg(code.SUCCESS)
                    resp['d'] = user_info(user.id)
                    resp['d']['identity'] = login_type
                    resp['d']['manage'] = user.manage
                    resp['d']['admin'] = user.is_admin
                    resp['d']['company_id'] = user.tcompany.id if user.tcompany else ''
                    resp['d']['company_name'] = user.tcompany.name if user.tcompany else ''
                    resp['d']['director'] = user.director
                    resp['d']['last_experiment_id'] = user.last_experiment_id
                    if user.last_experiment_id:
                        last_exp = Experiment.objects.get(pk=user.last_experiment_id)
                    else:
                        last_exp = Experiment()
                    resp['d']['last_experiment_status'] = last_exp.status
                    resp['d']['last_experiment_name'] = last_exp.name
                else:
                    resp = code.get_msg(code.PERMISSION_DENIED)
            else:
                resp = code.get_msg(code.USERNAME_OR_PASSWORD_ERROR)

        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_login Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 用户列表-三期
def api_account_users_v3(request):
    resp = auth_check(request, "GET")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        search = request.GET.get("search", None)  # 搜索关键字
        identity = request.GET.get("identity", 1)  # 管理员类型，实验人员类型类型
        page = int(request.GET.get("page", 1))  # 页码
        size = int(request.GET.get("size", const.ROW_SIZE))  # 页面条数
        user = request.user

        sql = '''SELECT t.id,t.username,t.name,c.name class_name,d.name company_name,t.gender,t.qq,t.nickname,t.phone,t.email,
                    t.director,t.manage,e.name assigned_by, t.is_share
                    from t_user t 
                    LEFT JOIN t_class c ON t.tclass_id=c.id
                    LEFT JOIN t_company d ON t.tcompany_id=d.id
                    LEFT JOIN t_user e on t.assigned_by = e.id'''
        count_sql = '''SELECT count(1) from t_user t 
                    LEFT JOIN t_class c ON t.tclass_id=c.id
                    LEFT JOIN t_company d ON t.tcompany_id=d.id
                    LEFT JOIN t_user e on t.assigned_by = e.id'''
        where_sql = ' WHERE t.del_flag=0 and t.is_active=1 '  # and t.is_superuser=0'

        if search:
            where_sql += ' and (t.`name` like \'%' + search + '%\' or t.username like \'%' + search + '%\')'

        if identity:
            where_sql += ' and t.identity=%s ' % identity

        # if not user.is_admin:
        #     where_sql += ' and t.tcompany_id=%s ' % user.tcompany_id

        # 三期 - 加上是否共享字段 并且 只显示本单位数据或者共享数据
        if request.session['login_type'] != 4:
            where_sql += ' and (t.tcompany_id = ' + str(user.tcompany_id) + ' or t.is_share = 1)'

        sql += where_sql
        count_sql += where_sql
        sql += ' order by t.update_time desc'
        logger.info(sql)
        data = query.pagination_page(sql, ['id', 'username', 'name', 'class_name', 'company_name', 'gender', 'qq',
                                           'nickname', 'phone', 'email', 'director', 'manage', 'assigned_by', 'is_share'],
                                     count_sql, int(page), int(size))
        resp = code.get_msg(code.SUCCESS)
        resp['d'] = data
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_users Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 查询单位列表
def api_account_companys(request):
    resp = auth_check(request, "GET")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        companys = TCompany.objects.all().order_by("-update_time")
        data = [{'id': i.id, 'name': i.name} for i in companys]
        resp = code.get_msg(code.SUCCESS)
        resp['d'] = data
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_companys Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 查询班级列表
def api_account_classes(request):
    resp = auth_check(request, "GET")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        classes = TClass.objects.all().order_by("-update_time")
        data = [{'id': i.id, 'name': i.name} for i in classes]
        resp = code.get_msg(code.SUCCESS)
        resp['d'] = data
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_classes Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 用户更新
def api_account_user_update(request):
    resp = auth_check(request, "POST")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        user_id = request.POST.get('id', None)  # 账号
        username = request.POST.get('username', None)  # 账号
        password = request.POST.get('password', None)  # 密码
        nickname = request.POST.get('nickname', None)  # 昵称
        gender = request.POST.get('gender', None)  # 性别
        name = request.POST.get('name', None)  # 姓名
        email = request.POST.get('email', None)  # 邮箱
        phone = request.POST.get('phone', None)  # 联系方式
        qq = request.POST.get('qq', None)  # qq
        identity = request.POST.get('identity', None)  # 身份
        type = request.POST.get('type', None)  # 类型
        class_id = request.POST.get('class_id', None)  # 班级id
        company_id = request.POST.get('company_id', None)  # 所在单位
        director = request.POST.get('director', None)  # 是否具有指导权限
        manage = request.POST.get('manage', None)  # 是否具有管理权限

        user = Tuser.objects.get(pk=user_id)
        user.assigned_by = request.user.id
        if username:
            user.username = username
        if password:
            user.set_password(password)
        if nickname:
            user.nickname = nickname
        if gender:
            user.gender = gender
        if name:
            user.name = name
        if email:
            user.email = email
        if phone:
            user.phone = phone
        if qq:
            user.qq = qq
        if identity:
            user.identity = identity
        if type:
            user.type = type
        if class_id:
            user.tclass_id = class_id
        if company_id:
            user.tcompany_id = company_id
        if director and 'TRUE' == director.upper():
            user.director = True
        else:
            user.director = False
        if manage and 'TRUE' == manage.upper():
            user.manage = True
        else:
            user.manage = False

        user.save()

        resp = code.get_msg(code.SUCCESS)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_logout Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 用户保存
def api_account_user_save(request):
    resp = auth_check(request, "POST")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        username = request.POST.get('username', None)  # 账号
        password = request.POST.get('password', None)  # 密码
        nickname = request.POST.get('nickname', None)  # 昵称
        gender = request.POST.get('gender', None)  # 性别
        name = request.POST.get('name', None)  # 姓名
        email = request.POST.get('email', None)  # 邮箱
        phone = request.POST.get('phone', None)  # 联系方式
        qq = request.POST.get('qq', None)  # qq
        identity = request.POST.get('identity', None)  # 身份
        type = request.POST.get('type', None)  # 类型
        class_id = request.POST.get('class_id', None)  # 班级
        company_id = request.POST.get('company_id', None)  # 所在单位
        director = request.POST.get('director', None)  # 是否具有指导权限
        manage = request.POST.get('manage', None)  # 是否具有管理权限

        users = Tuser.objects.filter(username=username, del_flag=0)
        user = Tuser()
        if users:  # 如果用户时系统中有的， 恢复正常然后更新, md, 这都是什么鬼
            resp = code.get_msg(code.SYSTEM_ERROR)
            resp['m'] = '账户已存在'
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
        else:
            users = Tuser.objects.filter(username=username)
            if users:  # 如果用户时系统中有的， 恢复正常然后更新, md, 这都是什么鬼
                user = users.first()
                user.del_flag = 0
        user.assigned_by = request.user.id
        user.is_active = 1
        if username:
            user.username = username
            # u = Tuser.objects.filter(username=username, del_flag=0)
            # if u:
            #     resp = code.get_msg(code.USER_EXIST)
            #     return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
        if password:
            user.set_password(password)
        if nickname:
            user.nickname = nickname
        if gender:
            user.gender = gender
        if name:
            user.name = name
        if email:
            user.email = email
        if phone:
            user.phone = phone
        if qq:
            user.qq = qq
        if identity:
            user.identity = identity
        if type:
            user.type = type
        if class_id:
            user.tclass_id = class_id
        if company_id:
            user.tcompany_id = company_id
        if director and 'TRUE' == director.upper():
            user.director = True
        else:
            user.director = False
        if manage and 'TRUE' == manage.upper():
            user.manage = True
        else:
            user.manage = False

        user.save()
        easemob_success, easemob_result = easemob.register_new_user(user.pk, easemob.EASEMOB_PASSWORD)

        resp = code.get_msg(code.SUCCESS)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_logout Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 根据id查询用户信息
def api_account_get_user(request):
    resp = auth_check(request, "GET")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        user_id = request.GET.get('id', None)
        user = Tuser.objects.get(id=user_id)
        assigned_by = None
        if user.assigned_by:
            assigned_by = Tuser.objects.get(id=user.assigned_by)
        data = {'id': user.id, 'username': user.username, 'nickname': user.nickname, 'gender': user.gender,
                'name': user.name, 'email': user.email, 'phone': user.phone, 'qq': user.qq,
                'identity': user.identity, 'type': user.type, 'ip': user.ip, 'is_active': user.is_active,
                'is_admin': user.is_admin, 'class_id': user.tclass.id if user.tclass else '',
                'company_id': user.tcompany.id if user.tcompany else '',
                'director': user.director,
                'manage': user.manage, 'assigned_by': assigned_by.name if assigned_by else '', }

        resp = code.get_msg(code.SUCCESS)
        resp['d'] = data
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_logout Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 导入用户列表
def api_account_import(request):
    resp = auth_check(request, "POST")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        identity = int(request.POST.get("identity", 1))  # 管理员类型，实验人员类型类型
        logger.info('----------------------')
        logger.info(identity)
        upload_file = request.FILES.get("file", None)  # 文件

        if identity is None or upload_file is None:
            resp = code.get_msg(code.PARAMETER_ERROR)
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

        # 解析exl内容，生成docx文件，保存数据库。
        wb = xlrd.open_workbook(filename=None, file_contents=upload_file.read())
        sheet = wb.sheet_by_index(0)

        # 返回的excel
        report = xlwt.Workbook(encoding='utf8')
        sheet_ret = report.add_sheet(u'sheet1')
        logger.info('name:%s,rows:%s,cols:%s' % (sheet.name, sheet.nrows, sheet.ncols))
        if identity == 1:  # 实验人员
            # 返回的excel的表头
            sheet_ret.write(0, 0, 'ID')
            sheet_ret.write(0, 1, '姓名')
            sheet_ret.write(0, 2, '班级')
            sheet_ret.write(0, 3, '所在单位')
            sheet_ret.write(0, 4, '性别')
            sheet_ret.write(0, 5, '指导权限')
            sheet_ret.write(0, 6, '管理权限')
            sheet_ret.write(0, 7, '权限分配责任人')
            sheet_ret.write(0, 8, '导入状态')
            sheet_ret.write(0, 9, '反馈信息')
            # u'ID', u'姓名', u'班级', u'所在单位', u'性别', u'指导权限', u'管理权限', u'权限分配责任人'
            # 读取excel每一行的数据
            for i in range(1, sheet.nrows):
                user = Tuser()  # 构造用户对象
                user.identity = identity
                user.set_password(const.PASSWORD_DEFAULT)
                user.is_active = 1
                flag = True  # 保存是否成功标志
                msg = []  # 错误信息

                # 获取excel数据行
                c0 = sheet.cell(i, 0).value
                if isinstance(c0, float):
                    c0 = int(c0)
                c1 = sheet.cell(i, 1).value
                c2 = sheet.cell(i, 2).value
                c3 = sheet.cell(i, 3).value
                c4 = sheet.cell(i, 4).value
                c5 = sheet.cell(i, 5).value
                c6 = sheet.cell(i, 6).value
                c7 = sheet.cell(i, 7).value

                # 返回excel数据行
                sheet_ret.write(i, 0, c0)
                sheet_ret.write(i, 1, c1)
                sheet_ret.write(i, 2, c2)
                # sheet_ret.write(i, 3, c3)
                sheet_ret.write(i, 4, c4)
                # sheet_ret.write(i, 5, c5)
                # sheet_ret.write(i, 6, c6)
                # sheet_ret.write(i, 7, request.user.name)

                if None in (c0, ):
                    flag = False
                    msg.append("错误：账号列1不允许为空")
                else:

                    # 检查账号是否为数字
                    if isinstance(c0, float):
                        c0 = int(c0)

                    # 检查账号是否存在
                    users = Tuser.objects.filter(username=c0, del_flag=0)
                    if users:
                        flag = False
                        msg.append('错误：(账户)已存在，（列1)')
                    else:
                        users = Tuser.objects.filter(username=c0)
                        if users:  # 如果用户时系统中有的， 恢复正常然后更新, md, 这都是什么鬼
                            user = users.first()
                            user.del_flag = 0
                            user.identity = identity
                        user.username = c0
                    if None in (c1, ):
                        flag = False
                        msg.append('错误：姓名列2不允许为空')
                    elif isinstance(c1, float):
                        flag = False
                        msg.append('错误：姓名列2不允许为数字(认真点好吗？谁家的名字是数字的)')
                    else:
                        # 姓名
                        user.name = c1

                    # 根据班级名称设置班级
                    tclass = TClass.objects.filter(name=c2)
                    if tclass:
                        user.tclass = tclass.first()
                    else:
                        # msg.append('警告：(班级)有误，（列3)')
                        pass

                    # 设置单位
                    # tcompany = TCompany.objects.filter(name=c3)
                    # if tcompany:
                    #     user.tcompany = tcompany.first()
                    # else:
                    #     msg.append('警告：(单位)有误，（列4)')
                    user.tcompany_id = request.user.tcompany_id
                    sheet_ret.write(i, 3, request.user.tcompany.name if request.user.tcompany else '')

                    # 设置性别
                    user.gender = 1 if '男' == c4 else 2
                    # 指导权限
                    # user.director = True if '是' == c5 else False
                    user.director = False
                    sheet_ret.write(i, 5, '否')
                    # 管理权限
                    # user.manage = True if '是' == c6 else False
                    user.manage = False
                    sheet_ret.write(i, 6, '否')

                    # 权限分配责任人
                    # assigned_by = Tuser.objects.filter(name=c7)
                    # if assigned_by:
                    #     user.assigned_by = assigned_by.first().id
                    # else:
                    #     msg.append('警告：(权限分配责任人)有误，（列8)')
                    user.assigned_by = request.user.id
                    sheet_ret.write(i, 7, request.user.name)

                # 保存用户并写入成功失败的状态和原因
                if flag:
                    user.save()
                    easemob_success, easemob_result = easemob.register_new_user(user.pk, easemob.EASEMOB_PASSWORD)
                    sheet_ret.write(i, 8, '成功')
                else:
                    sheet_ret.write(i, 8, '失败')
                sheet_ret.write(i, 9, '；'.join(msg))

                logger.info('c0:%s,c1:%s,c2:%s,c3:%s,c4:%s,c5:%s,c6:%s,c7:%s' % (c0, c1, c2, c3, c4, c5, c6, c7))
            pass

        if identity == 2:  # 实验指导
            # 返回的excel的表头
            sheet_ret.write(0, 0, 'ID')
            sheet_ret.write(0, 1, '姓名')
            sheet_ret.write(0, 2, '姓别')
            sheet_ret.write(0, 3, 'QQ')
            sheet_ret.write(0, 4, '昵称')
            sheet_ret.write(0, 5, '所在单位')
            sheet_ret.write(0, 6, '电话')
            sheet_ret.write(0, 7, '邮箱')
            sheet_ret.write(0, 8, '指导权限')
            sheet_ret.write(0, 9, '管理权限')
            sheet_ret.write(0, 10, '权限分配责任人')
            sheet_ret.write(0, 11, '导入状态')
            sheet_ret.write(0, 12, '反馈信息')
            # u'ID', u'姓名', u'姓别', u'QQ', u'昵称', u'所在单位', u'电话', u'邮箱', u'指导权限',
            # u'管理权限', u'权限分配责任人'
            for i in range(1, sheet.nrows):
                user = Tuser()  # 构造用户对象
                user.identity = identity
                user.set_password(const.PASSWORD_DEFAULT)
                user.is_active = 1
                flag = True  # 保存是否成功标志
                msg = []  # 错误信息

                # 获取excel数据行
                c0 = sheet.cell(i, 0).value
                if isinstance(c0, float):
                    c0 = int(c0)
                c1 = sheet.cell(i, 1).value
                c2 = sheet.cell(i, 2).value
                c3 = sheet.cell(i, 3).value
                if isinstance(c3, float):
                    c3 = int(c3)
                c4 = sheet.cell(i, 4).value
                c5 = sheet.cell(i, 5).value
                c6 = sheet.cell(i, 6).value
                if isinstance(c6, float):
                    c6 = int(c6)
                c7 = sheet.cell(i, 7).value
                c8 = sheet.cell(i, 8).value
                c9 = sheet.cell(i, 9).value
                c10 = sheet.cell(i, 10).value

                # 返回excel数据行
                sheet_ret.write(i, 0, c0)
                sheet_ret.write(i, 1, c1)
                sheet_ret.write(i, 2, c2)
                # sheet_ret.write(i, 3, c3)
                sheet_ret.write(i, 4, c4)
                # sheet_ret.write(i, 5, c5)
                # sheet_ret.write(i, 6, c6)
                sheet_ret.write(i, 7, c7)
                # sheet_ret.write(i, 8, c8)
                # sheet_ret.write(i, 9, c9)
                # sheet_ret.write(i, 10, request.user.name)

                if None in (c0, ):
                    flag = False
                    msg.append("错误：账号列1不允许为空")
                else:

                    # 检查账号是否为数字
                    if isinstance(c0, float):
                        c0 = int(c0)

                    # 检查账号是否存在
                    users = Tuser.objects.filter(username=c0, del_flag=0)
                    if users:
                        flag = False
                        msg.append('错误：(账户)已存在，（列1)')
                    else:
                        users = Tuser.objects.filter(username=c0)
                        if users:  # 如果用户时系统中有的， 恢复正常然后更新, md, 这都是什么鬼
                            user = users.first()
                            user.del_flag = 0
                            user.identity = identity
                        user.username = c0
                    # 姓名
                    if None in (c1, ):
                        flag = False
                        msg.append('错误：姓名列2不允许为空')
                    elif isinstance(c1, float):
                        flag = False
                        msg.append('错误：姓名列2不允许为数字(认真点好吗？谁家的名字是数字的)')
                    else:
                        # 姓名
                        user.name = c1

                    # 设置性别
                    user.gender = 1 if '男' == c2 else 2
                    # QQ
                    user.qq = c3
                    sheet_ret.write(i, 3, str(c3))
                    # 昵称
                    if isinstance(c4, float):
                        flag = False
                        msg.append('错误：昵称列5不允许为数字')
                    else:
                        user.nickname = c4

                    # 设置单位
                    # tcompany = TCompany.objects.filter(name=c5)
                    # if tcompany:
                    #     user.tcompany = tcompany.first()
                    # else:
                    #     msg.append('警告：(单位)有误，（列6)')
                    user.tcompany_id = request.user.tcompany_id
                    sheet_ret.write(i, 5, request.user.tcompany.name if request.user.tcompany else '')

                    # 电话
                    user.phone = c6
                    sheet_ret.write(i, 6, str(c6))
                    # 邮箱
                    user.email = c7

                    # 指导权限, 实验指导都具有指导权限
                    user.director = True
                    sheet_ret.write(i, 8, '否')
                    # 管理权限
                    # user.manage = True if '是' == c9 else False
                    user.manage = False
                    sheet_ret.write(i, 9, '否')

                    # 权限分配责任人
                    # assigned_by = Tuser.objects.filter(name=c10)
                    # if assigned_by:
                    #     user.assigned_by = assigned_by.first().id
                    # else:
                    #     msg.append('警告：(权限分配责任人)有误，（列11)')
                    user.assigned_by = request.user.id
                    sheet_ret.write(i, 10, request.user.name)

                # 保存用户并写入成功失败的状态和原因
                if flag:
                    user.save()
                    easemob_success, easemob_result = easemob.register_new_user(user.pk, easemob.EASEMOB_PASSWORD)
                    sheet_ret.write(i, 11, '成功')
                else:
                    sheet_ret.write(i, 11, '失败')
                sheet_ret.write(i, 12, '；'.join(msg))

                logger.info('c0:%s,c1:%s,c2:%s,c3:%s,c4:%s' % (c0, c1, c2, c3, c4))
            pass

        if identity == 3:  # 系统管理员
            # 返回的excel的表头
            sheet_ret.write(0, 0, 'ID')
            sheet_ret.write(0, 1, '姓名')
            sheet_ret.write(0, 2, '姓别')
            sheet_ret.write(0, 3, 'QQ')
            sheet_ret.write(0, 4, '昵称')
            sheet_ret.write(0, 5, '所在单位')
            sheet_ret.write(0, 6, '电话')

            sheet_ret.write(0, 7, '邮箱')
            sheet_ret.write(0, 8, '管理权限')
            sheet_ret.write(0, 9, '权限分配责任人')
            sheet_ret.write(0, 10, '导入状态')
            sheet_ret.write(0, 11, '反馈信息')
            # u'ID', u'姓名', u'姓别', u'QQ', u'昵称', u'所在单位', u'电话', u'邮箱', u'管理权限', u'权限分配责任人'
            for i in range(1, sheet.nrows):
                user = Tuser()  # 构造用户对象
                user.identity = identity
                user.set_password(const.PASSWORD_DEFAULT)
                user.is_active = 1
                flag = True  # 保存是否成功标志
                msg = []  # 错误信息

                # 获取excel数据行
                c0 = sheet.cell(i, 0).value
                if isinstance(c0, float):
                    c0 = int(c0)
                c1 = sheet.cell(i, 1).value
                c2 = sheet.cell(i, 2).value
                c3 = sheet.cell(i, 3).value
                if isinstance(c3, float):
                    c3 = int(c3)
                c4 = sheet.cell(i, 4).value
                c5 = sheet.cell(i, 5).value
                c6 = sheet.cell(i, 6).value
                if isinstance(c6, float):
                    c6 = int(c6)
                c7 = sheet.cell(i, 7).value
                c8 = sheet.cell(i, 8).value
                c9 = sheet.cell(i, 9).value

                # 返回excel数据行
                sheet_ret.write(i, 0, c0)
                sheet_ret.write(i, 1, c1)
                sheet_ret.write(i, 2, c2)
                # sheet_ret.write(i, 3, c3)
                sheet_ret.write(i, 4, c4)
                # sheet_ret.write(i, 5, c5)
                # sheet_ret.write(i, 6, c6)
                sheet_ret.write(i, 7, c7)
                # sheet_ret.write(i, 8, c8)
                # sheet_ret.write(i, 9, request.user.name)

                if None in (c0, ):
                    flag = False
                    msg.append("错误：账号列1不允许为空")
                else:

                    # 检查账号是否为数字
                    if isinstance(c0, float):
                        c0 = int(c0)

                    # 检查账号是否存在
                    users = Tuser.objects.filter(username=c0, del_flag=0)
                    if users:
                        flag = False
                        msg.append('错误：(账户)已存在，（列1)')
                    else:
                        users = Tuser.objects.filter(username=c0)
                        if users:  # 如果用户时系统中有的， 恢复正常然后更新, md, 这都是什么鬼
                            user = users.first()
                            user.del_flag = 0
                            user.identity = identity
                        user.username = c0
                    # 姓名
                    if None in (c1, ):
                        flag = False
                        msg.append('错误：姓名列2不允许为空')
                    elif isinstance(c1, float):
                        flag = False
                        msg.append('错误：姓名列2不允许为数字(认真点好吗？谁家的名字是数字的)')
                    else:
                        # 姓名
                        user.name = c1

                    # 设置性别
                    user.gender = 1 if '男' == c2 else 2
                    # QQ
                    user.qq = c3
                    sheet_ret.write(i, 3, str(c3))
                    # 昵称
                    user.nickname = c4

                    # 设置单位
                    # tcompany = TCompany.objects.filter(name=c5)
                    # if tcompany:
                    #     user.tcompany = tcompany.first()
                    # else:
                    #     msg.append('警告：(单位)有误，（列6)')
                    user.tcompany_id = request.user.tcompany_id
                    sheet_ret.write(i, 5, request.user.tcompany.name if request.user.tcompany else '')

                    # 电话
                    user.phone = c6
                    sheet_ret.write(i, 6, str(c6))
                    # 邮箱
                    user.email = c7

                    # 指导权限, 系统管理员都具有指导权限
                    user.director = True
                    # 管理权限, 系统管理员都具有管理权限
                    user.manage = True
                    sheet_ret.write(i, 8, '否')

                    # 权限分配责任人
                    # assigned_by = Tuser.objects.filter(name=c9)
                    # if assigned_by:
                    #     user.assigned_by = assigned_by.first().id
                    # else:
                    #     msg.append('警告：(权限分配责任人)有误，（列11)')
                    user.assigned_by = request.user.id
                    sheet_ret.write(i, 9, request.user.name)

                # 保存用户并写入成功失败的状态和原因
                if flag:
                    user.save()
                    easemob_success, easemob_result = easemob.register_new_user(user.pk, easemob.EASEMOB_PASSWORD)
                    sheet_ret.write(i, 10, '成功')
                else:
                    sheet_ret.write(i, 10, '失败')
                sheet_ret.write(i, 11, '；'.join(msg))

                logger.info('c0:%s,c1:%s,c2:%s,c3:%s,c4:%s' % (c0, c1, c2, c3, c4))
            pass

        # 返回带结果和原因的excel
        # response = HttpResponse(content_type='application/vnd.ms-excel')
        filename = u'用户导入结果反馈'
        # response['Content-Disposition'] = u'attachment;filename=%s.xls' % filename
        # report.save(response)
        report.save('media/%s.xls' % filename)
        resp = code.get_msg(code.SUCCESS)
        resp['d'] = {
            'file': '/media/%s.xls' % filename
        }
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_import Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 设置样式
def set_style(height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


# 导出用户列表
def api_account_export(request):
    resp = auth_check(request, "GET")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        identity = int(request.GET.get("identity", 1))  # 管理员类型，实验人员类型类型
        search = request.GET.get("search", None)  # 搜索关键字
        template = request.GET.get("template", None)  # 是否是模板

        if identity:
            users = Tuser.objects.filter(identity=identity, del_flag=0).filter(Q(name__contains=search) |
                                                                               Q(username__contains=search))

            if template == '1':
                user = users.first()
                users = []
                users.append(user)

            report = xlwt.Workbook(encoding='utf8')
            sheet = report.add_sheet(u'用户列表')
            row = 1
            if identity == 1:  # 实验人员
                title = [u'ID', u'姓名', u'班级', u'所在单位', u'性别', u'指导权限', u'管理权限', u'权限分配责任人']
                for r in users:
                    sheet.write(row, 0, r.username)
                    sheet.write(row, 1, r.name)
                    sheet.write(row, 2, r.tclass.name if r.tclass else '')
                    sheet.write(row, 3, r.tcompany.name if r.tcompany else '')
                    sheet.write(row, 4, '男' if r.gender == 1 else '女')
                    sheet.write(row, 5, '是' if r.director else '否')
                    sheet.write(row, 6, '是' if r.manage else '否')
                    assigned_by = None
                    if r.assigned_by:
                        assigned_by = Tuser.objects.get(id=r.assigned_by)
                    sheet.write(row, 7, assigned_by.name if assigned_by else '')
                    row += 1

            if identity == 2:  # 实验指导
                title = [u'ID', u'姓名', u'姓别', u'QQ', u'昵称', u'所在单位', u'电话', u'邮箱', u'指导权限',
                         u'管理权限', u'权限分配责任人']
                for r in users:
                    sheet.write(row, 0, r.username)
                    sheet.write(row, 1, r.name)
                    sheet.write(row, 2, '男' if r.gender == 1 else '女')
                    sheet.write(row, 3, r.qq)
                    sheet.write(row, 4, r.nickname)
                    sheet.write(row, 5, r.tcompany.name if r.tcompany else '')
                    sheet.write(row, 6, r.phone)
                    sheet.write(row, 7, r.email)
                    sheet.write(row, 8, '是' if r.director else '否')
                    sheet.write(row, 9, '是' if r.manage else '否')
                    assigned_by = None
                    if r.assigned_by:
                        assigned_by = Tuser.objects.get(id=r.assigned_by)
                    sheet.write(row, 10, assigned_by.name if assigned_by else '')
                    row += 1

            if identity == 3 or identity == 4:  # 系统管理员 or # 超级管理员
                title = [u'ID', u'姓名', u'姓别', u'QQ', u'昵称', u'所在单位', u'电话', u'邮箱', u'管理权限',
                         u'权限分配责任人']
                for r in users:
                    sheet.write(row, 0, r.username)
                    sheet.write(row, 1, r.name)
                    sheet.write(row, 2, '男' if r.gender == 1 else '女')
                    sheet.write(row, 3, r.qq)
                    sheet.write(row, 4, r.nickname)
                    sheet.write(row, 5, r.tcompany.name if r.tcompany else '')
                    sheet.write(row, 6, r.phone)
                    sheet.write(row, 7, r.email)
                    sheet.write(row, 8, '是' if r.manage else '否')
                    assigned_by = None
                    if r.assigned_by:
                        assigned_by = Tuser.objects.get(id=r.assigned_by)
                    sheet.write(row, 9, assigned_by.name if assigned_by else '')
                    row += 1

            # 设置样式
            for i in range(0, len(title)):
                sheet.write(0, i, title[i], set_style(220, True))

            response = HttpResponse(content_type='application/vnd.ms-excel')
            filename = urlquote(u'用户列表')
            response['Content-Disposition'] = u'attachment;filename=%s.xls' % filename
            report.save(response)
            return response
        else:
            resp = code.get_msg(code.SYSTEM_ERROR)
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
        resp = code.get_msg(code.SUCCESS)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_logout Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 用户权限编辑
def api_account_user_auth_update(request):
    resp = auth_check(request, "POST")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:

        user_id = request.POST.get('id', None)  # 账号
        is_admin = request.POST.get('is_admin', None)  # 超级管理员
        director = request.POST.get('director', None)  # 是否具有指导权限
        manage = request.POST.get('manage', None)  # 是否具有管理权限

        user = Tuser.objects.get(pk=user_id)
        if is_admin:
            user.is_admin = is_admin
        if director:
            user.director = director
        if manage:
            user.manage = manage

        user.save()

        resp = code.get_msg(code.SUCCESS)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_account_logout Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 删除用户
def api_course_user_delete(request):
    resp = auth_check(request, "GET")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        ids = request.GET.get("ids", None)  # 关联id，用逗号连接

        # 删除关联关系， 根据多个id删除
        id_arr = ids.split(',')
        if None in id_arr or u'' in id_arr:
            resp = code.get_msg(code.PARAMETER_ERROR)
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

        for delete_id in id_arr:
            item = Tuser.objects.get(pk=delete_id)
            item.del_flag = 1

            # 还有各种关联的东西要判断
            # 我的十二指肠都被绕痛了 这个项目的各种神逻辑回路太长 我现在只想删数据库跑路
            # 一期，二期都是谁设计的业务逻辑， 三期又是谁设计的业务逻辑， 神奇
            # 关联课堂不能被删除的
            cc = CourseClassStudent.objects.filter(student_id=delete_id)
            if cc:
                resp = {'c': 3333, 'm': u'关联课堂不能被删除的'}
                return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

            # 用户管理-删除实验者指导者功能中，教师如果关联了课堂是不能被删除的
            classes = CourseClass.objects.filter(Q(teacher1_id=delete_id) | Q(teacher2_id=delete_id))
            if classes:
                resp = {'c': 3333, 'm': u'有教师关联了课堂不能被删除的'}
                return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

            # 关联小组的用户不能被删除
            team_member = TeamMember.objects.filter(user_id=delete_id, del_flag=0)
            if team_member:
                resp = {'c': 3333, 'm': u'关联小组的用户不能被删除'}
                return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

            item.save()

        resp = code.get_msg(code.SUCCESS)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_course_user_delete Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")


# 三期 - 共享
def api_account_share(request):
    resp = auth_check(request, "GET")
    if resp != {}:
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    try:
        data = request.GET.get("data", None)  # id列表json:[1,2,3]
        if data is None:
            resp = code.get_msg(code.PARAMETER_ERROR)
            return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
        data = json.loads(data)
        ids_set = set(data)
        ids = [i for i in ids_set]
        Tuser.objects.filter(id__in=ids).update(is_share=1)

        resp = code.get_msg(code.SUCCESS)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")

    except Exception as e:
        logger.exception('api_workflow_list Exception:{0}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return HttpResponse(json.dumps(resp, ensure_ascii=False), content_type="application/json")
