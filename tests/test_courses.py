def test_public_course_listing_and_admin_course_management(client):
    response = client.get("/api/v1/courses")
    assert response.status_code == 200
    assert response.json() == []

    admin_payload = {"name": "Admin User", "email": "admin@example.com", "password": "adminpass123", "role": "admin"}
    client.post("/api/v1/auth/register", json=admin_payload)

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": admin_payload["email"], "password": admin_payload["password"]},
    )
    token = login_response.json()["access_token"]

    course_data = {"title": "Intro to Python", "code": "CS101", "capacity": 2}
    create_response = client.post(
        "/api/v1/courses",
        json=course_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 200
    course = create_response.json()
    assert course["code"] == "CS101"
    assert course["capacity"] == 2

    detail_response = client.get(f"/api/v1/courses/{course['id']}")
    assert detail_response.status_code == 200
    assert detail_response.json()["title"] == "Intro to Python"

    update_response = client.put(
        f"/api/v1/courses/{course['id']}",
        json={"title": "Python Fundamentals", "capacity": 3, "is_active": False},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Python Fundamentals"
    assert update_response.json()["is_active"] is False


def test_student_cannot_create_course(client):
    student_payload = {
        "name": "Student User",
        "email": "student-course@example.com",
        "password": "studentpass123",
        "role": "student",
    }
    client.post("/api/v1/auth/register", json=student_payload)

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": student_payload["email"], "password": student_payload["password"]},
    )
    token = login_response.json()["access_token"]

    create_response = client.post(
        "/api/v1/courses",
        json={"title": "Unauthorized Course", "code": "UA101", "capacity": 10},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 403
    assert create_response.json()["detail"] == "Admin credentials required"
