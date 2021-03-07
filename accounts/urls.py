# -*- coding: utf-8 -*-
from django.conf.urls import url

from accounts.views.group import PilotLaureateGroupView
from .views import (
    AskForResetPasswordEmailView,
    GroupAdminView,
    GroupView,
    PasswordChangeView,
    PasswordResetConfirmView,
    UserAndRgpdConsentCreateOnlyView,
    UserAndRgpdConsentView,
    UserProfilePicView,
    UserView,
    # UserSearchView,
    UserWithGroupView,
)

app_name = "accounts"

urlpatterns = [
    url(r"^profile/$", UserAndRgpdConsentView.as_view(), name="profile"),
    url(
        r"^profile/(?P<pk>\d+)/$",
        UserAndRgpdConsentView.as_view(),
        name="profile_detail",
    ),
    url(
        r"^profile/create/$",
        UserAndRgpdConsentCreateOnlyView.as_view(),
        name="profile_create",
    ),
    # Ask for a reset password email
    url(
        r"^password/reset/$",
        AskForResetPasswordEmailView.as_view(),
        name="password_reset",
    ),
    # Reset password
    url(
        r"^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        PasswordResetConfirmView.as_view(),
        {"post_reset_redirect": "accounts:password_reset_complete"},
        name="password_reset_confirm",
    ),
    url(r"^password/change/$", PasswordChangeView.as_view(), name="password_change"),
    url(r"^group/$", GroupView.as_view(), name="group_list"),
    url(r"^group/(?P<pk>\d+)/$", GroupView.as_view(), name="group_detail"),
    url(r"^group-admin/$", GroupAdminView.as_view(), name="group_admin_list"),
    url(r"^group-fac/$", PilotLaureateGroupView.as_view(), name="group_fac_detail"),
    url(r"^user/$", UserView.as_view(), name="user_list"),
    # url(
    #     r"^user/search/(?P<user_type>[^/.]+)/(?P<query>[^/.]+)/$",
    #     UserSearchView.as_view(),
    #     name="user_search_by_user_type",
    # ),
    # url(
    #     r"^user/search/(?P<query>[^/.]+)/$",
    #     UserSearchView.as_view(),
    #     name="user_search",
    # ),
    url(r"^user/(?P<pk>\d+)/$", UserView.as_view(), name="user_detail"),
    url(
        r"^user-with-group/$", UserWithGroupView.as_view(), name="user_with_group_list"
    ),
    url(
        r"^user-profile-pic/$", UserProfilePicView.as_view(), name="userprofilepic_list"
    ),
    url(
        r"^user-profile-pic/(?P<pk>\d+)/$",
        UserProfilePicView.as_view(),
        name="userprofilepic_detail",
    ),
]
