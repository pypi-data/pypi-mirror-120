# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 CESNET.
#
# NR datasets repository is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration."""

from __future__ import absolute_import, print_function

from functools import partial

from elasticsearch_dsl.query import Bool, Q
from invenio_records_rest.facets import terms_filter, range_filter
from invenio_records_rest.utils import allow_all, deny_all
from oarepo_communities.constants import STATE_PUBLISHED, STATE_EDITING, STATE_APPROVED, STATE_PENDING_APPROVAL, \
    STATE_DELETED
# TODO: this needs to be updated to new common data model
# from nr_generic.config import FACETS, CURATOR_FACETS, CURATOR_FILTERS, FILTERS
from oarepo_communities.links import community_record_links_factory
from oarepo_communities.permissions import update_object_permission_impl
from oarepo_communities.search import community_search_factory
from oarepo_multilingual import language_aware_text_term_facet, language_aware_text_terms_filter
from oarepo_records_draft import DRAFT_IMPORTANT_FILTERS
from oarepo_taxonomies.serializers import taxonomy_enabled_search
from oarepo_tokens.permissions import put_file_token_permission_factory
from oarepo_ui.facets import translate_facets, term_facet, nested_facet, translate_facet, date_histogram_facet
from oarepo_ui.filters import nested_filter

from nr_datasets.constants import PUBLISHED_DATASET_PID_TYPE, PUBLISHED_DATASET_RECORD, \
    published_index_name, \
    DRAFT_DATASET_PID_TYPE, DRAFT_DATASET_RECORD, ALL_DATASET_PID_TYPE, ALL_DATASET_RECORD, \
    all_datasets_index_name
from nr_datasets.record import draft_index_name
from .links import nr_links_factory
from .search import DatasetRecordsSearch

_ = lambda x: x

RECORDS_DRAFT_ENDPOINTS = {
    'datasets-community': {
        'draft': 'draft-datasets-community',
        'pid_type': PUBLISHED_DATASET_PID_TYPE,
        'pid_minter': 'nr_datasets',
        'pid_fetcher': 'nr_datasets',
        'default_endpoint_prefix': True,
        'max_result_window': 500000,
        'record_class': PUBLISHED_DATASET_RECORD,
        'search_index': published_index_name,
        'search_factory_imp': taxonomy_enabled_search(community_search_factory,
                                                      taxonomy_aggs=[],
                                                      fallback_language="cs"),

        'list_route': '/<community_id>/datasets/',
        'item_route': f'/<commpid({PUBLISHED_DATASET_PID_TYPE},model="datasets",record_class="'
                      f'{PUBLISHED_DATASET_RECORD}"):pid_value>',

        # Who can publish a draft dataset record
        'publish_permission_factory_imp': 'oarepo_communities.permissions.publish_permission_impl',
        # Who can unpublish (delete published & create a new draft version of)
        # a published dataset record
        'unpublish_permission_factory_imp': 'oarepo_communities.permissions.unpublish_permission_impl',
        # Who can edit (create a new draft version of) a published dataset record
        'edit_permission_factory_imp': 'oarepo_communities.permissions.unpublish_permission_impl',
        # Who can enumerate published dataset record collection
        'list_permission_factory_imp': allow_all,
        # Who can view an existing published dataset record detail
        'read_permission_factory_imp': allow_all,
        # Make sure everything else is for biden
        'create_permission_factory_imp': deny_all,
        'update_permission_factory_imp': deny_all,
        'delete_permission_factory_imp': deny_all,

        'default_media_type': 'application/json',
        'links_factory_imp': partial(community_record_links_factory,
                                     original_links_factory=nr_links_factory),
        'search_class': DatasetRecordsSearch,
        # 'indexer_class': CommitingRecordIndexer,
        'files': dict(
            # Who can upload attachments to a draft dataset record
            put_file_factory=deny_all,
            # Who can download attachments from a draft dataset record
            get_file_factory=allow_all,
            # Who can delete attachments from a draft dataset record
            delete_file_factory=deny_all
        )

    },
    'draft-datasets-community': {
        'pid_type': DRAFT_DATASET_PID_TYPE,
        'record_class': DRAFT_DATASET_RECORD,

        'list_route': '/<community_id>/datasets/draft/',
        'item_route': f'/<commpid({DRAFT_DATASET_PID_TYPE},model="datasets/draft",record_cla'
                      f'ss="{DRAFT_DATASET_RECORD}"):pid_value>',
        'search_index': draft_index_name,
        'links_factory_imp': partial(community_record_links_factory,
                                     original_links_factory=nr_links_factory),
        'search_factory_imp': community_search_factory,
        'search_class': DatasetRecordsSearch,
        'search_serializers': {
            'application/json': 'oarepo_validate:json_search',
        },
        'record_serializers': {
            'application/json': 'oarepo_validate:json_response',
        },

        # Who can create a new draft dataset record
        'create_permission_factory_imp': 'oarepo_communities.permissions.create_object_permission_impl',
        # Who can edit an existing draft dataset record
        'update_permission_factory_imp': 'oarepo_communities.permissions.update_object_permission_impl',
        # Who can view an existing draft dataset record
        'read_permission_factory_imp': 'oarepo_communities.permissions.read_object_permission_impl',
        # Who can delete an existing draft dataset record
        'delete_permission_factory_imp': 'oarepo_communities.permissions.delete_object_permission_impl',
        # Who can enumerate a draft dataset record collection
        'list_permission_factory_imp': deny_all,

        'record_loaders': {
            'application/json': 'oarepo_validate.json_files_loader',
            'application/json-patch+json': 'oarepo_validate.json_loader'
        },
        'files': dict(
            put_file_factory=put_file_token_permission_factory(update_object_permission_impl),
            get_file_factory='oarepo_communities.permissions.read_object_permission_impl',
            delete_file_factory='oarepo_communities.permissions.update_object_permission_impl'
        )

    },
    'datasets': {
        'draft': 'draft-datasets',
        'pid_type': PUBLISHED_DATASET_PID_TYPE + '-datasets',
        'pid_minter': 'nr_datasets',
        'pid_fetcher': 'nr_datasets',
        'default_endpoint_prefix': True,
        'max_result_window': 500000,
        'record_class': ALL_DATASET_RECORD,
        'search_index': published_index_name,

        'list_route': '/datasets/',
        'item_route': f'/not-really-used',
        'publish_permission_factory_imp': deny_all,
        'unpublish_permission_factory_imp': deny_all,
        'edit_permission_factory_imp': deny_all,
        'list_permission_factory_imp': allow_all,
        'read_permission_factory_imp': allow_all,
        'create_permission_factory_imp': deny_all,
        'update_permission_factory_imp': deny_all,
        'delete_permission_factory_imp': deny_all,
        'default_media_type': 'application/json',
        'links_factory_imp': partial(community_record_links_factory,
                                     original_links_factory=nr_links_factory),
        'search_class': DatasetRecordsSearch,
        # 'indexer_class': CommitingRecordIndexer,
        'files': dict(
            # Who can upload attachments to a draft dataset record
            put_file_factory=deny_all,
            # Who can download attachments from a draft dataset record
            get_file_factory=allow_all,
            # Who can delete attachments from a draft dataset record
            delete_file_factory=deny_all
        )
    },
    'draft-datasets': {
        'pid_type': DRAFT_DATASET_PID_TYPE + '-draft-datasets',
        'record_class': ALL_DATASET_RECORD,

        'list_route': '/datasets/draft/',
        'item_route': f'/not-really-used',
        'search_index': draft_index_name,
        'links_factory_imp': partial(community_record_links_factory,
                                     original_links_factory=nr_links_factory),
        'search_class': DatasetRecordsSearch,
        'search_serializers': {
            'application/json': 'oarepo_validate:json_search',
        },
        'record_serializers': {
            'application/json': 'oarepo_validate:json_response',
        },

        'create_permission_factory_imp': deny_all,
        'update_permission_factory_imp': deny_all,
        'read_permission_factory_imp': 'oarepo_communities.permissions.read_object_permission_impl',
        'delete_permission_factory_imp': deny_all,
        'list_permission_factory_imp': deny_all,
        'files': dict(
            put_file_factory=deny_all,
            get_file_factory='oarepo_communities.permissions.read_object_permission_impl',
            delete_file_factory=deny_all
        )
    }
}

RECORDS_REST_ENDPOINTS = {
    'all-datasets': dict(
        pid_type=ALL_DATASET_PID_TYPE,
        pid_minter='nr_datasets',
        pid_fetcher='nr_datasets',
        default_endpoint_prefix=True,
        record_class=ALL_DATASET_RECORD,
        search_class=DatasetRecordsSearch,
        search_index=all_datasets_index_name,
        search_serializers={
            'application/json': 'oarepo_validate:json_search',
        },
        list_route='/datasets/all/',
        links_factory_imp=partial(community_record_links_factory,
                                  original_links_factory=nr_links_factory),
        default_media_type='application/json',
        max_result_window=10000,
        # not used really
        item_route=f'/datasets/'
                   f'/not-used-but-must-be-present',
        list_permission_factory_imp=allow_all,
        create_permission_factory_imp=deny_all,
        delete_permission_factory_imp=deny_all,
        update_permission_factory_imp=deny_all,
        read_permission_factory_imp=deny_all,
        record_serializers={
            'application/json': 'oarepo_validate:json_response',
        },
        use_options_view=False
    ),
    'community-datasets': dict(
        pid_type=ALL_DATASET_PID_TYPE + '-community-all',
        pid_minter='nr_datasets',
        pid_fetcher='nr_datasets',
        default_endpoint_prefix=True,
        record_class=ALL_DATASET_RECORD,
        search_class=DatasetRecordsSearch,
        search_index=all_datasets_index_name,
        search_factory_imp=community_search_factory,
        search_serializers={
            'application/json': 'oarepo_validate:json_search',
        },
        list_route='/<community_id>/datasets/all/',
        links_factory_imp=partial(community_record_links_factory,
                                  original_links_factory=nr_links_factory),
        default_media_type='application/json',
        max_result_window=10000,
        # not used really
        item_route=f'/dataset/'
                   f'/not-used-but-must-be-present',
        list_permission_factory_imp=allow_all,
        create_permission_factory_imp=deny_all,
        delete_permission_factory_imp=deny_all,
        update_permission_factory_imp=deny_all,
        read_permission_factory_imp=deny_all,
        record_serializers={
            'application/json': 'oarepo_validate:json_response',
        },
        use_options_view=False
    )
}


def state_terms_filter(field):
    def inner(values):
        if 'filling' in values:
            return Bool(should=[
                Q('terms', **{field: values}),
                Bool(
                    must_not=[
                        Q('exists', field='state')
                    ]
                )
            ], minimum_should_match=1)
        else:
            return Q('terms', **{field: values})

    return inner


DATASETS_FILTERS = {
    _('oarepo:recordStatus'): state_terms_filter('oarepo:recordStatus'),
    _('keywords'): terms_filter('keywords'),
    _('languages'): nested_filter('languages', language_aware_text_terms_filter('languages.title')),
    _('creators'): terms_filter('creators.fullName'),
    _('affiliations'): nested_filter('creators.affiliations', terms_filter('creators.affiliations.name')),
    _('rights'): nested_filter('rights', language_aware_text_terms_filter('rights.title')),
}

# TODO: merge this to nr-generic
FILTERS = {
    _('creators'): terms_filter('creators.fullName'),
    _('accessRights'): nested_filter("accessRights",
                                     language_aware_text_terms_filter('accessRights.title')),
    _('resourceType'): nested_filter('resourceType',
                                     language_aware_text_terms_filter('resourceType.title')),
    _('keywords'): language_aware_text_terms_filter('keywords'),
    _('subjectCategories'): nested_filter('subjectCategories',
                                          language_aware_text_terms_filter('subjectCategories.title')),
    _('language'): nested_filter('language',
                                 language_aware_text_terms_filter('language.title')),
    _('dateCreated'): range_filter('dateCreated'),
    _('dateAvailable'): range_filter('dateAvailable'),
    _('dateModified'): range_filter('dateModified'),
    _('dateCollected'): range_filter('dateCollected'),
    _('dateWithdrawn'): range_filter('dateWithdrawn'),
    _('dateValidTo'): range_filter('dateValidTo'),
}

# TODO: merge this to nr-generic
CURATOR_FILTERS = {
    _('rights'): nested_filter('rights', language_aware_text_terms_filter('rights.title')),
    _('fundingReferences'): nested_filter('fundingReferences.funder',
                                          language_aware_text_terms_filter(
                                              'fundingReferences.funder.title')),
}

DATASETS_FACETS = {
    'oarepo:recordStatus': translate_facet(
        term_facet('oarepo:recordStatus', missing=STATE_EDITING),
        possible_values=[
            _(STATE_EDITING),
            _(STATE_PENDING_APPROVAL),
            _(STATE_APPROVED),
            _(STATE_PUBLISHED),
            _(STATE_DELETED)
        ]),
    'language': nested_facet('language', language_aware_text_term_facet('language.title')),
    'keywords': language_aware_text_term_facet('keywords'),
    'creators': term_facet('creators.fullName'),
    'affiliation': nested_facet('creators.affiliation', language_aware_text_term_facet('creators.affiliation.title')),
    'rights': nested_facet('rights', language_aware_text_term_facet('rights.title')),
}

# TODO: merge this to nr-generic
FACETS = {
    'creators': term_facet('creators.fullName'),
    'accessRights': nested_facet("accessRights", language_aware_text_term_facet('accessRights.title')),
    'resourceType': nested_facet('resourceType', language_aware_text_term_facet('resourceType.title')),
    'keywords': language_aware_text_term_facet('keywords'),
    'subjectCategories': nested_facet('subjectCategories', language_aware_text_term_facet('subjectCategories.title')),
    'language': nested_facet('language', language_aware_text_term_facet('language.title')),
    'dateCreated': date_histogram_facet('dateCreated'),
}
# TODO: merge this to nr-generic
CURATOR_FACETS = {
    'rights': nested_facet('rights', language_aware_text_term_facet('rights.title')),
    'fundingReferences': nested_facet('fundingReferences.funder',
                                      language_aware_text_term_facet('fundingReferences.funder.title')),
    'dateAvailable': date_histogram_facet('dateAvailable'),
    'dateModified': date_histogram_facet('dateModified'),
    'dateCollected': date_histogram_facet('dateCollected'),
    'dateWithdrawn': date_histogram_facet('dateWithdrawn'),
    'dateValidTo': date_histogram_facet('dateValidTo'),
}

RECORDS_REST_FACETS = {
    draft_index_name: {
        "aggs": translate_facets(
            {**DATASETS_FACETS,
             **FACETS,
             # **CURATOR_FACETS,
             # **DRAFT_IMPORTANT_FACETS
             },
            label='{facet_key}',
            value='{value_key}'),
        "filters": {**DATASETS_FILTERS,
                    **FILTERS,
                    **CURATOR_FILTERS,
                    **DRAFT_IMPORTANT_FILTERS}
    },
    all_datasets_index_name: {
        "aggs": translate_facets(
            {**DATASETS_FACETS,
             **FACETS,
             # **CURATOR_FACETS,
             # **DRAFT_IMPORTANT_FACETS
             },
            label='{facet_key}',
            value='{value_key}'),
        "filters": {**DATASETS_FILTERS,
                    **FILTERS,
                    **CURATOR_FILTERS,
                    **DRAFT_IMPORTANT_FILTERS}
    },
}

RECORDS_REST_SORT_OPTIONS = {
    draft_index_name: {
        'alphabetical': {
            'title': 'alphabetical',
            'fields': [
                'title.cs.raw'
            ],
            'default_order': 'asc',
            'order': 1
        },
        'best_match': {
            'title': 'Best match',
            'fields': ['_score'],
            'default_order': 'desc',
            'order': 1,
        }
    }
}

RECORDS_REST_DEFAULT_SORT = {
    draft_index_name: {
        'query': 'best_match',
        'noquery': 'best_match'
    }
}
