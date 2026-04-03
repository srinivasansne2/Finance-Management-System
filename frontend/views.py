import requests
from django.shortcuts import render, redirect
import jwt
from django.contrib import messages
from django.conf import settings

def login_view(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
        }

        res = requests.post("http://127.0.0.1:8000/api/token/", json=data)

        if res.status_code == 200:
            access_token = res.json()['access']

            # store token
            request.session['token'] = access_token
            request.session['username'] = data['username']

            # 🔥 GET REAL USER ROLE
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            user_res = requests.get("http://127.0.0.1:8000/api/users/", headers=headers)

            if user_res.status_code == 200:
                users = user_res.json()

                # find logged-in user
                for u in users:
                    if u['username'] == data['username']:
                        request.session['role'] = u['role']
                        break

            return redirect('dashboard')

        return render(request, 'frontend/login.html', {"error": "Invalid login"})

    return render(request, 'frontend/login.html')

def dashboard_view(request):
    import requests
    from django.shortcuts import render, redirect
    from django.contrib import messages

    token = request.session.get('token')

    if not token:
        return redirect('login')

    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = requests.get("http://127.0.0.1:8000/api/dashboard/", headers=headers)

    if res.status_code == 401:
        request.session.flush()
        messages.warning(request, "Session expired. Please login again.")
        return redirect('login')

    data = res.json()

    return render(request, 'frontend/dashboard.html', {
        "data": data
    })

def transactions_view(request):
    import requests
    from django.shortcuts import render, redirect
    from django.contrib import messages

    token = request.session.get('token')
    role = request.session.get('role')

    # 🔐 If not logged in
    if not token:
        return redirect('login')

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # 🔥 PAGE NUMBER
    page = int(request.GET.get("page", 1))

    # 🔥 CLEAN PARAMS (NO None VALUES)
    params = {
        "page": page
    }

    if request.GET.get("category"):
        params["category"] = request.GET.get("category")

    if request.GET.get("type"):
        params["type"] = request.GET.get("type")

    if request.GET.get("search"):
        params["search"] = request.GET.get("search")

    if request.GET.get("start_date"):
        params["start_date"] = request.GET.get("start_date")

    if request.GET.get("end_date"):
        params["end_date"] = request.GET.get("end_date")

    # 🔥 DEBUG (REMOVE LATER)
    print("PARAMS:", params)

    # 🔥 API CALL
    res = requests.get(
        "http://127.0.0.1:8000/api/transactions/",
        headers=headers,
        params=params
    )

    # 🚨 HANDLE TOKEN EXPIRED
    if res.status_code == 401:
        request.session.flush()
        messages.warning(request, "Session expired. Please login again.")
        return redirect('login')

    data = res.json() if res.status_code == 200 else {}

    # 🔥 PAGINATION DATA
    transactions = data.get("results", [])
    next_page = data.get("next")
    previous_page = data.get("previous")

    # 🔥 TOTAL COUNT + PAGE INFO
    total_count = data.get("count", 0)
    page_size = 5  # ⚠ must match backend
    total_pages = (total_count // page_size) + (1 if total_count % page_size else 0)

    # 🔥 PAGE NUMBERS (FOR UI)
    page_numbers = list(range(1, total_pages + 1))

    return render(request, 'frontend/transactions.html', {
        "transactions": transactions,
        "role": role,
        "next_page": next_page,
        "previous_page": previous_page,
        "current_page": page,
        "total_pages": total_pages,
        "total_count": total_count,
        "page_numbers": page_numbers,
    })

def delete_transaction(request, id):
    token = request.session.get('token')

    headers = {
        "Authorization": f"Bearer {token}"
    }

    requests.delete(f"http://127.0.0.1:8000/api/transactions/{id}/", headers=headers)

    messages.success(request, "Transaction deleted successfully")

    return redirect('transactions')

def add_transaction(request):
    token = request.session.get('token')

    if request.method == "POST":
        data = {
            "amount": float(request.POST.get("amount")),
            "type": request.POST.get("type"),
            "category": request.POST.get("category"),
            "date": request.POST.get("date"),
            "note": ""
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        requests.post("http://127.0.0.1:8000/api/transactions/", json=data, headers=headers)

        messages.success(request, "Transaction added successfully")

        return redirect('transactions')

    return render(request, 'frontend/add.html')

def edit_transaction(request, id):
    token = request.session.get('token')

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # GET existing data
    res = requests.get(f"http://127.0.0.1:8000/api/transactions/{id}/", headers=headers)
    data = res.json()

    if request.method == "POST":
        updated_data = {
            "amount": float(request.POST.get("amount")),
            "type": request.POST.get("type"),
            "category": request.POST.get("category"),
            "date": request.POST.get("date"),
            "note": ""
        }

        requests.put(
            f"http://127.0.0.1:8000/api/transactions/{id}/",
            json=updated_data,
            headers=headers
        )
        messages.success(request, "Transaction updated successfully")

        return redirect('transactions')

    return render(request, 'frontend/edit.html', {"t": data})

def logout_view(request):
    request.session.flush()   # 🔥 clears everything
    return redirect('login')

def users_view(request):
    token = request.session.get('token')
    role = request.session.get('role')

    if role != 'admin':
        return redirect('dashboard')

    headers = {
        "Authorization": f"Bearer {token}"
    }

    res = requests.get("http://127.0.0.1:8000/api/users/", headers=headers)

    if res.status_code == 401:
        from django.contrib import messages
        request.session.flush()
        messages.warning(request, "Session expired. Please login again.")
        return redirect('login')
    
    data = res.json()

    return render(request, 'frontend/users.html', {"users": data})

def update_user(request, id):
    import requests
    from django.shortcuts import redirect
    from django.contrib import messages

    token = request.session.get('token')

    if request.method == "POST":
        data = {
            "role": request.POST.get("role"),
            "is_active": request.POST.get("is_active") == "on"
        }

        headers = {
            "Authorization": f"Bearer {token}"
        }

        res = requests.patch(   # 🔥 use PATCH (not PUT)
            f"http://127.0.0.1:8000/api/users/{id}/",
            json=data,
            headers=headers
        )

        print("STATUS:", res.status_code)
        print("RESPONSE:", res.text)

        messages.success(request, "User updated successfully")

    return redirect('users')

def register_view(request):

    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
        }

        res = requests.post("http://127.0.0.1:8000/api/users/", json=data)

        if res.status_code == 201:
            messages.success(request, "✅ Account created! Please login.")
            return redirect('login')

        else:
            error_data = res.json()

            messages_list = []

            for field, errors in error_data.items():
            
                # 🔥 if error is string
                if isinstance(errors, str):
                    messages_list.append(f"{field.capitalize()}: {errors}")

                # 🔥 if error is list
                elif isinstance(errors, list):
                    for err in errors:
                        messages_list.append(f"{field.capitalize()}: {err}")

            return render(request, 'frontend/register.html', {
                "errors": messages_list
            })

    # 🔥 IMPORTANT: this must always be present
    return render(request, 'frontend/register.html')
