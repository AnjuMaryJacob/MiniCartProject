from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile
from .forms import ProfileForm


@login_required
def profile_detail(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        'profiles/profile_detail.html',
        {
            'profile': profile
        }
    )


@login_required
def profile_create(request):

    # Check whether profile already exists
    if Profile.objects.filter(
        user=request.user
    ).exists():

        return redirect('profile_detail')

    if request.method == 'POST':

        form = ProfileForm(request.POST)

        if form.is_valid():

            profile = form.save(commit=False)

            profile.user = request.user

            profile.save()

            messages.success(
                request,
                'Profile created successfully.'
            )

            return redirect('profile_detail')

    else:

        form = ProfileForm()

    return render(
        request,
        'profiles/profile_form.html',
        {
            'form': form
        }
    )


@login_required
def profile_update(request):

    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Profile updated successfully.'
            )

            return redirect('profile_detail')

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'profiles/profile_form.html',
        {
            'form': form,
            'profile': profile
        }
    )


@login_required
def profile_delete(request):

    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    if request.method == 'POST':

        profile.delete()

        messages.success(
            request,
            'Profile deleted successfully.'
        )

        return redirect('product_list')

    return render(
        request,
        'profiles/profile_delete.html',
        {
            'profile': profile
        }
    )