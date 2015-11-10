import subprocess

def map(commands):
    processes = [subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                 for cmd in commands]
    results = []
    for proc in processes:
        try:
            outs, errs = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        results.append((proc.returncode, outs, errs))
    return results
