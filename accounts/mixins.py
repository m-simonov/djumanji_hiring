from django.shortcuts import redirect
from hiring.models import Company


class CompanyAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner_id=request.user.id)
        except Company.DoesNotExist:
            return redirect('letsstart')
        return super(CompanyAccessMixin, self).dispatch(request, *args, **kwargs)
