from glob import glob
import subprocess

from util import timing


@timing
def benchmark_file(file):
    print(f"benchmarking file:{file}")
    subprocess.run(["python", file], stdout=subprocess.DEVNULL)


def benchmark_all():
    days = glob("day*.py")
    for day in sorted(days):
        benchmark_file(day)


if __name__ == "__main__":
    benchmark_all()