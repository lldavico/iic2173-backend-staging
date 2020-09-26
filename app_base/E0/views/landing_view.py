from django.views.generic import TemplateView
from django.http import HttpResponse
from E0.models.board_model import BoardModel
from django.shortcuts import get_object_or_404, render
class LandingView(TemplateView):

    @staticmethod
    def index(request):
        board_list = BoardModel.objects.order_by('-board_id')
        ctx = {"board_list": board_list}
        template_name = "landing_page.html"
        return render(request, template_name, ctx)