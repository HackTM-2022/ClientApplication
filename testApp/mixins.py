from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

class UserMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user and user.is_active:
            return super(UserMixin, self).dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('login'))

class AdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user and user.is_active and user.role==1:
            return super(AdminMixin, self).dispatch(request, *args, **kwargs)
        raise Http404()