import os
import pytest
import dotenv

dotenv.read_dotenv()

if __name__ == "__main__":
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "dce_course_admin.settings"
    )
    pytest.main('tests')
