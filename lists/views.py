from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth, Group
from django.contrib import messages

@login_required(login_url='/sign-in')
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@login_required(login_url='/sign-in')
def group_list(request):
    groups = Group.objects.all()
    return render(request, 'group_list.html', {'groups': groups})

@staff_member_required
def delete_group(request, pk):
    try:
        group = Group.objects.get(pk=pk)
        group.delete()
        messages.success(request, "The group is deleted")

    except Group.DoesNotExist:
        messages.error(request, "Group does not exist")
        return render(request, 'group_list.html')

    except Exception as e:
        return render(request, 'group_list.html', {'err': e})

    return redirect('group_list')

@login_required(login_url='/sign-in')
def create_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username, email=email).exists():
                messages.info(request, 'Username or email is already exists!')
                return redirect('user_create')
            else:
                user = User.objects.create_user(email=email, username=username, password=password)
                user.save()
                return redirect('/')
        else:
            messages.info(request, 'Passwords not correct')
            return redirect('user_create')
    else:
        return render(request, 'user_create.html')


@staff_member_required
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        messages.success(request, "The user is deleted")

    except User.DoesNotExist:
        messages.error(request, "User does not exist")
        return render(request, 'user_list.html')

    except Exception as e:
        return render(request, 'user_list.html', {'err': e})

    return redirect('user_list')

@login_required(login_url='/sign-in')
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)

    if not request.user.is_superuser:
        if request.user != user:
            return redirect('user_list')

    if request.method == 'POST':
        new_email = request.POST.get('email')
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')

        user.email = new_email
        user.username = new_username
        user.password = new_password

        user.save()

        return redirect('user_list')

    return render(request, 'user_edit.html', {'user': user})

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Неправильні дані для входу!")
        return redirect('/sign-in')
    return render(request, 'sing_in.html')

@login_required(login_url='/sign-in')
def logout(request):
    auth.logout(request)
    return redirect('sign_in')
