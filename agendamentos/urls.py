from django.urls import path

from .views import AgendamentoView, AgendamentoAddView, AgendamentoUpdateView, AgendamentoDeleteView

urlpatterns = [
    path('agendamentos', AgendamentoView.as_view(), name='agendamentos'),
    path('agendamento/adicionar/', AgendamentoAddView.as_view(), name='agendamento_adicionar'),
    path('<int:pk>/agendamento/editar/', AgendamentoUpdateView.as_view(), name='agendamento_editar'),
    path('<int:pk>/agendamento/apagar/', AgendamentoDeleteView.as_view(), name='agendamento_apagar'),
]