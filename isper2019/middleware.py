# -*- coding: utf-8 -*-

import json
import logging
from django.utils.deprecation import MiddlewareMixin
from account.models import Tuser, TCompany, TClass, LoginLog, TRole, TCompanyManagerAssistants, TPermission, TAction, \
    TNotifications, WorkLog
from account.service import get_client_ip

logger = logging.getLogger(__name__)


class LogMiddleware(MiddlewareMixin):
    workLogMatch = {
        # workflow
        '/api/workflow/create': '新建流程',
        '/api/workflow/flow/copy': '复制为未发布流程',
        '/api/workflow/update': '编辑流程',
        '/api/workflow/delete': '删除流程',
        '/api/workflow/publish': '发布流程',
        '/api/workflow/public': '公开流程',
        '/api/workflow/unpublic': '不公开流程',
        '/api/workflow/share': '共享流程',
        # account
        '/api/account/set/assistants': '配置助理',
        '/api/account/unset/assistants': '取消绑定',
        '/api/account/password/update': '重置密码',
        '/api/account/user/create': '注册用户',
        '/api/account/set/roles/actions': '设置角色',
        # userManager
        '/api/userManager/excelDataSave':'导入用户',
        '/api/userManager/newUserSet':'增加用户',
        '/api/userManager/deleteUsers':'删除用户',
        '/api/userManager/set_Review':'审核',
        '/api/userManager/set_gChange':'变更集群',
        '/api/userManager/set_cChange':'变更单位',
        '/api/userManager/resetPass':'重置密码',
        # group & company
        '/api/group/create':'创建集群',
        '/api/group/delete':'删除集群',
        '/api/group/update':'更新集群',
        '/api/group/addManager':'添加集群管理员',
        '/api/group/addAssistant':'添加集群管理员助理',
        '/api/group/updateManager':'更新集群管理员',
        '/api/group/resetManager':'重置密码',
        '/api/group/saveInstructors':'保存集群指导者',
        '/api/group/createInstructors':'创建集群指导者',
        '/api/group/deleteGroupInstructor':'删除集群指导者',
        '/api/company/createCompany':'创建单位',
        '/api/company/deleteCompany':'删除单位',
        '/api/company/updateCompany':'更新单位',
        '/api/company/addCManager':'添加单位管理员',
        '/api/company/addCAssistant':'添加单位管理员助理',
        '/api/company/updateCManager':'更新单位管理员',
        '/api/company/pCResetManager':'重置密码',
        # dictionary
        '/api/dic/newItemSave':'添加事项',
        '/api/dic/editItemSave':'编辑事项',
        '/api/dic/deleteItemSave':'删除事项',
        '/api/advertising/create':'创建公告',
        '/api/advertising/delete$':'删除公告',
        # part Position
        '/api/partPosition/newPPSave':'添加部门和职务',
        '/api/partPosition/deletePPSave':'删除部门和职务',
        '/api/partPosition/setNewPP':'变更部门和职务',
        '/api/partPosition/setInnerPermissions':'内部权限管理',
        # project
        '/api/project/create':'创建项目',
        '/api/project/docs/create': '创建素材',
        '/api/project/docs/delete': '删除素材',
        '/api/project/update': '编辑项目',
        '/api/project/delete': '删除项目',
        '/api/project/share': '共享项目',
        '/api/project/unshare': '不共享项目',
        # business
        '/api/business/delete':'删除业务',
        '/api/business/recovery': '恢复业务',
        # course and student
        '/api/course/save_new': '新建课堂',
        '/api/course/excel_data_save': '导入课堂',
        '/api/course/delete_course': '删除课堂',
        '/api/course/save_edit': '编辑课堂',
        '/api/course/save_teacher_change$': '关联指导者',
        '/api/course/send_request_data': '签订关注许可',
        '/api/course/send_cancel_data': '取消关注协议',
    }

    def process_request(self, request):
        try:
            if request.path in self.workLogMatch.keys():
                user = None if request.user.is_anonymous else request.user if request.user else None
                loginType = request.session['login_type'] if 'login_type' in request.session else None
                targets = request.GET.get("targets", None) if request.method == 'GET'.upper() else request.POST.get(
                    "targets", None)
                role = user.roles.get(pk=loginType) if loginType else None
                group = None
                company = None
                if loginType == 1:
                    pass
                elif loginType == 2:
                    group = user.allgroups_set.get()
                elif loginType == 6:
                    group = user.allgroups_set_assistants.get()
                elif loginType == 3:
                    company_id = user.tcompanymanagers_set.get().tcompany.id
                    company = TCompany.objects.get(pk=company_id)
                    group = company.group
                elif loginType == 7:
                    company = user.t_company_set_assistants.get()
                    if company is not None:
                        group = company.group
                elif loginType == 4:
                    group = user.allgroups_set_instructors.all().first()
                elif loginType == 8:
                    group = user.allgroups_set_instructor_assistants.all().first()
                elif loginType is not None and user is not None:
                    company = user.tcompany
                    if company is not None:
                        group = company.group
                work_log = WorkLog(user=user, role=role, group=group, company=company, ip=get_client_ip(request),
                                   action=self.workLogMatch[request.path], targets=targets, request_url=request.path)
                work_log.save()
        except Exception as e:
            logger.exception('middleware Request Exception:{0}'.format(str(e)))
