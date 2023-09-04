from django.urls import path

from agenda.views import agendamento_list, agendamento_detail
from agenda.views import agendamento_list_api_view, agendamento_detail_api_view
from agenda.views import agendamento_list_api_view_create_update, agendamento_detail_api_view_create_update
from agenda.views import agendamento_list_api_view_model_serializer, agendamento_detail_api_view_model_serializer
from agenda.views import AgendamentoListClassBasedView, AgendamentoDetailClassBasedView
from agenda.views import AgendamentoListMixins, AgendamentoDetailMixins
from agenda.views import AgendamentoListGenericView, AgendamentoDetailGenericView
from agenda.views import AgendamentoListGenericCustom, AgendamentoDetailGenericCustom, PrestadorListGenericCustom


urlpatterns = [
    path("agendamentos/", agendamento_list),
    path("agendamentos/<int:id>/", agendamento_detail),

    path("agendamentos/api-view/", agendamento_list_api_view),
    path("agendamentos/api-view/<int:id>/", agendamento_detail_api_view),

    path("agendamentos/api-view-create-update/", agendamento_list_api_view_create_update),
    path("agendamentos/api-view-create-update/<int:id>/", agendamento_detail_api_view_create_update),

    path("agendamentos/api-view-model-serializer/", agendamento_list_api_view_model_serializer),
    path("agendamentos/api-view-model-serializer/<int:id>/", agendamento_detail_api_view_model_serializer),

    path("agendamentos/class-based-view-model-serializer/", AgendamentoListClassBasedView.as_view()),
    path("agendamentos/class-based-view-model-serializer/<int:id>/", AgendamentoDetailClassBasedView.as_view()),

    path("agendamentos/mixins-model-serializer/", AgendamentoListMixins.as_view()),
    path("agendamentos/mixins-model-serializer/<int:id>/", AgendamentoDetailMixins.as_view()),

    path("agendamentos/generic-view-model-serializer/", AgendamentoListGenericView.as_view()),
    path("agendamentos/generic-view-model-serializer/<int:id>/", AgendamentoDetailGenericView.as_view()),

    path("agendamentos/custom-model-serializer/", AgendamentoListGenericCustom.as_view()),
    path("agendamentos/custom-model-serializer/<int:id>/", AgendamentoDetailGenericCustom.as_view()),
    path("agendamentos/custom-model-serializer/prestadores/", PrestadorListGenericCustom.as_view()),
]
