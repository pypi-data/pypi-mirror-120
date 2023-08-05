#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0OA
#
# Authors:
# - Wen Guan, <wen.guan@cern.ch>, 2019 - 2020


"""
operations related to Requests.
"""

import copy

from idds.common.constants import (RequestStatus, RequestLocking, WorkStatus,
                                   CollectionType, CollectionStatus, CollectionRelationType)
from idds.orm.base.session import read_session, transactional_session
from idds.orm import requests as orm_requests
from idds.orm import transforms as orm_transforms
from idds.orm import workprogress as orm_workprogresses
from idds.orm import collections as orm_collections
from idds.orm import messages as orm_messages
from idds.core import messages as core_messages


def create_request(scope=None, name=None, requester=None, request_type=None,
                   username=None, userdn=None, transform_tag=None,
                   status=RequestStatus.New, locking=RequestLocking.Idle, priority=0,
                   lifetime=None, workload_id=None, request_metadata=None,
                   processing_metadata=None):
    """
    Add a request.

    :param scope: The scope of the request data.
    :param name: The name of the request data.
    :param requestr: The requester, such as panda, user and so on.
    :param request_type: The type of the request, such as ESS, DAOD.
    :param transform_tag: Transform tag, such as ATLAS AMI tag.
    :param status: The request status as integer.
    :param locking: The request locking as integer.
    :param priority: The priority as integer.
    :param lifetime: The life time as umber of days.
    :param workload_id: The external workload id.
    :param request_metadata: The metadata as json.
    :param processing_metadata: The metadata as json.

    :returns: request id.
    """
    if workload_id is None and request_metadata and 'workload_id' in request_metadata:
        workload_id = int(request_metadata['workload_id'])

    # request_metadata = convert_request_metadata_to_workflow(scope, name, workload_id, request_type, request_metadata)
    kwargs = {'scope': scope, 'name': name, 'requester': requester, 'request_type': request_type,
              'username': username, 'userdn': userdn,
              'transform_tag': transform_tag, 'status': status, 'locking': locking,
              'priority': priority, 'lifetime': lifetime, 'workload_id': workload_id,
              'request_metadata': request_metadata, 'processing_metadata': processing_metadata}
    return orm_requests.create_request(**kwargs)


@transactional_session
def add_request(scope=None, name=None, requester=None, request_type=None,
                username=None, userdn=None, transform_tag=None,
                status=RequestStatus.New, locking=RequestLocking.Idle, priority=0,
                lifetime=None, workload_id=None, request_metadata=None,
                processing_metadata=None, session=None):
    """
    Add a request.

    :param scope: The scope of the request data.
    :param name: The name of the request data.
    :param requestr: The requester, such as panda, user and so on.
    :param request_type: The type of the request, such as ESS, DAOD.
    :param transform_tag: Transform tag, such as ATLAS AMI tag.
    :param status: The request status as integer.
    :param locking: The request locking as integer.
    :param priority: The priority as integer.
    :param lifetime: The life time as umber of days.
    :param workload_id: The external workload id.
    :param request_metadata: The metadata as json.
    :param processing_metadata: The metadata as json.

    :returns: request id.
    """
    if workload_id is None and request_metadata and 'workload_id' in request_metadata:
        workload_id = int(request_metadata['workload_id'])
    # request_metadata = convert_request_metadata_to_workflow(scope, name, workload_id, request_type, request_metadata)

    kwargs = {'scope': scope, 'name': name, 'requester': requester, 'request_type': request_type,
              'username': username, 'userdn': userdn,
              'transform_tag': transform_tag, 'status': status, 'locking': locking,
              'priority': priority, 'lifetime': lifetime, 'workload_id': workload_id,
              'request_metadata': request_metadata, 'processing_metadata': processing_metadata,
              'session': session}
    return orm_requests.add_request(**kwargs)


@read_session
def get_request_ids_by_workload_id(workload_id, session=None):
    """
    Get request id or raise a NoObject exception.

    :param workload_id: The workload_id of the request.
    :param session: The database session in use.

    :raises NoObject: If no request is founded.

    :returns: Request ids.
    """
    return orm_requests.get_request_ids_by_workload_id(workload_id, session=session)


@read_session
def get_requests(request_id=None, workload_id=None, with_detail=False, with_processing=False, with_metadata=False, to_json=False, session=None):
    """
    Get a request or raise a NoObject exception.

    :param request_id: The id of the request.
    :param workload_id: The workload_id of the request.
    :param to_json: return json format.

    :raises NoObject: If no request is founded.

    :returns: Request.
    """
    return orm_requests.get_requests(request_id=request_id, workload_id=workload_id,
                                     with_detail=with_detail, with_metadata=with_metadata,
                                     with_processing=with_processing,
                                     to_json=to_json, session=session)


@transactional_session
def extend_requests(request_id=None, workload_id=None, lifetime=30, session=None):
    """
    extend an request's lifetime.

    :param request_id: The id of the request.
    :param workload_id: The workload_id of the request.
    :param lifetime: The life time as umber of days.
    """
    return orm_requests.extend_request(request_id=request_id, workload_id=workload_id, lifetime=lifetime,
                                       session=session)


@transactional_session
def cancel_requests(request_id=None, workload_id=None, session=None):
    """
    cancel an request.

    :param request_id: The id of the request.
    :param workload_id: The workload_id of the request.
    """
    return orm_requests.cancel_request(request_id=request_id, workload_id=workload_id, session=session)


@transactional_session
def update_request(request_id, parameters, session=None):
    """
    update an request.

    :param request_id: the request id.
    :param parameters: A dictionary of parameters.
    """
    return orm_requests.update_request(request_id, parameters, session=session)


def generate_collection(transform, collection, relation_type=CollectionRelationType.Input):
    coll_metadata = collection.coll_metadata

    if 'coll_type' in coll_metadata:
        coll_type = coll_metadata['coll_type']
    else:
        coll_type = CollectionType.Dataset

    if collection.status is None:
        collection.status = CollectionStatus.Open

    coll = {'transform_id': transform['request_id'],
            'request_id': transform['request_id'],
            'workload_id': transform['workload_id'],
            'coll_type': coll_type,
            'scope': collection.scope,
            'name': collection.name,
            'relation_type': relation_type,
            'bytes': coll_metadata['bytes'] if 'bytes' in coll_metadata else 0,
            'total_files': coll_metadata['total_files'] if 'total_files' in coll_metadata else 0,
            'new_files': coll_metadata['new_files'] if 'new_files' in coll_metadata else 0,
            'processed_files': 0,
            'processing_files': 0,
            'coll_metadata': coll_metadata,
            'status': collection.status,
            'expired_at': transform['expired_at'],
            'collection': collection}
    return coll


def generate_collections(transform):
    work = transform['transform_metadata']['work']

    input_collections = work.get_input_collections()
    output_collections = work.get_output_collections()
    log_collections = work.get_log_collections()

    input_colls, output_colls, log_colls = [], [], []
    for input_coll in input_collections:
        in_coll = generate_collection(transform, input_coll, relation_type=CollectionRelationType.Input)
        input_colls.append(in_coll)
    for output_coll in output_collections:
        out_coll = generate_collection(transform, output_coll, relation_type=CollectionRelationType.Output)
        output_colls.append(out_coll)
    for log_coll in log_collections:
        l_coll = generate_collection(transform, log_coll, relation_type=CollectionRelationType.Log)
        log_colls.append(l_coll)
    return input_colls + output_colls + log_colls


@transactional_session
def update_request_with_transforms(request_id, parameters,
                                   new_transforms=None, update_transforms=None,
                                   new_messages=None, update_messages=None, session=None):
    """
    update an request.

    :param request_id: the request id.
    :param parameters: A dictionary of parameters.
    :param new_transforms: list of transforms
    :param update_transforms: list of transforms
    """
    if new_transforms:
        for tf in new_transforms:
            # tf_id = orm_transforms.add_transform(**tf, session=session)
            # original_work = tf['transform_metadata']['original_work']
            # del tf['transform_metadata']['original_work']
            workflow = tf['transform_metadata']['workflow']
            del tf['transform_metadata']['workflow']

            work = tf['transform_metadata']['work']
            tf_copy = copy.deepcopy(tf)
            tf_id = orm_transforms.add_transform(**tf_copy, session=session)
            tf['transform_id'] = tf_id

            # work = tf['transform_metadata']['work']
            # original_work.set_work_id(tf_id, transforming=True)
            # original_work.set_status(WorkStatus.New)
            work.set_work_id(tf_id, transforming=True)
            work.set_status(WorkStatus.New)
            workflow.refresh_works()

            collections = generate_collections(tf)
            for coll in collections:
                collection = coll['collection']
                del coll['collection']
                coll['transform_id'] = tf_id
                coll_id = orm_collections.add_collection(**coll, session=session)
                # work.set_collection_id(coll, coll_id)
                collection.coll_id = coll_id

            # update transform to record the coll_id
            work.refresh_work()
            orm_transforms.update_transform(transform_id=tf_id,
                                            parameters={'transform_metadata': tf['transform_metadata']},
                                            session=session)

    if update_transforms:
        for tr_id in update_transforms:
            orm_transforms.update_transform(transform_id=tr_id, parameters=update_transforms[tr_id], session=session)

    if new_messages:
        orm_messages.add_messages(new_messages, session=session)
    if update_messages:
        orm_messages.update_messages(update_messages, session=session)
    return orm_requests.update_request(request_id, parameters, session=session)


@transactional_session
def update_request_with_workprogresses(request_id, parameters, new_workprogresses=None, update_workprogresses=None, session=None):
    """
    update an request.

    :param request_id: the request id.
    :param parameters: A dictionary of parameters.
    :param new_workprogresses: list of new workprogresses.
    """
    if new_workprogresses:
        orm_workprogresses.add_workprogresses(new_workprogresses, session=session)
    if update_workprogresses:
        for workprogress_id in update_workprogresses:
            orm_workprogresses.update_workprogress(workprogress_id, update_workprogresses[workprogress_id], session=session)
    return orm_requests.update_request(request_id, parameters, session=session)


@transactional_session
def get_requests_with_messaging(locking=False, bulk_size=None, session=None):
    msgs = core_messages.retrieve_request_messages(request_id=None, bulk_size=bulk_size, session=session)
    if msgs:
        req_ids = [msg['request_id'] for msg in msgs]
        if locking:
            req2s = orm_requests.get_requests_by_status_type(status=None, request_ids=req_ids,
                                                             locking=locking, locking_for_update=True,
                                                             bulk_size=None, session=session)
            if req2s:
                reqs = []
                for req_id in req_ids:
                    if len(reqs) >= bulk_size:
                        break
                    for req in req2s:
                        if req['request_id'] == req_id:
                            reqs.append(req)
                            break
            else:
                reqs = []

            parameters = {'locking': RequestLocking.Locking}
            for req in reqs:
                orm_requests.update_request(request_id=req['request_id'], parameters=parameters, session=session)
            return reqs
        else:
            reqs = orm_requests.get_requests_by_status_type(status=None, request_ids=req_ids, locking=locking,
                                                            locking_for_update=locking,
                                                            bulk_size=bulk_size, session=session)
            return reqs
    else:
        return []


@transactional_session
def get_requests_by_status_type(status, request_type=None, time_period=None, locking=False, bulk_size=None, to_json=False, by_substatus=False, with_messaging=False, session=None):
    """
    Get requests by status and type

    :param status: list of status of the request data.
    :param request_type: The type of the request data.
    :param time_period: Delay of seconds before last update.
    :param locking: Wheter to lock requests to avoid others get the same request.
    :param bulk_size: Size limitation per retrieve.
    :param to_json: return json format.

    :returns: list of Request.
    """
    if with_messaging:
        reqs = get_requests_with_messaging(locking=locking, bulk_size=bulk_size, session=session)
        if reqs:
            return reqs

    if locking:
        if bulk_size:
            # order by cannot work together with locking. So first select 2 * bulk_size without locking with order by.
            # then select with locking.
            req_ids = orm_requests.get_requests_by_status_type(status, request_type, time_period, locking=locking, bulk_size=bulk_size * 2,
                                                               locking_for_update=False, to_json=False, by_substatus=by_substatus,
                                                               only_return_id=True, session=session)
            if req_ids:
                req2s = orm_requests.get_requests_by_status_type(status, request_type, time_period, request_ids=req_ids,
                                                                 locking=locking, locking_for_update=True, bulk_size=None, to_json=to_json,
                                                                 by_substatus=by_substatus, session=session)
                if req2s:
                    # reqs = req2s[:bulk_size]
                    # order requests
                    reqs = []
                    for req_id in req_ids:
                        if len(reqs) >= bulk_size:
                            break
                        for req in req2s:
                            if req['request_id'] == req_id:
                                reqs.append(req)
                                break
                    # reqs = reqs[:bulk_size]
                else:
                    reqs = []
            else:
                reqs = []
        else:
            reqs = orm_requests.get_requests_by_status_type(status, request_type, time_period, locking=locking, locking_for_update=locking,
                                                            bulk_size=bulk_size,
                                                            to_json=to_json, by_substatus=by_substatus, session=session)

        parameters = {'locking': RequestLocking.Locking}
        for req in reqs:
            orm_requests.update_request(request_id=req['request_id'], parameters=parameters, session=session)
    else:
        reqs = orm_requests.get_requests_by_status_type(status, request_type, time_period, locking=locking, bulk_size=bulk_size,
                                                        to_json=to_json, by_substatus=by_substatus, session=session)
    return reqs


@transactional_session
def clean_locking(time_period=3600, session=None):
    """
    Clearn locking which is older than time period.

    :param time_period in seconds
    """
    orm_requests.clean_locking(time_period=time_period, session=session)


@transactional_session
def clean_next_poll_at(status, session=None):
    """
    Clearn next_poll_at.

    :param status: status of the request
    """
    orm_requests.clean_next_poll_at(status=status, session=session)
