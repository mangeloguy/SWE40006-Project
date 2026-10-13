# SQLite 部署历史集成测试骨架（brief 1.3 / 1.4）
# 依赖 app 同学先实现「部署历史」的写入与读取功能，当前以 skip 占位，
# 避免功能未落地时导致 CI 失败。功能落地后：删除下方 pytestmark 并补全真实断言。
#
# 期望的 app 侧契约（供 app 同学对齐，具体接口以最终实现为准）：
#   1. 每次部署写入一条记录：Git commit hash、时间戳、环境(environment)。
#   2. 记录持久化到 SQLite，文件路径由 DB_PATH 环境变量指定（DECISIONS.md 1.3）。
#   3. 提供读取历史的能力，按时间倒序返回，供页面展示部署历史。
import pytest

pytestmark = pytest.mark.skip(reason="依赖 app 的 SQLite 部署历史功能尚未实现")


def test_deployment_record_is_persisted():
    """写入一条部署记录后，应能从 SQLite 读回一致的 commit、环境与时间。"""


def test_deployment_history_is_ordered():
    """历史记录应按时间倒序返回，最新部署在前。"""


def test_db_path_env_var_controls_location():
    """修改 DB_PATH 后，记录应写入到指定文件路径。"""