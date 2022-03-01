def test_profile_representation(profile):
    assert profile.__str__() == f"{profile.user.username}'s profile"
