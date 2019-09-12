from django.conf.urls import url

from .views import (RecentsQuestionList,
	QuestionDetailFromIndex,
	QuestionCreate,questionlist, 
	questionlist_byTag,
	questionlist_WithoutResponses,
	QuestionUpdate,
	QuestionDelete,
	AnswerUpdate,
	AnswerDelete,
	)

urlpatterns = [
url (r'^$', RecentsQuestionList.as_view(), name='question_recents_list'),
url(r'^question/(?P<id>\d+)/$',QuestionDetailFromIndex.as_view(), name='question_detail_fromindex'),
url(r'^question/toask/$',QuestionCreate.as_view(), name='question_ask_create'),
url(r'^question/list/$',questionlist, name='question_list'),
url(r'^question/list/WithoutResponses$',questionlist_WithoutResponses, name='question_list_withouR'),
url(r'^question/$',QuestionCreate.as_view(), name='question_ask_create'),
url(r'^question/tag/(?P<id>\d+)/$',questionlist_byTag, name='question_detail_ByTag'),
url(r'^question/update/(?P<pk>\d+)/$', QuestionUpdate.as_view(), name='question_update'),
url(r'^question/delete/(?P<pk>\d+)/$', QuestionDelete.as_view(), name='question_delete'),
url(r'^answer/update/(?P<pk>\d+)/$', AnswerUpdate.as_view(), name='answer_update'),
url(r'^answer/delete/(?P<pk>\d+)/$', AnswerDelete.as_view(), name='answer_delete'),
]