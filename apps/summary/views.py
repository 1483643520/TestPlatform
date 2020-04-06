import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.db.models import Sum, Count

from projects.models import Projects
from testcase.models import Testcases
from reports.models import ReportsModel

from .utils import cartogram_one, cartogram_two


class SummaryAPIView(APIView):
    """
    返回统计信息
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        获取统计信息
        """
        user = request.user
        user_info = {
            'username': user.username,
            "user_id": user.id,
            'role': '管理员' if user.is_superuser else '普通用户',
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S') if user.date_joined else '',
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '',
        }

        projects_count = Projects.objects.count()
        testcases_count = Testcases.objects.count()
        reports_count = ReportsModel.objects.count()

        run_testcases_success_count = ReportsModel.objects.aggregate(Sum('success'))['success__sum'] or 0
        run_testcases_filed_count = ReportsModel.objects.aggregate(Sum('filed'))['filed__sum'] or 0
        run_testcases_skip_count = ReportsModel.objects.aggregate(Sum('skip'))['skip__sum'] or 0
        run_testcases_total_count = ReportsModel.objects.aggregate(Sum('count'))['count__sum'] or 0

        if run_testcases_total_count:
            success_rate = int((run_testcases_success_count / run_testcases_total_count) * 100)
            filed_rate = int((run_testcases_filed_count / run_testcases_total_count) * 100)
            skip_rate = int((run_testcases_skip_count / run_testcases_total_count) * 100)
        else:
            success_rate = 0
            filed_rate = 0
            skip_rate = 0

        # 组装地图数据
        cartogram_first = cartogram_one()
        cartogram_seconde = cartogram_two()

        statistics = {
            'projects_count': projects_count,
            'testcases_count': testcases_count,
            'reports_count': reports_count,
            'success_rate': success_rate,
            'fail_rate': filed_rate,
            'skip_rate': skip_rate,

        }

        return Response(data={
            'user': user_info,
            'statistics': statistics,
            "cartogram_first": cartogram_first,
            "cartogram_seconde": cartogram_seconde
        })
