from django.shortcuts import reverse, redirect


def redirect_to_nxt(request, redirect_path):
    """
    Redirect to GET["next"] if it exists else
    navigate to redirect_path.
    """
    nxt = request.GET.get('next', None)
    if nxt:
        return redirect(nxt)
    return redirect(reverse(redirect_path))
