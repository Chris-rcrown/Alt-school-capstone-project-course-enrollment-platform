def test_admin_can_view_and_remove_enrollments(client):
    admin_payload = {"name": "Admin Three", "email": "admin3@example.com", "password": "adminpass3", "role": "admin"}
    client.post("/api/v1/auth/register", json=admin_payload)
    admin_login = client.post(
        "/api/v1/auth/login",
        data={"username": admin_payload["email"], "password": admin_payload["password"]},
    )
    admin_token = admin_login.json()["access_token"]

    course_response = client.post(
        "/api/v1/courses",
        json={"title": "APIs", "code": "API101", "capacity": 2},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    course_id = course_response.json()["id"]

    student_payload = {"name": "Student Three", "email": "student3@example.com", "password": "studpass3", "role": "student"}
    client.post("/api/v1/auth/register", json=student_payload)
    student_login = client.post(
        "/api/v1/auth/login",
        data={"username": student_payload["email"], "password": student_payload["password"]},
    )
    student_token = student_login.json()["access_token"]

    student_enroll = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert student_enroll.status_code == 200

    all_enrollments = client.get(
        "/api/v1/enrollments",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert all_enrollments.status_code == 200
    assert len(all_enrollments.json()) == 1

    course_enrollments = client.get(
        f"/api/v1/enrollments/course/{course_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert course_enrollments.status_code == 200
    assert course_enrollments.json()[0]["course_id"] == course_id

    removed = client.delete(
        f"/api/v1/enrollments/{course_id}/users/{student_enroll.json()['user_id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert removed.status_code == 200
    assert removed.json()["user_id"] == student_enroll.json()["user_id"]
