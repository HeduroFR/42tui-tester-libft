#!/usr/bin/env python3
import json
import pathlib
import subprocess
import sys
import tempfile

image = sys.argv[1] if len(sys.argv) > 1 else '42tui-tester-libft-local'
with tempfile.TemporaryDirectory(prefix='libft-report-') as tmp:
    project = pathlib.Path(tmp)
    (project / 'ft_isalpha.c').write_text('int ft_isalpha(int c) { return (c >= 65 && c <= 90) || (c >= 97 && c <= 122); }\n')
    (project / 'Makefile').write_text('all:\n\tcc -c ft_isalpha.c -o ft_isalpha.o\n\tar rcs libft.a ft_isalpha.o\nbonus: all\n')
    def run(*args):
        return subprocess.run(['docker', 'run', '--rm', '--network', 'none', '--mount', f'type=bind,source={tmp},target=/project', image, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120)
    result = run('--report', '/project/report.json')
    assert result.returncode == 1, result.stderr.decode(errors='replace')
    report = json.loads((project / 'report.json').read_text())
    assert report['version'] == 1 and report['passed'] > 0 and report['failed'] > 0
    assert report['total'] == sum(report[key] for key in ('passed', 'failed', 'errors', 'skipped'))
    assert run('--report', '/project/report.json').returncode == 2
    (project / 'ft_isalpha.c').write_text('int ft_isalpha(int c) { (void)c; return 0; }\n')
    assert run('--report', '/project/wrong.json').returncode == 1
    wrong = json.loads((project / 'wrong.json').read_text())
    assert wrong['failed'] > report['failed'] and wrong['passed'] < report['passed']
    (project / 'Makefile').write_text('all:\n\tfalse\nbonus:\n\tfalse\n')
    assert run('--report', '/project/failed.json').returncode == 2
    assert not (project / 'failed.json').exists()
print('Container report checks passed')
