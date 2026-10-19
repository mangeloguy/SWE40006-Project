from html import escape
from string import Template

PAGE = Template("""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="10">
<title>Build status dashboard</title>
<style>
  body { font-family: Arial, Helvetica, sans-serif; color: #222; background: #fff; margin: 0; line-height: 1.5; }
  main { max-width: 720px; margin: 0 auto; padding: 24px 16px 48px; }
  header { border-bottom: 3px solid #c8102e; padding-bottom: 8px; margin-bottom: 20px; }
  h1 { font-size: 28px; margin: 0; }
  .sub { color: #666; margin: 2px 0 0; }
  code { font-family: Consolas, "Courier New", monospace; font-size: 1.25em; background: #eee; padding: 1px 6px; }
  .ok { color: #2e7d32; }
  .bad { color: #c62828; }
  h2 { font-size: 20px; margin: 32px 0 8px; }
  .table-wrap { overflow-x: auto; }
  table { border-collapse: collapse; width: 100%; }
  th, td { border: 1px solid #999; padding: 6px 10px; text-align: left; }
  th { background: #eee; }
  td.hash { font-family: Consolas, "Courier New", monospace; }
  .note { color: #666; font-size: 14px; margin-top: 24px; }
</style>
</head>
<body>
<main>
  <header>
    <h1>Build status dashboard test</h1>
    <p class="sub">SWE40006 project, Group 02</p>
  </header>
  <p>This is the <strong>$environment</strong> environment. It is running commit <code>$commit</code>, built at $build_time.</p>
  <p>Status: <strong class="$status_class">$status_text</strong></p>
  <h2>Recent deployments</h2>
  <div class="table-wrap">
    <table>
      <tr><th>Commit</th><th>Environment</th><th>Built</th><th>Deployed</th></tr>
      $rows
    </table>
  </div>
  <p class="note">This page refreshes every 10 seconds.</p>
</main>
</body>
</html>
""")


def render_dashboard(info: dict, history: list[dict]) -> str:
    healthy = info.get("status") == "ok"
    rows = "".join(
        "<tr>"
        f"<td class='hash'>{escape(str(r['commit_hash']))}</td>"
        f"<td>{escape(str(r['environment']))}</td>"
        f"<td>{escape(str(r['build_time']))}</td>"
        f"<td>{escape(str(r['deployed_at']))}</td>"
        "</tr>"
        for r in history
    )
    if not rows:
        rows = "<tr><td colspan='4'>No deployments recorded yet.</td></tr>"
    return PAGE.substitute(
        status_text="Healthy" if healthy else "Unhealthy",
        status_class="ok" if healthy else "bad",
        environment=escape(str(info.get("environment", "unknown"))),
        commit=escape(str(info.get("commit", "unknown"))),
        build_time=escape(str(info.get("build_time", "unknown"))),
        rows=rows,
    )