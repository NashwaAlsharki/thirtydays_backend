from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

# ----------------------------------------- #
# home page tests


def test_get_featured_challenges():
    # featured challenges are the 3 challenges with the most joiners
    response = client.get("/")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}

# ----------------------------------------- #
# browse page tests


def test_get_all_challenges():
    response = client.get("/browse")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_get_challenges_by_keyword():
    response = client.get("/browse/?keyword=flexibility")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_get_challenges_by_category():
    response = client.get("/browse/?category=fitness")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_get_challenges_by_duration():
    response = client.get("/browse/?duration=7")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_get_challenges_by_keyword_category_duration():
    response = client.get(
        "/browse/?keyword=fitness&category=fitness&duration=7")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_get_challenges_no_matches():
    response = client.get(
        "/browse/?keyword=fitness&category=fitness&duration=7")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}

# ----------------------------------------- #
# challenge page tests


def test_get_challenge():
    response = client.get("/challenge/1")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_get_challenge_module():
    response = client.get("/challenge/1/day/1")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_join_challenge():
    response = client.post("/challenge/1/join")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}

# ----------------------------------------- #
# create page tests


def test_create_challenge():
    response = client.post("/create")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_update_challenge_details():
    response = client.patch("/create/1")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_save_challenge_day():
    response = client.patch("/create/1/day/1")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_add_excercise_to_day():
    response = client.patch("/create/1/day/1")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_delete_excercise_from_day():
    response = client.delete("/create/1/day/1")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_publish_challenge():
    response = client.patch("/create/1")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}

# ----------------------------------------- #
# dashboard page tests


def test_get_created_challenges():
    response = client.patch("/dashboard")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_get_created_challenges_is_empty():
    response = client.patch("/dashboard")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_get_joined_challenges():
    response = client.patch("/dashboard")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}


def test_get_joined_challenges_is_empty():
    response = client.patch("/dashboard")
    assert response.status_code == 200
    # assert response.json() == {"msg": "Hello World"}
