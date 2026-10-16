
import pytest

pytestmark = pytest.mark.skip(reason="依赖 app 的 SQLite 部署历史功能尚未实现")


def test_deployment_record_is_persisted():
    """写入一条部署记录后，应能从 SQLite 读回一致的 commit、环境与时间。"""


def test_deployment_history_is_ordered():
    """历史记录应按时间倒序返回，最新部署在前。"""


def test_db_path_env_var_controls_location():
    """修改 DB_PATH 后，记录应写入到指定文件路径。"""