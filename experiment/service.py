# -*- coding: utf-8 -*-
import logging

from datetime import datetime

from account.service import user_simple_info
from django.db import transaction
from django.db.models import Q
from experiment.models import *
from course.models import CourseClass
from project.models import ProjectRole, Project, ProjectRoleAllocation, ProjectJump, ProjectDocRole, ProjectDoc
from team.models import Team, TeamMember
from utils import code, const, query, tools
from workflow.models import FlowRolePosition, FlowPosition, FlowNode, FlowTrans, RoleImage, RoleImageFile, \
    FlowProcess, ProcessAction, FlowDocs, FlowNodeDocs
from workflow.service import get_start_node
from django.core.cache import cache
from django.conf import settings
from docx import Document
import os

logger = logging.getLogger(__name__)


def set_cache_keys(experiment_id, item):
    """
    保存缓存key列表
    """
    pass
    # try:
    #     key = tools.make_key(const.CACHE_EXPERIMENT_KEYS, experiment_id, 1)
    #     data = cache.get(key)
    #     if data:
    #         if item not in data:
    #             data.append(item)
    #     else:
    #         data = [item]
    #         cache.set(key, data)
    # except Exception as e:
    #     logger.exception(u'set_cache_keys Exception:{}'.format(str(e)))


def clear_cache(experiment_id):
    """
    清除缓存
    """
    cache.clear()
    # try:
    #     key = tools.make_key(const.CACHE_EXPERIMENT_KEYS, experiment_id, 1)
    #     data = cache.get(key)
    #     cache.delete_many(data)
    #     cache.delete(key)
    # except Exception as e:
    #     logger.exception(u'set_cache_keys Exception:{}'.format(str(e)))


def experiment_can_start(exp, project_id):
    """
    实验是否可以开始（所有小组成员均分配角色，角色全部分配）
    :param exp: 实验对象
    :return:
    """
    user_ids1 = MemberRole.objects.filter(experiment_id=exp.id, project_id=project_id,
                                          del_flag=0).values_list('user_id', flat=True)
    user_ids2 = TeamMember.objects.filter(team_id=exp.team_id, del_flag=0).values_list('user_id', flat=True)
    member_role_count = MemberRole.objects.filter(experiment_id=exp.id, project_id=project_id, del_flag=0).count()
    role_count = ProjectRole.objects.filter(Q(project_id=project_id) & ~Q(type=const.ROLE_TYPE_OBSERVER)).count()

    user_ids_set1 = set(user_ids1)
    user_ids_set2 = set(user_ids2)

    if user_ids_set2 != user_ids_set1 or member_role_count != role_count:
        return False
    else:
        return True


def check_jump_project(project):
    """
    实验是否可以开始（所有小组成员均分配角色，角色全部分配）
    :param exp: 实验对象
    :return:
    """
    flag = True
    jump_process = FlowProcess.objects.filter(type=const.PROCESS_JUMP_TYPE,
                                              del_flag=const.DELETE_FLAG_NO).first()
    if jump_process:
        jumps = FlowNode.objects.filter(flow_id=project.flow_id, process=jump_process,
                                        del_flag=const.DELETE_FLAG_NO).count()
        if jumps > 0:
            count = ProjectJump.objects.filter(project_id=project.pk).count()
            if jumps > count:
                flag = False
    return flag


def action_role_banned(exp, node_id, path_id, control_status):
    """
    表达管理
    :param control_status:  表达管理状态：1，未启动；2，已启动
    :param exp: 实验
    :return:
    """
    try:
        ExperimentTransPath.objects.filter(pk=exp.path_id).update(control_status=control_status)
        if control_status == 2:
            ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id,
                                                path_id=path_id).update(speak_times=0, show_status=9, submit_status=9)
        opt = {'control_status': control_status}
        return True, opt
    except Exception as e:
        logger.exception(u'action_role_banned Exception:{}'.format(str(e)))
        return False, str(e)


def action_role_meet(exp, node_id, path_id, role):
    """
    申请约见
    :param role_id: 角色id
    :param node_id: 环节id
    :param exp: 实验
    :return:
    """
    try:
        ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                            role_id=role.id).update(come_status=1, stand_status=2)

        role_info = {'id': role.id, 'name': role.name}
        return True, role_info
    except Exception as e:
        logger.exception(u'action_role_meet Exception:{}'.format(str(e)))
        return False, str(e)


def action_role_speak_opt(exp, node_id, path_id, data):
    """
    申请发言操作结果
    :param exp: 实验
    :param node_id: 环节id
    :param role_id: 角色id
    :param is_pass: 是否同意: 1,同意；2，不同意
    :return:
    """
    try:
        if 'msg_id' in data.keys():
            ExperimentMessage.objects.filter(pk=data['msg_id']).update(opt_status=True)
        role_status = ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                          role_id=data['role_id']).first()
        if role_status and int(data['result']) == 1:
            role_status.speak_times = const.MESSAGE_MAX_TIMES
            role_status.save(update_fields=['speak_times'])
        role = ProjectRole.objects.get(pk=data['role_id'])
        return True, {'role_id': data['role_id'], 'role_name': role.name, 'result': data['result']}
    except Exception as e:
        logger.exception(u'action_role_speak_opt Exception:{}'.format(str(e)))
        return False, str(e)


def action_doc_apply_show_opt(exp, node_id, path_id, data):
    """
    申请展示操作结果
    :param exp: 实验
    :param node_id: 环节id
    :param role_id: 角色id
    :param is_pass: 是否同意: 1,同意；2，不同意
    :return:
    """
    try:
        if 'msg_id' in data.keys():
            ExperimentMessage.objects.filter(pk=data['msg_id']).update(opt_status=True)
        ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                            role_id=data['role_id']).update(show_status=data['result'])
        role = ProjectRole.objects.get(pk=data['role_id'])
        return True, {'role_id': data['role_id'], 'role_name': role.name, 'result': data['result']}
    except Exception as e:
        logger.exception(u'action_doc_apply_show_opt Exception:{}'.format(str(e)))
        return False, str(e)


def action_doc_show(doc_id):
    """
    展示
    :return:
    """
    try:
        if doc_id is None:
            resp = code.get_msg(code.PARAMETER_ERROR)
            return False, resp
        doc = ExperimentDoc.objects.filter(pk=doc_id).first()
        data = {
            'id': doc.id, 'name': doc.filename, 'url': doc.file.url, 'file_type': doc.file_type
        }
        return True, data
    except Exception as e:
        logger.exception(u'action_role_apply_show Exception:{}'.format(str(e)))
        return False, str(e)


def action_role_letout(exp, node, path_id, role_ids):
    """
    送出
    :return:
    """
    try:
        with transaction.atomic():
            ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node.pk, path_id=path_id,
                                                role_id__in=role_ids).exclude(come_status=9).update(come_status=1,
                                                                                                    sitting_status=1,
                                                                                                    stand_status=2)
            # 报告席
            report_pos = FlowPosition.objects.filter(process=node.process, type=const.SEAT_REPORT_TYPE).first()

            role_list = []
            for role_id in role_ids:
                role = ProjectRole.objects.get(pk=role_id)
                report_exists = ExperimentReportStatus.objects.filter(experiment_id=exp.pk, node_id=node.pk,
                                                                      path_id=path_id, role_id=role.pk,
                                                                      schedule_status=const.SCHEDULE_UP_STATUS).exists()
                if report_exists:
                    ExperimentReportStatus.objects.filter(experiment_id=exp.pk, node_id=node.pk,
                                                          path_id=path_id, role_id=role.pk,
                                                          schedule_status=const.SCHEDULE_UP_STATUS).update(
                        schedule_status=const.SCHEDULE_INIT_STATUS)

                    pos = report_pos
                else:
                    role_position = FlowRolePosition.objects.filter(node_id=node.pk, role_id=role.flow_role_id).first()
                    pos = FlowPosition.objects.filter(pk=role_position.position_id).first()

                # 占位状态更新
                ExperimentPositionStatus.objects.filter(experiment_id=exp.id, node_id=node.pk, path_id=path_id,
                                                        position_id=pos.id).update(sitting_status=1, role_id=None)

                role_list.append({
                    'id': role.id, 'name': role.name,
                    'code_position': pos.code_position if pos else ''
                })
        return True, role_list
    except Exception as e:
        logger.exception(u'action_role_letout Exception:{}'.format(str(e)))
        return False, str(e)


def action_role_letin(exp, node_id, path_id, role_ids):
    """
    请入
    :param exp: 实验
    :param node_id: 环节id
    :param role_ids: 角色id列表
    :return:
    """
    try:
        project = Project.objects.get(pk=exp.cur_project_id)
        role_list = []
        role_status_list = ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                               role_id__in=role_ids)
        for role_status in role_status_list:
            project_role = ProjectRole.objects.filter(pk=role_status.role_id).first()

            if project_role:
                role_position = FlowRolePosition.objects.filter(flow_id=project.flow_id, node_id=node_id,
                                                                role_id=project_role.flow_role_id).first()
                image = RoleImage.objects.filter(pk=project_role.image_id).first()

            else:
                continue

            qs_files = RoleImageFile.objects.filter(image=image)
            actors = []
            if role_position:
                pos = FlowPosition.objects.filter(pk=role_position.position_id).first()
                if pos:
                    # 占位状态更新
                    pos_status = ExperimentPositionStatus.objects.filter(experiment_id=exp.id, node_id=node_id,
                                                                         path_id=path_id, position_id=pos.id).first()
                    if pos_status:
                        if pos_status.sitting_status == const.SITTING_UP_STATUS and role_status.come_status != 9:
                            pos_status.sitting_status = const.SITTING_DOWN_STATUS
                            pos_status.save(update_fields=['sitting_status'])
                            role_status.come_status = 2
                            role_status.sitting_status = const.SITTING_DOWN_STATUS
                            role_status.save(update_fields=['come_status', 'sitting_status'])
                        else:
                            continue
                    else:
                        # 占位状态
                        ExperimentPositionStatus.objects.update_or_create(experiment_id=exp.id, node_id=node_id,
                                                                          path_id=path_id, position_id=pos.id,
                                                                          defaults={'sitting_status': 2,
                                                                                    'role_id': role_status.role_id})
                        if role_status.come_status != 9:
                            role_status.come_status = 2
                            role_status.sitting_status = const.SITTING_DOWN_STATUS
                            role_status.save(update_fields=['come_status', 'sitting_status'])

                    if pos.actor1:
                        actor1 = qs_files.filter(direction=pos.actor1).first()
                        actors.append(('/media/' + actor1.file.name) if actor1 and actor1.file else '')
                    if pos.actor2:
                        actor2 = qs_files.filter(direction=pos.actor2).first()
                        actors.append(('/media/' + actor2.file.name) if actor2 and actor2.file else '')
                    position = {'id': pos.id, 'position': pos.position, 'code_position': pos.code_position}
                else:
                    continue
            else:
                continue

            role_list.append({
                'role_id': role_status.role_id, 'role_name': project_role.name,
                'user': user_simple_info(role_status.user_id),
                'come_status': role_status.come_status,
                'sitting_status': role_status.sitting_status,
                'stand_status': role_status.stand_status, 'position': position,
                'actors': actors, 'gender': image.gender if image else 1
            })
        return True, role_list
    except Exception as e:
        logger.exception(u'action_role_letin Exception:{}'.format(str(e)))
        return False, str(e)


def action_role_sitdown(exp, node_id, path_id, role, pos):
    """
    坐下
    :return:
    """
    try:
        ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                            role_id=role.id).update(stand_status=2)

        role_info = {'id': role.id, 'name': role.name, 'code_position': pos['code_position']}
        return True, role_info
    except Exception as e:
        logger.exception(u'action_role_sitdown Exception:{}'.format(str(e)))
        return False, str(e)


def action_role_stand(exp, node_id, path_id, role, pos):
    """
    起立
    :return:
    """
    try:
        ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                            role_id=role.id).update(stand_status=1)

        role_info = {'id': role.id, 'name': role.name, 'code_position': pos['code_position']}
        return True, role_info
    except Exception as e:
        logger.exception(u'action_role_stand Exception:{}'.format(str(e)))
        return False, str(e)


def action_role_hide(exp, node_id, path_id, role, pos):
    """
    退席
    :return:
    """
    try:
        with transaction.atomic():
            ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                role_id=role.id).update(stand_status=2, sitting_status=1)
            # 占位状态
            ExperimentPositionStatus.objects.update_or_create(experiment_id=exp.id, node_id=node_id,
                                                              path_id=path_id, position_id=pos['position_id'],
                                                              defaults={'sitting_status': const.SITTING_UP_STATUS,
                                                                        'role_id': None}
                                                              )
            role_info = {'id': role.id, 'name': role.name, 'code_position': pos['code_position']}

        return True, role_info
    except Exception as e:
        logger.exception(u'action_role_hide Exception:{}'.format(str(e)))
        return False, str(e)


def action_role_show(exp, node_id, path_id, role, pos):
    """
    入席
    :return:
    """
    try:
        # 角色状态
        ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                            role_id=role.id).update(stand_status=2, sitting_status=2)

        role_status = ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                          role_id=role.id).first()

        # 占位状态
        ExperimentPositionStatus.objects.update_or_create(experiment_id=exp.id, node_id=node_id,
                                                          path_id=path_id, position_id=pos['position_id'],
                                                          defaults={'sitting_status': const.SITTING_DOWN_STATUS,
                                                                    'role_id': role.pk})

        image = RoleImage.objects.filter(pk=role.image_id).first()
        qs_files = RoleImageFile.objects.filter(image=image)
        actors = []
        if pos['actor1']:
            actor1 = qs_files.filter(direction=pos['actor1']).first()
            actors.append(('/media/' + actor1.file.name) if actor1 and actor1.file else '')
        if pos['actor2']:
            actor2 = qs_files.filter(direction=pos['actor2']).first()
            actors.append(('/media/' + actor2.file.name) if actor2 and actor2.file else '')
        position = {'id': pos['position_id'], 'position': pos['position'], 'code_position': pos['code_position']}

        role_info = {
            'role_id': role_status.role_id, 'user': user_simple_info(role_status.user_id),
            'come_status': role_status.come_status, 'sitting_status': role_status.sitting_status,
            'stand_status': role_status.stand_status, 'position': position,
            'actors': actors, 'gender': image.gender if image else 1
        }
        return True, role_info
    except Exception as e:
        logger.exception(u'action_role_show Exception:{}'.format(str(e)))
        return False, str(e)


def action_doc_apply_submit_opt(exp, node_id, path_id, data):
    """
    申请提交操作结果
    :param exp: 实验
    :param node_id: 环节id
    :param role_id: 角色id
    :param is_pass: 是否同意: 1,同意；2，不同意
    :return:
    """
    try:
        if 'msg_id' in data.keys():
            ExperimentMessage.objects.filter(pk=data['msg_id']).update(opt_status=True)
        ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                            role_id=data['role_id']).update(submit_status=data['result'])
        role = ProjectRole.objects.get(pk=data['role_id'])
        return True, {'role_id': data['role_id'], 'role_name': role.name, 'result': data['result']}
    except Exception as e:
        logger.exception(u'action_doc_apply_submit_opt Exception:{}'.format(str(e)))
        return False, str(e)


def action_doc_submit(doc_ids):
    """
    提交
    :return:
    """
    try:
        doc_list = []
        for doc_id in doc_ids:
            doc = ExperimentDoc.objects.filter(pk=doc_id).first()
            doc_list.append({
                'id': doc.id, 'name': doc.filename, 'url': doc.file.url, 'file_type': doc.file_type
            })
        return True, doc_list
    except Exception as e:
        logger.exception(u'action_role_apply_submit Exception:{}'.format(str(e)))
        return False, str(e)


def get_pre_node_path(exp):
    """
    获取上一个环节信息
    :param exp: 实验
    :return:
    """
    try:
        cur_path = ExperimentTransPath.objects.filter(experiment_id=exp.id,
                                                      node_id=exp.node_id).last()
        if cur_path is None:
            return None
        if cur_path.step == 1:
            return None
        pre_path = ExperimentTransPath.objects.filter(experiment_id=exp.id,
                                                      step__lt=cur_path.step).last()
        if pre_path is None:
            return None
        return pre_path
    except Exception as e:
        logger.exception(u'get_pre_node_path Exception:{}'.format(str(e)))
        return None


def get_user_with_node(exp, user_id):
    """
    实验下一环节
    """
    nodes = []
    try:
        role_ids = MemberRole.objects.filter(experiment_id=exp.pk, project_id=exp.cur_project_id,
                                             user_id=user_id, del_flag=0).values_list('role_id', flat=True)
        node_ids = ProjectRoleAllocation.objects.filter(project_id=exp.cur_project_id,
                                                        role_id__in=role_ids).values_list('node_id', flat=True)
        nodes = list(FlowNode.objects.filter(id__in=node_ids).values_list('name', flat=True))
    except Exception as e:
        logger.exception(u'get_user_with_node Exception:{}'.format(str(e)))
    return nodes


def action_exp_back(exp):
    """
    实验环节回退
    :param exp: 实验
    :return:
    """
    try:
        if exp.status == 9:  # 如果实验已结束
            resp = code.get_msg(code.EXPERIMENT_HAS_FINISHED)
            return False, resp
        elif exp.status == 1:  # 如果实验还未开始
            resp = code.get_msg(code.EXPERIMENT_HAS_NOT_STARTED)
            return False, resp
        else:  # 如果实验正在进行中
            previous_path = get_pre_node_path(exp)
            if previous_path:
                previous_node = FlowNode.objects.filter(pk=previous_path.node_id).first()
                if previous_node is None:
                    resp = code.get_msg(code.EXPERIMENT_IN_FIRST_NODE)
                    return False, resp

                cur_node_id = exp.node_id
                with transaction.atomic():
                    # 删除当前环节路径已保存的信息
                    cur_path = ExperimentTransPath.objects.filter(experiment_id=exp.id).last()
                    ExperimentDoc.objects.filter(experiment_id=exp.id, node_id=cur_node_id,
                                                 path_id=cur_path.id).delete()
                    ExperimentExperience.objects.filter(experiment_id=exp.id).delete()
                    ExperimentMessage.objects.filter(experiment_id=exp.id, node_id=cur_node_id,
                                                     path_id=cur_path.id).delete()
                    ExperimentMessageFile.objects.filter(experiment_id=exp.id, node_id=cur_node_id,
                                                         path_id=cur_path.id).delete()
                    ExperimentNotes.objects.filter(experiment_id=exp.id, node_id=cur_node_id).delete()
                    ExperimentDocContent.objects.filter(experiment_id=exp.id, node_id=cur_node_id).delete()
                    ExperimentRoleStatus.objects.filter(experiment_id=exp.id, path_id=cur_path.pk).delete()
                    ExperimentReportStatus.objects.filter(experiment_id=exp.id, path_id=cur_path.pk).delete()
                    ExperimentPositionStatus.objects.filter(experiment_id=exp.id, path_id=cur_path.pk).delete()

                    # 如上一环节和当前环节项目不一致，清除跳转项目用户角色配置
                    if cur_path.project_id != previous_path.project_id:
                        MemberRole.objects.filter(experiment_id=exp.id, project_id=cur_path.project_id).delete()

                    # 删除最后一步
                    if cur_path.step > 1:
                        cur_path.delete()
                    else:
                        first_count = ExperimentTransPath.objects.filter(experiment_id=exp.id, setp=1).count()
                        if first_count > 1:
                            ExperimentTransPath.objects.filter(experiment_id=exp.id, setp=1).last().delete()

                    path = ExperimentTransPath.objects.filter(experiment_id=exp.id).last()

                    exp.cur_project_id = previous_path.project_id
                    exp.node_id = previous_path.node_id
                    exp.path_id = path.pk
                    exp.save()
                    opt = {
                        'node_id': previous_node.id, 'name': previous_node.name, 'condition': previous_node.condition,
                        'experiment_id': exp.id, 'process_type': previous_node.process.type
                    }
                    return True, opt
            else:
                resp = code.get_msg(code.EXPERIMENT_IN_FIRST_NODE)
                return False, resp
    except Exception as e:
        logger.exception(u'action_exp_back Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def action_exp_restart(exp, user_id):
    """
    重新开始实验
    :param exp: 实验
    :return:
    """
    try:
        if exp and exp.status == 2:
            # 查询小组组长
            team = Team.objects.filter(pk=exp.team_id).first()
            can_opt = True if exp.created_by == user_id or team.leader == user_id else False
            if can_opt is False:
                resp = code.get_msg(code.EXPERIMENT_PERMISSION_DENIED)
                return False, resp
            # 初始项目
            project = Project.objects.get(pk=exp.project_id)
            first_node_id = get_start_node(project.flow_id)
            logger.info('first_node_id: {}'.format(first_node_id))

            with transaction.atomic():
                # 删除实验流程中产生的相关信息（文件、心得、消息、笔记、编辑内容）
                ExperimentDoc.objects.filter(experiment_id=exp.id).delete()
                ExperimentExperience.objects.filter(experiment_id=exp.id).delete()
                ExperimentMessage.objects.filter(experiment_id=exp.id).delete()
                ExperimentMessageFile.objects.filter(experiment_id=exp.id).delete()
                ExperimentNotes.objects.filter(experiment_id=exp.id).delete()
                ExperimentDocContent.objects.filter(experiment_id=exp.id).delete()
                ExperimentRoleStatus.objects.filter(experiment_id=exp.id).delete()
                ExperimentReportStatus.objects.filter(experiment_id=exp.id).delete()
                ExperimentPositionStatus.objects.filter(experiment_id=exp.id).delete()
                ExperimentTransPath.objects.filter(experiment_id=exp.id).delete()

                # 清除跳转项目用户角色配置
                MemberRole.objects.filter(experiment_id=exp.id).exclude(project_id=exp.project_id).delete()

                # 实验路径
                node = FlowNode.objects.get(pk=first_node_id)
                path = ExperimentTransPath.objects.create(experiment_id=exp.pk, node_id=first_node_id,
                                                          project_id=exp.project_id, task_id=node.task_id, step=1)

                # 设置初始环节角色状态信息
                allocation = ProjectRoleAllocation.objects.filter(project_id=project.pk, node_id=first_node_id)
                role_status_list = []
                for item in allocation:
                    if item.can_brought:
                        come_status = 1
                    else:
                        come_status = 9
                    # role_status_list.append(ExperimentRoleStatus(experiment_id=exp.id, node_id=item.node_id,
                    #                                              path_id=path.pk, role_id=item.role_id,
                    #                                              come_status=come_status))
                    # 三期 - 不能直接创建， 在service中结束并走向下一环节的时候会创建角色状态，这里再创建一次就重复了
                    ers = ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=item.node_id,
                                                              path_id=path.pk,
                                                              role_id=item.role_id)
                    if ers:  # 存在则更新
                        ers = ers.first()
                        ers.come_status = come_status
                        ers.save()
                    else:  # 不存在则创建
                        ExperimentRoleStatus.objects.update_or_create(experiment_id=exp.id, node_id=item.node_id,
                                                                      path_id=path.pk, role_id=item.role_id,
                                                                      come_status=come_status)

                # ExperimentRoleStatus.objects.bulk_create(role_status_list)
                # 设置环节中用户的角色状态
                member_roles = MemberRole.objects.filter(experiment_id=exp.id, del_flag=0)
                for item in member_roles:
                    ExperimentRoleStatus.objects.filter(experiment_id=exp.id,
                                                        role_id=item.role_id).update(user_id=item.user_id)
                exp.cur_project_id = exp.project_id
                exp.node_id = first_node_id
                exp.path_id = path.pk
                exp.save()
            node = FlowNode.objects.filter(pk=first_node_id).first()
            opt = {
                'node_id': node.id, 'name': node.name, 'condition': node.condition,
                'experiment_id': exp.pk, 'process_type': node.process.type
            }
            return True, opt
        elif exp is None:
            resp = code.get_msg(code.EXPERIMENT_NOT_EXIST)
            return False, resp
        elif exp.status == 9:
            resp = code.get_msg(code.EXPERIMENT_HAS_FINISHED)
            return False, resp
        elif exp.status == 1:
            resp = code.get_msg(code.EXPERIMENT_HAS_NOT_STARTED)
            return False, resp
        else:
            # resp = code.get_msg(code.SYSTEM_ERROR)
            # return False, resp
            pass
    except Exception as e:
        logger.exception(u'action_exp_restart Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def action_exp_node_end(exp, role_id, data):
    """
    结束实验环节
    :param tran_id: 环节流转id
    :param exp: 实验
    :param role_id: 实验角色id
    :return:
    """
    try:
        # 当前项目环节权限判断
        if not ProjectRoleAllocation.objects.filter(project_id=exp.cur_project_id, node_id=exp.node_id, role_id=role_id,
                                                    can_terminate=True).exists():
            resp = code.get_msg(code.PERMISSION_DENIED)
            return False, resp
        else:
            if data['tran_id'] == 0 or data['tran_id'] == '0':
                next_node = None
            else:
                tran = FlowTrans.objects.get(pk=data['tran_id'])
                next_node = FlowNode.objects.filter(flow_id=tran.flow_id, task_id=tran.outgoing).first()

            if 'project_id' in data.keys() and data['project_id']:
                # 如果是跳转项目
                project = Project.objects.filter(pk=data['project_id']).first()
            else:
                project = Project.objects.filter(pk=exp.cur_project_id).first()

            if next_node is None:
                # 结束实验，验证实验心得
                experience_count = ExperimentExperience.objects.filter(experiment_id=exp.id, del_flag=0).count()
                role_ids = ProjectRoleAllocation.objects.filter(project_id=project.pk,
                                                                node_id=exp.node_id).values_list('role_id', flat=True)
                # logger.info(role_ids)
                user_count = MemberRole.objects.filter(experiment_id=exp.id, project_id=project.pk, del_flag=0,
                                                       role_id__in=role_ids).values('user_id').distinct().count()
                logger.info('user_count=%s' % user_count)
                if experience_count < user_count:
                    resp = code.get_msg(code.EXPERIMENT_EXPERIENCE_USER_NOT_SUBMIT)
                    return False, resp

                exp.status = 9
                exp.finish_time = datetime.now()
                process_type = 0
            else:
                process_type = next_node.process.type
                cur_node = FlowNode.objects.filter(pk=exp.node_id).first()
                # 判断是否投票环节和配置
                cur_path = ExperimentTransPath.objects.filter(experiment_id=exp.pk).last()
                if cur_node.process.type == const.PROCESS_VOTE_TYPE:
                    cur_path = ExperimentTransPath.objects.filter(experiment_id=exp.pk).last()

                    if cur_path.vote_status == 1:
                        resp = code.get_msg(code.EXPERIMENT_ROLE_VOTE_NOT_END)
                        return False, resp

                # 创建新环节路径
                step = ExperimentTransPath.objects.filter(experiment_id=exp.id).count() + 1
                path = ExperimentTransPath.objects.create(experiment_id=exp.id, node_id=next_node.pk,
                                                          project_id=project.pk, task_id=next_node.task_id,
                                                          step=step)
                # 设置初始环节角色状态信息 按实验路径创建
                allocation = ProjectRoleAllocation.objects.filter(project_id=project.pk, node_id=next_node.pk)

                role_status_list = []
                for item in allocation:
                    if item.can_brought:
                        come_status = 1
                    else:
                        come_status = 9
                    # role_status_list.append(
                    #     ExperimentRoleStatus(experiment_id=exp.id, node_id=item.node_id, path_id=path.pk,
                    #                          role_id=item.role_id, come_status=come_status))
                    # 三期 - 不能直接创建， 在service中结束并走向下一环节的时候会创建角色状态，这里再创建一次就重复了
                    ers = ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=item.node_id,
                                                              path_id=path.pk,
                                                              role_id=item.role_id)
                    if ers:  # 存在则更新
                        ers = ers.first()
                        ers.come_status = come_status
                        ers.save()
                    else:  # 不存在则创建
                        ExperimentRoleStatus.objects.update_or_create(experiment_id=exp.id, node_id=item.node_id,
                                                                      path_id=path.pk, role_id=item.role_id,
                                                                      come_status=come_status)
                # ExperimentRoleStatus.objects.bulk_create(role_status_list)

                # 设置环节中用户的角色状态
                member_roles = MemberRole.objects.filter(experiment_id=exp.id, project_id=project.pk, del_flag=0)
                for item in member_roles:
                    ExperimentRoleStatus.objects.filter(experiment_id=exp.id,
                                                        role_id=item.role_id).update(user_id=item.user_id)
                    # 三期 - 当上下两个环节的场景一样、角色一致，则下一个环节启动后，所有具备入席权限的角色自动在席
                    # 这样实现不行，会引入重复角色的bug
                    if cur_node.process_id == next_node.process_id:
                        item_role = ProjectRole.objects.filter(pk=item.role_id).first()
                        # 角色占位
                        pos = get_role_position(exp, project, next_node, item_role)
                        if pos:
                            # 占位状态, 如果上一环节占位存在并且已入席则创建当前环节占位数据
                            eps = ExperimentPositionStatus.objects.filter(experiment_id=exp.id, node_id=cur_node.id,
                                                                          path_id=cur_path.id, role_id=item.role_id)\
                                .first()
                            if eps and eps.sitting_status == const.SITTING_DOWN_STATUS:
                                ExperimentPositionStatus.objects.filter(experiment_id=exp.id, node_id=next_node.pk,
                                                                        path_id=path.id, role_id=item.role_id).update(
                                    sitting_status=const.SITTING_DOWN_STATUS)
                            # 角色状态， 如果上一环节角色存在并且已入席则创建当前环节占位数据
                            ers = ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=cur_node.id,
                                                                      user_id=item.user_id, role_id=item.role_id,
                                                                      path_id=cur_path.id).first()
                            if ers and ers.sitting_status == const.SITTING_DOWN_STATUS:
                                ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=next_node.pk,
                                                                    user_id=item.user_id, role_id=item.role_id,
                                                                    path_id=path.id).update(
                                    sitting_status=const.SITTING_DOWN_STATUS)

                exp.cur_project_id = project.pk
                exp.node_id = next_node.pk
                exp.path_id = path.pk
            exp.save()
            exp.save()
            exp.save()
            exp.save()

            opt = {'node_id': next_node.pk if next_node else None, 'status': exp.status,
                   'experiment_id': exp.pk, 'process_type': process_type}
            return True, opt
    except Exception as e:
        logger.exception(u'action_exp_node_end Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def action_submit_experience(exp, content, user_id):
    """
    实验
    :param exp: 实验
    :param content: 心得内容
    :param user_id 用户id
    :return:
    """
    try:
        if exp.status == 2:
            if content is None or len(content) > 30000:
                return False, code.get_msg(code.PARAMETER_ERROR)

            if ExperimentExperience.objects.filter(experiment_id=exp.id, created_by=user_id, status=2).exists():
                return False, code.get_msg(code.EXPERIMENT_EXPERIENCE_HAS_EXIST)

            instance, flag = ExperimentExperience.objects.update_or_create(experiment_id=exp.id,
                                                                           created_by=user_id,
                                                                           defaults={'content': content,
                                                                                     'created_by': user_id,
                                                                                     'status': 2})
            opt = {
                'id': instance.id, 'content': instance.content, 'status': instance.status,
                'created_by': user_simple_info(instance.created_by),
                'create_time': instance.create_time.strftime('%Y-%m-%d')
            }
            return True, opt
        elif exp.status == 1:
            return False, code.get_msg(code.EXPERIMENT_HAS_NOT_STARTED)
        else:
            return False, code.get_msg(code.EXPERIMENT_HAS_FINISHED)
    except Exception as e:
        logger.exception(u'action_submit_experience Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def action_exp_finish(exp, user_id):
    """
    提前结束实验
    :param exp: 实验
    :param user_id: 用户
    :return:
    """
    try:
        if exp.status == const.EXPERIMENT_WAITING:
            resp = code.get_msg(code.EXPERIMENT_HAS_NOT_STARTED)
            result = False
        elif exp.status == const.EXPERIMENT_PROCESSING:
            team = Team.objects.filter(pk=exp.team_id).first()
            if team and team.leader == user_id:
                exp.status = const.EXPERIMENT_FINISHED
                exp.finish_time = datetime.now()
                exp.save()
                opt = {'status': exp.status,
                       'experiment_id': exp.pk}
                result, resp = True, opt
            else:
                result, resp = False, code.get_msg(code.PERMISSION_DENIED)
        else:
            resp = code.get_msg(code.EXPERIMENT_HAS_FINISHED)
            result = False
        return result, resp
    except Exception as e:
        logger.exception(u'action_exp_finish Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def experiment_template_save(experiment_id, node_id, name, content):
    """
    保存应用模板生成文件
    :param content: 内容
    :param doc_id: 模板id
    :return:
    """
    path = ''
    try:
        # 打开文档
        document = Document()
        # 添加文本
        document.add_paragraph(content)
        # 保存文件
        media = settings.MEDIA_ROOT
        path = u'{}/experiment/{}'.format(media, experiment_id)
        is_exists = os.path.exists(path)
        if not is_exists:
            os.makedirs(path)
        media_path = u'{}/{}-{}'.format(path, node_id, name)
        logger.info(media_path)
        document.save(media_path)

        path = u'experiment/{}/{}-{}'.format(experiment_id, node_id, name)
    except Exception as e:
        logger.exception(u'experiment_template_save Exception:{}'.format(str(e)))
    return path


# 当前环节所有角色状态
def action_roles_vote_status(exp, node_id, path):
    sql = '''SELECT t.role_id,t.vote_status, r.`name` role_name,u.`name` user_name
    from t_experiment_role_status t
    LEFT JOIN t_project_role r ON t.role_id=r.id
    LEFT JOIN t_user u ON t.user_id=u.id
    WHERE t.experiment_id=%s and t.node_id=%s and t.path_id=%s''' % (exp.pk, node_id, path.pk)
    sql += ' and r.name != \'' + const.ROLE_TYPE_OBSERVER + '\''
    role_status_list = query.select(sql, ['role_id', 'vote_status', 'role_name', 'user_name'])
    return role_status_list


def action_role_vote(exp, node_id, path, role_id, status):
    """
    实验投票
    :param exp: 实验
    :param node_id: 环节id
    :param path_id 路径id
    :param role_id 角色id
    :param status 投票状态
    :return:
    """
    try:
        if path.vote_status == 2:
            return False, code.get_msg(code.EXPERIMENT_ROLE_VOTE_IS_END)

        exists = ExperimentRoleStatus.objects.filter(experiment_id=exp.pk, node_id=node_id,
                                                     path_id=path.pk, role_id=role_id, vote_status=0).exists()
        if not exists:
            return False, code.get_msg(code.EXPERIMENT_ROLE_HAS_VOTE)

        ExperimentRoleStatus.objects.filter(experiment_id=exp.pk, node_id=node_id, path_id=path.pk,
                                            role_id=role_id).update(vote_status=status)

        has_vote = ExperimentRoleStatus.objects.filter(experiment_id=exp.pk, node_id=node_id,
                                                       path_id=path.pk, role_id=role_id, vote_status=0).exists()
        opt = {
            'role_status_list': action_roles_vote_status(exp, node_id, path),
            'has_vote': False if has_vote else True,
            'end_vote': False
        }
        return True, opt

    except Exception as e:
        logger.exception(u'action_role_vote Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def action_role_vote_end(exp, node_id, path):
    """
    实验投票
    :param exp: 实验
    :param node_id: 环节id
    :param path_id 路径id
    :return:
    """
    try:
        path.vote_status = 2
        path.save()
        opt = {
            'role_status_list': action_roles_vote_status(exp, node_id, path), 'end_vote': True
        }
        return True, opt

    except Exception as e:
        logger.exception(u'action_role_vote_end Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def action_role_request_sign(exp, node_id, data):
    """
    要求签字
    :param exp: 实验
    :param data
    :return:
    """
    try:
        obj = ExperimentDocSign.objects.filter(experiment_id=exp.pk, node_id=node_id, role_id=data['role_id'],
                                               doc_id=data['doc_id']).first()
        if obj:
            return False, code.get_msg(code.EXPERIMENT_HAS_REQUEST_SIGN_ERROR)
        else:
            ExperimentDocSign.objects.create(experiment_id=exp.pk, node_id=node_id, role_id=data['role_id'],
                                             doc_id=data['doc_id'])

        doc = ExperimentDoc.objects.filter(id=data['doc_id']).first()
        opt = {"doc_id": doc.pk, "doc_name": doc.filename, 'url': doc.file.url, 'file_type': doc.file_type,
               "role_id": data['role_id'], "role_name": data['role_name']}
        return True, opt
    except Exception as e:
        logger.exception(u'action_role_request_sign Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def action_role_sign(exp, sign, node_id, role_id, data):
    """
    签字msg_id, doc_id, doc_name,
    :param exp: 实验
    :param data
    :return:
    """
    try:
        if 'msg_id' in data.keys():
            ExperimentMessage.objects.filter(pk=data['msg_id']).update(opt_status=True)

        ExperimentDocSign.objects.filter(experiment_id=exp.pk, node_id=node_id, role_id=role_id,
                                         doc_id=data['doc_id']).update(sign=sign, sign_status=data['result'])
        opt = {
            'doc_id': data['doc_id'], 'doc_name': data['doc_name'], 'name': sign, 'result': data['result']
        }
        return True, opt
    except Exception as e:
        logger.exception(u'action_role_sign Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def action_role_schedule_report(exp, node_id, path_id, data):
    """
    安排报告
    :param exp: 实验
    :param node_id: 环节id
    :param path_id 路径id
    :param role_id 角色id
    :return:
    """
    try:
        # 判断是否有报告席
        node = FlowNode.objects.filter(pk=exp.node_id, del_flag=0).first()
        position = FlowPosition.objects.filter(process=node.process, type=const.SEAT_REPORT_TYPE).first()
        if position is None:
            return False, code.get_msg(code.EXPERIMENT_ROLE_REPORT_ERROR)

        # 占位状态
        ExperimentPositionStatus.objects.update_or_create(experiment_id=exp.id, node_id=node_id,
                                                          path_id=path_id, position_id=position.pk)
        # 报告状态
        ExperimentReportStatus.objects.update_or_create(experiment_id=exp.pk, node_id=node_id, path_id=path_id,
                                                        role_id=data['role_id'], position_id=position.pk,
                                                        defaults={'schedule_status': const.SCHEDULE_OK_STATUS})
        opt = {
            'role_id': data['role_id'], 'role_name': data['role_name'], 'schedule_status': const.SCHEDULE_OK_STATUS,
            'up_btn_status': const.FALSE, 'down_btn_status': const.FALSE
        }
        return True, opt

    except Exception as e:
        logger.exception(u'action_role_schedule_report Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def action_role_toward_report(exp, node_id, path_id, role, pos):
    """
    走向发言席：
    1、判断场景报告席是否配置正确；
    2、判断报告席占位是否占用；
    3、判断是否安排了发言；
    4、角色如以入席，修改占位和入席状态，修改报告席状态，未入席直接修改报告席状态；
    5、结果消息：动画cmd，报告席状态，报告按钮状态；
    :param exp: 实验
    :param node_id: 环节id
    :param path_id 路径id
    :param role_id 角色id
    :return:
    """
    try:
        logger.info('exp.id:%s,node_id:%s,path_id:%s,role_id:%s,position_id:%s' % (exp.pk, node_id, path_id, role.id,
                                                                                   pos['position_id']))
        # 1判断是否有报告席
        node = FlowNode.objects.filter(pk=exp.node_id, del_flag=0).first()
        report_pos = FlowPosition.objects.filter(process=node.process, type=const.SEAT_REPORT_TYPE).first()
        if report_pos is None:
            return False, code.get_msg(code.EXPERIMENT_ROLE_REPORT_ERROR)
        report_position = {'id': report_pos.id, 'position': report_pos.position,
                           'code_position': report_pos.code_position}

        origin_position = {'id': pos['position_id'], 'position': pos['position'],
                           'code_position': pos['code_position']}

        # 2判断报告席占位是否占用
        report_position_status = ExperimentPositionStatus.objects.filter(experiment_id=exp.pk, node_id=node_id,
                                                                         path_id=path_id,
                                                                         position_id=report_pos.pk).first()
        if report_position_status is None:
            return False, code.get_msg(code.EXPERIMENT_ROLE_REPORT_ERROR)

        if report_position_status.sitting_status == const.SITTING_DOWN_STATUS:
            return False, code.get_msg(code.EXPERIMENT_POSITION_HAS_USE)

        # 3判断是否安排了发言；
        report_status = ExperimentReportStatus.objects.filter(experiment_id=exp.pk, node_id=node_id, path_id=path_id,
                                                              role_id=role.pk).first()
        if report_status is None or report_status.schedule_status == const.SCHEDULE_INIT_STATUS:
            return False, code.get_msg(code.EXPERIMENT_ROLE_REPORT_SCHEDULE_ERROR)
        if report_status.schedule_status == const.SCHEDULE_UP_STATUS:
            return False, code.get_msg(code.EXPERIMENT_ROLE_HAS_IN_POSITION)

        # 修改状态为已上位
        report_status.schedule_status = const.SCHEDULE_UP_STATUS
        report_status.save()

        # 4角色如以入席，修改占位和入席状态，修改报告席状态，未入席直接修改报告席状态；
        # 角色状态
        role_status = ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                          role_id=role.id).first()

        ExperimentPositionStatus.objects.update_or_create(experiment_id=exp.id, node_id=node_id,
                                                          path_id=path_id, position_id=pos['position_id'])
        # 原席位判断，如果当前角色入席原席位，如果其他角色入席原席位
        origin_position_status = ExperimentPositionStatus.objects.filter(experiment_id=exp.pk, node_id=node_id,
                                                                         path_id=path_id,
                                                                         position_id=pos['position_id']).first()

        origin_position['sitting_status'] = origin_position_status.sitting_status
        origin_position['is_self'] = False
        if origin_position_status.role_id == role.pk:
            origin_position['is_self'] = True

        if role_status.sitting_status == const.SITTING_DOWN_STATUS:
            # 已入席修改原席位占位状态，退席
            ExperimentPositionStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                    position_id=pos['position_id']).update(sitting_status=const.SITTING_UP_STATUS,
                                                                                           role_id=None)

        role_status.stand_status = 2
        role_status.sitting_status = 2
        role_status.come_status = 2
        role_status.save()

        # 报告席状态为已入席
        ExperimentPositionStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                position_id=report_pos.id).update(sitting_status=const.SITTING_DOWN_STATUS,
                                                                                  role_id=role.pk)

        image = RoleImage.objects.filter(pk=role.image_id).first()
        qs_files = RoleImageFile.objects.filter(image=image)
        actors = []
        if report_pos.actor1:
            actor1 = qs_files.filter(direction=report_pos.actor1).first()
            actors.append(('/media/' + actor1.file.name) if actor1 and actor1.file else '')
        if report_pos.actor2:
            actor2 = qs_files.filter(direction=report_pos.actor2).first()
            actors.append(('/media/' + actor2.file.name) if actor2 and actor2.file else '')

        role_info = {
            'role_id': role_status.role_id, 'user': user_simple_info(role_status.user_id),
            'come_status': role_status.come_status, 'sitting_status': role_status.sitting_status,
            'stand_status': role_status.stand_status,
            'origin_position': origin_position, 'report_position': report_position,
            'up_btn_status': const.FALSE, 'down_btn_status': const.TRUE,
            'actors': actors, 'animate_cmd': u'cmd=trans&transname=走向发言席',
            'gender': image.gender if image else 1
        }
        return True, role_info
    except Exception as e:
        logger.exception(u'action_role_toward_report Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def action_role_end_report(exp, node_id, path_id, role, pos):
    """
    走下发言席
    :param exp: 实验
    :param node_id: 环节id
    :param path_id 路径id
    :param role_id 角色id
    :return:
    """
    try:
        # 原占位
        origin_pos = FlowPosition.objects.filter(pk=pos['org_position_id']).first()
        origin_position = {'id': origin_pos.id, 'position': origin_pos.position,
                           'code_position': origin_pos.code_position}
        report_position = {'id': pos['position_id'], 'position': pos['position'],
                           'code_position': pos['code_position']}

        # 2判断是否安排了发言；
        report_status = ExperimentReportStatus.objects.filter(experiment_id=exp.pk, node_id=node_id, path_id=path_id,
                                                              role_id=role.pk).first()
        if report_status is None or report_status.schedule_status != const.SCHEDULE_UP_STATUS:
            return False, code.get_msg(code.EXPERIMENT_ROLE_REPORT_SCHEDULE_ERROR)
        report_status.schedule_status = const.SCHEDULE_INIT_STATUS
        report_status.save()

        # 3角色如以入席，修改占位和入席状态，修改报告席状态，未入席直接修改报告席状态；
        # 修改原席位占位状态，入席, 判断原席位是否被其他角色占用
        origin_position_use = ExperimentPositionStatus.objects.filter(experiment_id=exp.id, node_id=node_id,
                                                                      path_id=path_id, position_id=origin_pos.id,
                                                                      sitting_status=const.SITTING_DOWN_STATUS).exists()
        if origin_position_use:
            ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                role_id=role.id).update(stand_status=2, sitting_status=1, come_status=2)
        else:
            ExperimentPositionStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                    position_id=origin_pos.id).update(
                sitting_status=const.SITTING_DOWN_STATUS, role_id=role.id)

            ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                role_id=role.id).update(stand_status=2, sitting_status=2, come_status=2)

        # 报告席状态为已退席
        ExperimentPositionStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                position_id=pos['position_id']).update(sitting_status=const.SITTING_UP_STATUS,
                                                                                       role_id=None)

        role_status = ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node_id, path_id=path_id,
                                                          role_id=role.id).first()
        image = RoleImage.objects.filter(pk=role.image_id).first()
        qs_files = RoleImageFile.objects.filter(image=image)
        actors = []
        if origin_pos.actor1:
            actor1 = qs_files.filter(direction=origin_pos.actor1).first()
            actors.append(('/media/' + actor1.file.name) if actor1 and actor1.file else '')
        if origin_pos.actor2:
            actor2 = qs_files.filter(direction=origin_pos.actor2).first()
            actors.append(('/media/' + actor2.file.name) if actor2 and actor2.file else '')

        role_info = {
            'role_id': role_status.role_id, 'user': user_simple_info(role_status.user_id),
            'come_status': role_status.come_status, 'sitting_status': role_status.sitting_status,
            'stand_status': role_status.stand_status,
            'up_btn_status': const.FALSE, 'down_btn_status': const.FALSE,
            'origin_position': origin_position, 'report_position': report_position,
            'actors': actors, 'gender': image.gender if image else 1
        }
        return True, role_info
    except Exception as e:
        logger.exception(u'action_role_end_report Exception:{}'.format(str(e)))
        resp = code.get_msg(code.SYSTEM_ERROR)
        return False, resp


def action_roles_exit(exp, node, path_id, user_id):
    """
    送出
    :return:
    """
    try:
        with transaction.atomic():
            qs = ExperimentRoleStatus.objects.filter(experiment_id=exp.id, node_id=node.pk, path_id=path_id,
                                                     user_id=user_id, sitting_status=2)

            # 报告席
            report_pos = FlowPosition.objects.filter(process=node.process, type=const.SEAT_REPORT_TYPE).first()

            role_list = []
            for item in qs:
                role = ProjectRole.objects.get(pk=item.role_id)
                report_exists = ExperimentReportStatus.objects.filter(experiment_id=exp.pk, node_id=node.pk,
                                                                      path_id=path_id, role_id=role.pk,
                                                                      schedule_status=const.SCHEDULE_UP_STATUS).exists()
                if report_exists:
                    ExperimentReportStatus.objects.filter(experiment_id=exp.pk, node_id=node.pk,
                                                          path_id=path_id, role_id=role.pk,
                                                          schedule_status=const.SCHEDULE_UP_STATUS).update(
                        schedule_status=const.SCHEDULE_INIT_STATUS)

                    pos = report_pos
                else:
                    role_position = FlowRolePosition.objects.filter(node_id=node.pk, role_id=role.flow_role_id).first()
                    if role_position:
                        pos = FlowPosition.objects.filter(pk=role_position.position_id).first()

                # 占位状态更新
                ExperimentPositionStatus.objects.filter(experiment_id=exp.id, node_id=node.pk, path_id=path_id,
                                                        position_id=pos.id).update(sitting_status=1, role_id=None)
                role_list.append({
                    'id': role.id, 'name': role.name, 'code_position': pos.code_position if pos else ''
                })
            qs.update(come_status=1, sitting_status=1, stand_status=2)
        return True, role_list
    except Exception as e:
        logger.exception(u'action_roles_exit Exception:{}'.format(str(e)))
        return False, str(e)


def get_roles_status_simple_by_user(exp, node, path, user_id):
    """
    当前用户可选角色
    """
    prefix = '%s:%s:%s:%s' % (exp.pk, node.pk, path.pk, user_id)
    key = tools.make_key(const.CACHE_ROLES_STATUS_SIMPLE_BY_USER, prefix, 1)
    set_cache_keys(exp.pk, key)
    data = cache.get(key)
    if data:
        return data
    else:
        role_list = ExperimentRoleStatus.objects.filter(experiment_id=exp.pk, node_id=node.pk,
                                                        path_id=path.pk,
                                                        user_id=user_id).values('role_id', 'sitting_status')
        data = list(role_list)
        cache.set(key, data)
        return data


def get_roles_status_by_user(exp, path, user_id):
    """
    当前用户可选角色
    """
    prefix = '%s:%s:%s:%s' % (exp.pk, path.node_id, path.pk, user_id)
    key = tools.make_key(const.CACHE_ROLES_STATUS_BY_USER, prefix, 1)
    set_cache_keys(exp.pk, key)
    data = cache.get(key)
    if data:
        return data
    else:
        # 当前用户可选角色
        sql = '''SELECT r.id,t.come_status,t.sitting_status,t.stand_status,t.vote_status,
                t.show_status,t.speak_times,r.`name`,i.avatar from t_experiment_role_status t
                LEFT JOIN t_project_role r ON t.role_id=r.id
                LEFT JOIN t_role_image i ON i.id=r.image_id
                WHERE t.experiment_id=%s and t.node_id=%s and t.path_id=%s and t.user_id=%s''' % (exp.pk, path.node_id,
                                                                                                  path.pk, user_id)
        logger.info(sql)
        role_list = query.select(sql, ['id', 'come_status', 'sitting_status', 'stand_status',
                                       'vote_status', 'show_status', 'speak_times', 'name', 'avatar'])
        for i in range(0, len(role_list)):
            # 是否有结束环节的权限
            role_perm = ProjectRoleAllocation.objects.filter(project_id=exp.cur_project_id, node_id=path.node_id,
                                                             role_id=role_list[i]['id']).first()
            can_terminate = False
            can_edit = False
            if role_perm:
                can_edit = True
                can_terminate = role_perm.can_terminate

            role_list[i]['can_terminate'] = can_terminate
            role_list[i]['can_edit'] = can_edit
            role_list[i]['avatar'] = '/media/%s' % role_list[i]['avatar']
            role_list[i]['code_position'] = ''
            if path.control_status != 2:
                role_list[i]['speak_times'] = 0

        cache.set(key, role_list)
        return role_list

# def get_without_node_user_roles(exp, user_id):
#     """
#     当前用户可选角色
#     """
#     return role_list


def get_all_simple_roles_status(exp, node, path):
    """
    所有角色
    """
    key = tools.make_key(const.CACHE_ALL_SIMPLE_ROLES_STATUS, '%s:%s:%s' % (exp.pk, node.pk, path.pk), 1)
    set_cache_keys(exp.pk, key)
    data = cache.get(key)
    if data:
        return data
    else:
        sql = '''SELECT t.role_id,t.come_status,t.sitting_status,t.stand_status,t.vote_status,
            t.show_status,t.speak_times,r.`name` role_name,u.`name` user_name from t_experiment_role_status t
            LEFT JOIN t_project_role r ON t.role_id=r.id
            LEFT JOIN t_user u ON t.user_id=u.id
            WHERE t.experiment_id=%s and t.node_id=%s and t.path_id=%s''' % (exp.pk, node.pk, path.pk)
        logger.info(sql)
        role_status_list = query.select(sql, ['role_id', 'come_status', 'sitting_status', 'stand_status',
                                              'vote_status', 'show_status', 'speak_times', 'role_name', 'user_name'])
        cache.set(key, role_status_list)
        return role_status_list


def get_all_roles_status(exp, project, node, path):
    """
    所有角色
    """
    key = tools.make_key(const.CACHE_ALL_ROLES_STATUS, '%s:%s:%s' % (exp.pk, node.pk, path.pk), 1)
    set_cache_keys(exp.pk, key)
    data = cache.get(key)
    if data:
        return data
    else:
        # 报告席
        report_pos = FlowPosition.objects.filter(process=node.process, type=const.SEAT_REPORT_TYPE).first()
        report_status = ExperimentReportStatus.objects.filter(experiment_id=exp.pk, node_id=node.pk,
                                                              path_id=path.pk,
                                                              schedule_status=const.SCHEDULE_UP_STATUS).first()

        sql = '''SELECT t.role_id,t.come_status,t.sitting_status,t.stand_status,t.vote_status,
                t.show_status,t.speak_times,r.`name` role_name,r.flow_role_id,u.name,r.image_id,i.gender
                from t_experiment_role_status t
                LEFT JOIN t_project_role r ON t.role_id=r.id
                LEFT JOIN t_user u ON t.user_id=u.id
                LEFT JOIN t_role_image i ON i.id=r.image_id
                WHERE t.experiment_id=%s and t.node_id=%s and t.path_id=%s''' % (exp.pk, node.pk, path.pk)
        sql += ' order by t.sitting_status '
        logger.info(sql)
        role_list = query.select(sql, ['role_id', 'come_status', 'sitting_status', 'stand_status',
                                       'vote_status', 'show_status', 'speak_times', 'role_name', 'flow_role_id',
                                       'user_name', 'image_id', 'gender'])
        for i in range(0, len(role_list)):
            role_position = FlowRolePosition.objects.filter(flow_id=project.flow_id, node_id=node.pk,
                                                            role_id=role_list[i]['flow_role_id']).first()
            actors = []
            if role_position:
                qs_files = RoleImageFile.objects.filter(image_id=role_list[i]['image_id'])
                if report_pos and report_status:
                    if role_list[i]['role_id'] == report_status.role_id:
                        if report_pos.actor1:
                            actor1 = qs_files.filter(direction=report_pos.actor1).first()
                            actors.append(('/media/' + actor1.file.name) if actor1 and actor1.file else '')
                        if report_pos.actor2:
                            actor2 = qs_files.filter(direction=report_pos.actor2).first()
                            actors.append(('/media/' + actor2.file.name) if actor2 and actor2.file else '')
                        position = {'id': report_pos.id, 'position': report_pos.position,
                                    'code_position': report_pos.code_position}
                    else:
                        pos = FlowPosition.objects.filter(pk=role_position.position_id).first()
                        if pos:
                            if pos.actor1:
                                actor1 = qs_files.filter(direction=pos.actor1).first()
                                actors.append(('/media/' + actor1.file.name) if actor1 and actor1.file else '')
                            if pos.actor2:
                                actor2 = qs_files.filter(direction=pos.actor2).first()
                                actors.append(('/media/' + actor2.file.name) if actor2 and actor2.file else '')
                            position = {'id': pos.id, 'position': pos.position, 'code_position': pos.code_position}
                        else:
                            position = None
                else:
                    pos = FlowPosition.objects.filter(pk=role_position.position_id).first()
                    if pos:
                        if pos.actor1:
                            actor1 = qs_files.filter(direction=pos.actor1).first()
                            actors.append(('/media/' + actor1.file.name) if actor1 and actor1.file else '')
                        if pos.actor2:
                            actor2 = qs_files.filter(direction=pos.actor2).first()
                            actors.append(('/media/' + actor2.file.name) if actor2 and actor2.file else '')
                        position = {'id': pos.id, 'position': pos.position, 'code_position': pos.code_position}
                    else:
                        position = None
            else:
                position = None
            role_list[i]['position'] = position
            role_list[i]['actors'] = actors
        cache.set(key, role_list)
        return role_list


def get_role_process_actions(exp, path, role_id, process_action_ids):
    """
    当前角色动画
    """
    prefix = '%s:%s:%s' % (exp.pk, path.pk, role_id)
    key = tools.make_key(const.CACHE_ROLE_PROCESS_ACTIONS, prefix, 1)
    set_cache_keys(exp.pk, key)
    data = cache.get(key)
    if data:
        return data
    else:
        process_actions = ProcessAction.objects.filter(id__in=process_action_ids,
                                                       del_flag=0).values('id', 'name', 'cmd')

        data = list(process_actions)
        cache.set(key, data)
        return data


def get_experiment_path(exp):
    """
    实验流程路径
    """
    key = tools.make_key(const.CACHE_EXPERIMENT_PATH, exp.pk, 1)
    set_cache_keys(exp.pk, key)
    data = cache.get(key)
    if data:
        return data
    else:
        paths = ExperimentTransPath.objects.filter(experiment_id=exp.id)
        data = []
        for item in paths:
            node = FlowNode.objects.filter(pk=item.node_id, del_flag=0).first()
            data.append({'path_id': item.id, 'node_id': item.node_id, 'process_type': node.process.type,
                         'node_name': node.name})
        cache.set(key, data)
        return data


def get_node_docs(exp, node_id, project_id):
    """
    获取该环节项目所有素材
    """
    prefix = '%s:%s:%s' % (exp.pk, project_id, node_id)
    key = tools.make_key(const.CACHE_NODE_DOCS, prefix, 1)
    set_cache_keys(exp.pk, key)
    data = cache.get(key)
    if data:
        logger.info('key:%s' % key)
        return data
    else:
        # 获取该环节所有素材id
        doc_ids = list(ProjectDocRole.objects.filter(project_id=project_id,
                                                     node_id=node_id).values_list('doc_id', flat=True))

        project_doc_list = []
        operation_guide_list = []
        project_tips_list = []

        if doc_ids:
            doc_ids = list(set(doc_ids))
            # 角色项目素材
            project_docs = ProjectDoc.objects.filter(id__in=doc_ids)
            for d in project_docs:
                if d.usage in [2, 3, 4, 5]:
                    project_doc_list.append({
                        'id': d.id, 'name': d.name, 'type': d.type, 'usage': d.usage,
                        'content': d.content, 'url': d.file.url, 'file_type': d.file_type
                    })
                elif d.usage == 1:
                    operation_guide_list.append({
                        'id': d.id, 'name': d.name, 'type': d.type, 'usage': d.usage,
                        'content': d.content, 'url': d.file.url, 'file_type': d.file_type
                    })
                elif d.usage == 7:
                    project_tips_list.append({
                        'id': d.id, 'name': d.name, 'type': d.type, 'usage': d.usage,
                        'content': d.content, 'url': d.file.url, 'file_type': d.file_type
                    })
        data = {
            'operation_guides': operation_guide_list,
            'project_tips_list': project_tips_list,
            'project_docs': project_doc_list,
            'id': exp.id, 'name': exp.name
        }
        cache.set(key, data)
        return data


def get_node_role_docs(exp, node_id, project_id, flow_id, role_id):
    """
    获取该环节角色项目所有素材
    """
    prefix = '%s:%s:%s:%s' % (exp.pk, project_id, node_id, role_id)
    key = tools.make_key(const.CACHE_NODE_ROLE_DOCS, prefix, 1)
    set_cache_keys(exp.pk, key)
    data = None  # cache.get(key)
    if data:
        logger.info('key:%s' % key)
        return data
    else:
        # 角色项目素材
        cur_doc_list = []
        operation_guide_list = []
        project_tips_list = []

        # 流程素材，对所有角色
        doc_ids = FlowNodeDocs.objects.filter(flow_id=flow_id, node_id=node_id, del_flag=0).values_list('doc_id',
                                                                                                        flat=True)
        logger.info("-------------------------")
        logger.info(doc_ids)
        if doc_ids:
            node_docs = FlowDocs.objects.filter(id__in=doc_ids, usage__in=(1, 2, 3))
            for item in node_docs:
                url = ''
                if item.file:
                    url = item.file.url
                if item.usage == 1:
                    logger.info(item.name)
                    operation_guide_list.append({
                        'id': item.id, 'name': item.name, 'type': item.type, 'usage': item.usage,
                        'content': item.content,
                        'url': url, 'file_type': item.file_type
                    })
                else:
                    cur_doc_list.append({
                        'id': item.id, 'name': item.name, 'type': item.type, 'usage': item.usage,
                        'content': item.content,
                        'url': url, 'file_type': item.file_type
                    })

        # 获取该环节所有素材id
        # doc_ids = list(ProjectDocRole.objects.filter(project_id=project_id, node_id=node_id,
        #                                              role_id=role_id).values_list('doc_id', flat=True))
        #
        # if doc_ids:
        #     doc_ids = list(set(doc_ids))
        #     project_docs = ProjectDoc.objects.filter(id__in=doc_ids)
        #     for item in project_docs:
        #         url = ''
        #         if item.file:
        #             url = item.file.url
        #         if item.usage in [2, 3, 4, 5]:
        #             cur_doc_list.append({
        #                 'id': item.id, 'name': item.name, 'type': item.type, 'usage': item.usage, 'content': item.content,
        #                 'url': url, 'file_type': item.file_type
        #             })
        #         elif item.usage == 1:
        #             operation_guide_list.append({
        #                 'id': item.id, 'name': item.name, 'type': item.type, 'usage': item.usage, 'content': item.content,
        #                 'url': url, 'file_type': item.file_type
        #             })
        #         elif item.usage == 7:
        #             project_tips_list.append({
        #                 'id': item.id, 'name': item.name, 'type': item.type, 'usage': item.usage, 'content': item.content,
        #                 'url': url, 'file_type': item.file_type
        #             })
        data = {'cur_doc_list': cur_doc_list, 'operation_guides': operation_guide_list,
                'project_tips_list': project_tips_list}
        cache.set(key, data)
        return data


def get_pre_node_role_docs(exp, node_id, project_id, role_id):
    """
    前面所有环节素材
    """
    prefix = '%s:%s:%s:%s' % (exp.pk, node_id, project_id, role_id)
    key = tools.make_key(const.CACHE_PRE_NODE_ROLE_DOCS, prefix, 1)
    set_cache_keys(exp.pk, key)
    data = cache.get(key)
    if data:
        logger.info('key:%s' % key)
        return data
    else:
        data = []
        node_ids = list(ExperimentTransPath.objects.filter(experiment_id=exp.id).values_list('node_id', flat=True))
        if node_ids:
            node_ids.remove(exp.node_id)
            # logger.info(node_ids)
            doc_ids = ProjectDocRole.objects.filter(project_id=project_id, node_id__in=node_ids,
                                                    role_id=role_id).values_list('doc_id', flat=True)
            project_docs = ProjectDoc.objects.filter(id__in=doc_ids)
            for item in project_docs:
                if item.usage in [2, 3, 4, 5, 7]:
                    data.append({
                        'id': item.id, 'name': item.name, 'type': item.type, 'usage': item.usage,
                        'content': item.content, 'url': item.file.url, 'file_type': item.file_type
                    })
        cache.set(key, data)
        return data


def get_experiment_display_files(exp, node_id, path_id):
    """
    实验文件展示列表
    """
    doc_list = []
    if node_id:
        key = tools.make_key(const.CACHE_EXPERIMENT_FILE_DISPLAY, '%s:%s:%s' % (exp.pk, node_id, path_id), 1)
        set_cache_keys(exp.pk, key)
        data = cache.get(key)
        if data:
            return data
        else:
            node = FlowNode.objects.filter(pk=node_id).first()
            if node.process.type == 2:
                # 如果是编辑
                # 应用模板
                docs = ExperimentDocContent.objects.filter(experiment_id=exp.pk, node_id=node_id, has_edited=True)
                for d in docs:
                    r = tools.generate_code(6)
                    doc_list.append({
                        'id': d.doc_id, 'filename': d.name, 'content': d.content, 'file_type': d.file_type,
                        'signs': [{'sign_status': d.sign_status, 'sign': d.sign}],
                        'url': '{0}?{1}'.format(d.file.url, r) if d.file else None,
                        'allow_delete': False
                    })

                # 提交的文件
                docs = ExperimentDoc.objects.filter(experiment_id=exp.pk, node_id=node_id, path_id=path_id)
                for d in docs:
                    sign_list = ExperimentDocSign.objects.filter(doc_id=d.pk).values('sign', 'sign_status')
                    doc_list.append({
                        'id': d.id, 'filename': d.filename, 'content': d.content, 'file_type': d.file_type,
                        'signs': list(sign_list), 'url': d.file.url if d.file else None,
                        'allow_delete': True
                    })

            elif node.process.type == 3:
                # 如果是展示
                # 获取该环节所有素材id
                doc_ids = list(ProjectDocRole.objects.filter(project_id=exp.project_id,
                                                             node_id=node_id).values_list('doc_id', flat=True))

                if doc_ids:
                    doc_ids = list(set(doc_ids))

                # 角色项目素材
                project_docs = ProjectDoc.objects.filter(id__in=doc_ids, usage=4)
                for item in project_docs:
                    doc_list.append({
                        'id': item.id, 'filename': item.name, 'url': item.file.url, 'content': item.content,
                        'file_type': item.file_type, 'has_edited': False, 'signs': [],
                        'experiment_id': exp.pk, 'node_id': node.pk, 'created_by': None,
                        'role_name': '', 'node_name': node.name if node else None,
                        'allow_delete': False
                    })

                # 提交的文件
                docs = ExperimentDoc.objects.filter(experiment_id=exp.pk, node_id=node_id, path_id=path_id)
                for d in docs:
                    doc_list.append({
                        'id': d.id, 'filename': d.filename, 'content': d.content, 'file_type': d.file_type,
                        'node_id': node.pk, 'created_by': None, 'experiment_id': exp.pk,
                        'role_name': '', 'node_name': node.name if node else None,
                        'has_edited': False, 'signs': [], 'url': d.file.url if d.file else None,
                        'allow_delete': True
                    })

                # 若为模版，判断是否已经编辑
                docs = ExperimentDocContent.objects.filter(experiment_id=exp.pk, node_id=node_id, has_edited=True)
                for d in docs:
                    r = tools.generate_code(6)
                    doc_list.append({
                        'id': d.doc_id, 'filename': d.name, 'content': d.content,
                        'url': '{0}?{1}'.format(d.file.url, r) if d.file else None, 'file_type': d.file_type,
                        'has_edited': d.has_edited, 'experiment_id': exp.pk, 'node_id': node.pk, 'created_by': None,
                        'role_name': '', 'node_name': node.name if node else None,
                        'signs': [{'sign_status': d.sign_status, 'sign': d.sign}],
                    })
            else:
                # 环节路径上传文件
                exp_docs = ExperimentDoc.objects.filter(experiment_id=exp.pk, node_id=node_id, path_id=path_id)
                for item in exp_docs:
                    node = FlowNode.objects.filter(pk=item.node_id).first()
                    role = ProjectRole.objects.filter(pk=item.role_id).first()
                    sign_list = ExperimentDocSign.objects.filter(doc_id=item.pk).values('sign', 'sign_status')
                    doc = {
                        'id': item.id, 'filename': item.filename, 'url': item.file.url if item.file else None,
                        'experiment_id': item.experiment_id, 'node_id': item.node_id, 'content': item.content,
                        'created_by': user_simple_info(item.created_by), 'role_name': role.name if role else '',
                        'signs': list(sign_list), 'node_name': node.name if node else None,
                        'file_type': item.file_type
                    }
                    doc_list.append(doc)
            cache.set(key, doc_list)
    else:
        key = tools.make_key(const.CACHE_EXPERIMENT_FILE_DISPLAY, exp.pk, 1)
        set_cache_keys(exp.pk, key)
        data = cache.get(key)
        if data:
            return data
        else:
            # 已提交文件(不传node_id和path_id)：显示出实验环节中所有上传文件
            exp_docs = ExperimentDoc.objects.filter(experiment_id=exp.pk)
            for item in exp_docs:
                node = FlowNode.objects.filter(pk=item.node_id).first()
                sign_list = ExperimentDocSign.objects.filter(doc_id=item.pk).values('sign', 'sign_status')
                doc = {
                    'id': item.id, 'filename': item.filename, 'url': item.file.url if item.file else None,
                    'experiment_id': item.experiment_id, 'node_id': item.node_id, 'content': item.content,
                    'created_by': user_simple_info(item.created_by), 'role_name': '',
                    'signs': list(sign_list), 'node_name': node.name if node else None,
                    'file_type': item.file_type
                }
                doc_list.append(doc)

            docs = ExperimentDocContent.objects.filter(experiment_id=exp.pk, has_edited=True)
            for item in docs:
                r = tools.generate_code(6)
                node = FlowNode.objects.filter(pk=item.node_id).first()
                doc_list.append({
                    'id': item.doc_id, 'filename': item.name, 'content': item.content,
                    'experiment_id': item.experiment_id, 'node_id': item.node_id, 'file_type': item.file_type,
                    'created_by': user_simple_info(item.created_by), 'role_name': '',
                    'node_name': node.name if node else None,
                    'signs': [{'sign_status': item.sign_status, 'sign': item.sign}],
                    'url': '{0}?{1}'.format(item.file.url, r) if item.file else None
                })
            cache.set(key, doc_list)
    return doc_list


def get_experiment_templates(exp, node_id, role_id, usage):
    doc_list = []
    try:

        """
        实验模板
        """
        if usage and usage == '3':
            docs = ExperimentDocContent.objects.filter(experiment_id=exp.pk, node_id=node_id, role_id=role_id)
            for item in docs:
                doc_list.append({
                    'id': item.id, 'name': item.name, 'type': '', 'usage': 3,
                    'content': item.content, 'file_type': item.file_type,
                    'has_edited': item.has_edited, 'from': 1,
                    'sign_status': item.sign_status, 'sign': item.sign,
                    'role_id': item.role_id, 'url': item.file.url
                })
        else:
            logger.info('====================')
            logger.info(role_id)
            if role_id:
                doc_ids = ProjectDocRole.objects.filter(project_id=exp.cur_project_id, node_id=node_id,
                                                        role_id=role_id).values_list('doc_id', flat=True)
            else:
                doc_ids = ProjectDocRole.objects.filter(project_id=exp.cur_project_id,
                                                        node_id=node_id).values_list('doc_id', flat=True)

            qs = ProjectDoc.objects.filter(project_id=exp.cur_project_id)
            if usage:
                qs = qs.filter(usage=usage)
            if node_id:
                qs = qs.filter(id__in=doc_ids)
            for item in qs:
                doc_list.append({
                    'id': item.id, 'name': item.name, 'type': item.type, 'usage': item.usage,
                    'content': item.content, 'file_type': item.file_type,
                    'has_edited': False, 'from': 1,
                    'sign_status': 0,
                    'sign': '',
                    'role_id': None,
                    'url': item.file.url
                })

            # 三期改bug增加------流程素材，对所有角色----------我也不知道对不对 测试说要加我就加了呗
            # 一会儿流程素材一会儿项目素材的
            # 我也搞不懂了，这几行代码还是先注掉吧
            doc_ids = FlowNodeDocs.objects.filter(node_id=node_id, del_flag=0).values_list('doc_id', flat=True)
            if doc_ids:
                node_docs = FlowDocs.objects.filter(id__in=doc_ids, usage=usage)
                for item in node_docs:
                    url = ''
                    if item.file:
                        url = item.file.url
                    doc_list.append({
                        'id': item.id, 'name': item.name, 'type': item.type, 'usage': item.usage,
                        'content': item.content, 'file_type': item.file_type,
                        'has_edited': False, 'from': 1,
                        'sign_status': 0,
                        'sign': '',
                        'role_id': None,
                        'url': url
                    })
    except Exception as e:
        logger.exception('api_experiment_message_push Exception:{0}'.format(str(e)))
    return doc_list


def get_experiment_detail(exp):
    """
    实验详情
    """
    key = tools.make_key(const.CACHE_EXPERIMENT_DETAIL, exp.pk, 1)
    set_cache_keys(exp.pk, key)
    data = cache.get(key)

    if data:
        return data
    else:
        course_class = CourseClass.objects.filter(pk=exp.course_class_id).first()
        team = Team.objects.filter(pk=exp.team_id).first()
        project = Project.objects.filter(pk=exp.cur_project_id).first()

        # 课堂信息
        if course_class:
            course_class_dict = {
                'id': course_class.id, 'name': course_class.name, 'time': course_class.time,
                'teacher1': course_class.teacher1.name if course_class.teacher1 else None,
                'teacher2': course_class.teacher2.name if course_class.teacher2 else None,
                'no': course_class.no, 'sort': course_class.sort, 'term': course_class.term,
            }
        else:
            course_class_dict = None

        # 小组信息
        if team:
            team_dict = {
                'id': team.id, 'leader': user_simple_info(team.leader), 'open_join': team.open_join,
                'create_time': team.create_time.strftime('%Y-%m-%d')
            }
        else:
            team_dict = None

        # 项目信息
        if project:
            project_dict = {
                'id': project.id, 'name': project.name
            }
        else:
            project_dict = None

        # 角色分配信息，修改实验信息用
        mr = MemberRole.objects.filter(experiment_id=exp.pk, project_id=project.id, del_flag=0).exists()
        if mr:
            sql = '''SELECT t.id,t.`name`,t.type,m.user_id from t_project_role t
                LEFT JOIN t_member_role m ON t.id=m.role_id
                WHERE m.del_flag=0 and m.experiment_id=%s and m.project_id=%s''' % (exp.pk, project.id)
            logger.info(sql)
            role_list_temp = query.select(sql, ['id', 'name', 'type', 'user_id'])
            # 三期增加， 有些角色没有设置用户的话上面的sql将查不出来
            role_list = []
            roles = ProjectRole.objects.filter(project_id=project.id)
            for item in roles:
                user_id_temp = None
                if const.ROLE_TYPE_OBSERVER != item.type:
                    for temp in role_list_temp:
                        if item.id == temp['id']:
                            user_id_temp = temp['user_id']
                    role_list.append({
                        'id': item.id, 'name': item.name, 'type': item.type, 'user_id': user_id_temp
                    })
        else:
            role_list = []
            roles = ProjectRole.objects.filter(project_id=project.id)
            for item in roles:
                if const.ROLE_TYPE_OBSERVER != item.type:
                    role_list.append({
                        'id': item.id, 'name': item.name, 'type': item.type, 'user_id': None
                    })

        node = FlowNode.objects.filter(pk=exp.node_id).first()
        if node:
            process = node.process
            cur_node = {
                'id': node.id, 'name': node.name, 'condition': node.condition, 'process_type': process.type,
                'can_switch': process.can_switch
            }
        else:
            cur_node = None

        data = {
            'id': exp.id, 'show_nickname': exp.show_nickname, 'entire_graph': project.entire_graph,
            'status': exp.status, 'flow_id': project.flow_id,
            'start_time': exp.start_time.strftime('%Y-%m-%d') if exp.start_time else None,
            'end_time': exp.end_time.strftime('%Y-%m-%d') if exp.end_time else None,
            'create_by': user_simple_info(exp.created_by), 'node_id': exp.node_id,
            'create_time': exp.create_time.strftime('%Y-%m-%d'),
            'course_class': course_class_dict, 'team': team_dict, 'name': u'{0} {1}'.format(exp.id, exp.name),
            'project': project_dict, 'roles': role_list, 'node': cur_node, 'huanxin_id': exp.huanxin_id
        }
        cache.set(key, data)
    return data


def get_role_node_can_terminate(exp, project_id, node_id, role_id):
    """
    是否有结束环节的权限
    """
    prefix = '%s:%s:%s:%s' % (exp.pk, project_id, node_id, role_id)
    key = tools.make_key(const.CACHE_ROLE_NODE_CAN_TERMINATE, prefix, 1)
    set_cache_keys(exp.pk, key)
    try:
        data = cache.get(key)
        if data:
            return data['can_terminate']
        else:
            if ProjectRoleAllocation.objects.filter(project_id=project_id, node_id=node_id, role_id=role_id,
                                                    can_terminate=True).exists():
                can_terminate = True
            else:
                can_terminate = False
            data = {'can_terminate': can_terminate}
            cache.set(key, data)
            return can_terminate
    except Exception as e:
        logger.exception('get_role_node_can_terminate Exception:{0}'.format(str(e)))
        return False


def get_role_image(exp, image_id):
    """
    角色形象
    """
    prefix = '%s:%s' % (exp.pk, image_id)
    key = tools.make_key(const.CACHE_ROLE_IMAGE, prefix, 1)
    set_cache_keys(exp.pk, key)
    try:
        data = cache.get(key)
        if data:
            return data
        else:
            image = RoleImage.objects.filter(pk=image_id).first()
            if image:
                data = {'image_id': image.pk, 'name': image.name, 'gender': image.gender,
                        'avatar': image.avatar.url if image.avatar else ''}
                cache.set(key, data)
                return data
            else:
                return None
    except Exception as e:
        logger.exception('get_role_image Exception:{0}'.format(str(e)))
        return None


def get_role_position(exp, project, node, path, role):
    """
    角色占位
    """
    prefix = '%s:%s:%s:%s' % (exp.pk, project.flow_id, node.pk, role.flow_role_id)
    key = tools.make_key(const.CACHE_ROLE_POSITION, prefix, 1)
    set_cache_keys(exp.pk, key)
    try:
        data = cache.get(key)
        if data:
            return data
        else:
            role_position = FlowRolePosition.objects.filter(flow_id=project.flow_id, node_id=node.pk,
                                                            role_id=role.flow_role_id, del_flag=0).first()
            pos = None
            if role_position:
                pos = FlowPosition.objects.filter(pk=role_position.position_id, del_flag=0).first()

            # 判断是否存在报告席，是否已走向报告
            report_pos = FlowPosition.objects.filter(process=node.process, type=const.SEAT_REPORT_TYPE,
                                                     del_flag=0).first()
            if report_pos:
                report_exists = ExperimentReportStatus.objects.filter(experiment_id=exp.pk, node_id=node.pk,
                                                                      path_id=path.pk, role_id=role.pk,
                                                                      schedule_status=const.SCHEDULE_UP_STATUS).exists()
                if report_exists:
                    pos = report_pos
            if pos:
                data = {'position_id': pos.id, 'org_position_id': role_position.position_id,
                        'code_position': pos.code_position, 'position': pos.position,
                        'actor1': pos.actor1, 'actor2': pos.actor2, 'type': pos.type}
                cache.set(key, data)
                return data
            else:
                return None
    except Exception as e:
        logger.exception('get_role_position Exception:{0}'.format(str(e)))
        return None


def get_node_path_messages(exp, node_id, path_id, is_paging, page, size):
    """
    环节消息
    """
    if is_paging == 1:
        sql = '''SELECT t.id,t.user_id `from`,t.msg_type,t.msg `data`,t.ext,t.file_id,t.opt_status
        from t_experiment_message t WHERE t.experiment_id=%s and t.node_id=%s and t.path_id=%s
        order by timestamp desc''' % (exp.pk, node_id, path_id)
        count_sql = '''SELECT count(t.id) from t_experiment_message t
        WHERE t.experiment_id=%s and t.node_id=%s and t.path_id=%s''' % (exp.pk, node_id, path_id)
        logger.info(sql)
        data = query.pagination_page(sql, ['id', 'from', 'msg_type', 'data', 'ext', 'file_id', 'opt_status'],
                                     count_sql, page, size)
        return data
    else:
        sql = '''SELECT t.id,t.user_id `from`,t.msg_type,t.msg `data`,t.ext,t.file_id,t.opt_status
        from t_experiment_message t WHERE t.experiment_id=%s and t.node_id=%s and t.path_id=%s
        order by timestamp asc''' % (exp.pk, node_id, path_id)
        logger.info(sql)
        data = query.select(sql, ['id', 'from', 'msg_type', 'data', 'ext', 'file_id', 'opt_status'])
        return {'results': data, 'paging': None}
