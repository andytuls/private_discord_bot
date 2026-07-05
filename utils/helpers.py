def progress_bar(current: int, total: int, length: int = 10) -> str:
    if total == 0:
        return "█" * length
    filled = int(round((current / total) * length))
    empty = length - filled
    return "█" * filled + "░" * empty