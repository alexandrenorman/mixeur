# -*- coding: utf-8 -*-

from .token import CustomObtainJSONWebToken
from .group import GroupAdminView, GroupView

from .user import (
    AccountUpdate,
    AccountView,
    AskForResetPasswordEmailView,
    PasswordChangeView,
    PasswordResetConfirmView,
    UserAndRgpdConsentCreateOnlyView,
    UserAndRgpdConsentView,
    UserProfilePicView,
    UserView,
    UserWithGroupView,
)

__all__ = [
    "AccountUpdate",
    "AccountView",
    "AskForResetPasswordEmailView",
    "CustomObtainJSONWebToken",
    "GroupAdminView",
    "GroupView",
    "PasswordChangeView",
    "PasswordResetConfirmView",
    "UserAndRgpdConsentCreateOnlyView",
    "UserAndRgpdConsentView",
    "UserProfilePicView",
    "UserView",
    "UserWithGroupView",
]
