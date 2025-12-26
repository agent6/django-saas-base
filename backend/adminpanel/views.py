from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.forms import AdminUserCreateForm, AdminUserForm, SitePasswordResetForm
from accounts.permissions import admin_required
from core.email_utils import send_test_email
from core.models import SiteSettings

from .forms import GroupForm, SiteSettingsForm

User = get_user_model()


@admin_required
def settings_view(request):
    site_settings = SiteSettings.get_solo()
    if request.method == "POST":
        form = SiteSettingsForm(request.POST, instance=site_settings)
        if form.is_valid():
            site_settings = form.save()
            action = request.POST.get("action", "save")
            if action == "test":
                if not request.user.email:
                    messages.error(request, "Your account does not have an email address.")
                else:
                    try:
                        send_test_email(site_settings, request.user.email)
                        messages.success(request, "Test email sent.")
                    except Exception:
                        messages.error(request, "Test email failed. Check SMTP settings and logs.")
            else:
                messages.success(request, "Settings updated.")
            return redirect("admin-settings")
    else:
        form = SiteSettingsForm(instance=site_settings)

    return render(request, "admin/settings.html", {"form": form})


@admin_required
def user_list(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.all().order_by("email")
    if query:
        users = users.filter(Q(email__icontains=query) | Q(name__icontains=query))

    paginator = Paginator(users, 25)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {"page_obj": page_obj, "query": query}

    if request.headers.get("HX-Request"):
        return render(request, "admin/partials/user_table.html", context)

    return render(request, "admin/users_list.html", context)


@admin_required
def user_create(request):
    if request.method == "POST":
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User created.")
            return redirect("admin-user-edit", user_id=user.id)
    else:
        form = AdminUserCreateForm(initial={"is_active": True, "must_change_password": True})

    return render(request, "admin/user_create.html", {"form": form})


@admin_required
def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        form = AdminUserForm(request.POST, instance=user)
        if form.is_valid():
            if not form.cleaned_data.get("is_staff"):
                other_admins = User.objects.filter(is_staff=True).exclude(pk=user.pk).count()
                if other_admins == 0:
                    form.add_error(
                        "is_staff", "You are the last admin. Assign another admin first."
                    )
            if not form.errors:
                form.save()
                messages.success(request, "User updated.")
                return redirect("admin-users")
    else:
        form = AdminUserForm(instance=user)

    return render(request, "admin/user_edit.html", {"form": form, "user_obj": user})


@admin_required
def user_reset_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if not user.email:
        messages.error(request, "User does not have an email address.")
        return redirect("admin-user-edit", user_id=user_id)

    form = SitePasswordResetForm({"email": user.email})
    if form.is_valid():
        form.save(
            request=request,
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            use_https=request.is_secure(),
        )
        messages.success(request, "Password reset email sent.")
    else:
        messages.error(request, "Unable to send reset email.")

    return redirect("admin-user-edit", user_id=user_id)


@admin_required
def group_list(request):
    query = request.GET.get("q", "").strip()
    groups = Group.objects.all().order_by("name")
    if query:
        groups = groups.filter(name__icontains=query)

    paginator = Paginator(groups, 25)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {"page_obj": page_obj, "query": query}

    if request.headers.get("HX-Request"):
        return render(request, "admin/partials/group_table.html", context)

    return render(request, "admin/groups_list.html", context)


@admin_required
def group_edit(request, group_id=None):
    group = None
    if group_id:
        group = get_object_or_404(Group, pk=group_id)

    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group saved.")
            return redirect("admin-groups")
    else:
        form = GroupForm(instance=group)

    return render(request, "admin/group_edit.html", {"form": form, "group": group})
