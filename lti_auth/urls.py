from django.conf.urls import url

from lti_auth.views import LTIConfigView, LTILandingPage, LTIRoutingView, \
    LTICourseEnableView


urlpatterns = [
    url(r'^config.xml$', LTIConfigView.as_view(), {}, 'lti-config'),
    url(r'^enable/$', LTICourseEnableView.as_view(), {}, 'lti-enable-course'),
    url(r'^landing/(?P<context>\w[^/]*)/$',
        LTILandingPage.as_view(), {}, 'lti-landing-page'),
    url(r'^$', LTIRoutingView.as_view(), {}, 'lti-login'),
]
