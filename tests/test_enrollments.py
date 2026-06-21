def test_student_enroll_and_deregister_course(client):
    admin_payload = {"name": "Admin One", "email": "admin2@example.com", "password": "adminpassword", "role": "admin"}
    client.post("/api/v1/auth/register", json=admin_payload)
    admin_login = client.post(
        "/api/v1/auth/login",
        data={"username": admin_payload["email"], "password": admin_payload["password"]},
    )
    admin_token = admin_login.json()["access_token"]

    course_data = {"title": "Databases", "code": "DB101", "capacity": 1}
    course_response = client.post(
        "/api/v1/courses",
        json=course_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    course_id = course_response.json()["id"]

    student_payload = {"name": "Student Two", "email": "student2@example.com", "password": "studentpass", "role": "student"}
    client.post("/api/v1/auth/register", json=student_payload)
    student_login = client.post(
        "/api/v1/auth/login",
        data={"username": student_payload["email"], "password": student_payload["password"]},
    )
    student_token = student_login.json()["access_token"]

    enroll_response = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert enroll_response.status_code == 200
    assert enroll_response.json()["course_id"] == course_id

    deregister_response = client.delete(
        f"/api/v1/enrollments/{course_id}",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    assert deregister_response.status_code == 200
    assert deregister_response.json()["course_id"] == course_id
