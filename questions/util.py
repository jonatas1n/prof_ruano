def format_time(time):
    return f"{int(time // 3600):02d}:{int(time % 3600 // 60):02d}:{int(time % 60):02d}s"
