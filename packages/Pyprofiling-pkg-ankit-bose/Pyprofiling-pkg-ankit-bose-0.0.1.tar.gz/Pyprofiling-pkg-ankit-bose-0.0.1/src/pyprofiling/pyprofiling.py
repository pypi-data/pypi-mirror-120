import line_profiler
import atexit

def profiler():
    profile = line_profiler.LineProfiler()
    atexit.register(profile.print_stats)
    return profile