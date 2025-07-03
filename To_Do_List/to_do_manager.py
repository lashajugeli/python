import os
from typing import List, Tuple
from colors import RED, YELLOW, GREEN, RESET

# ფაილის მდებარეობა და პრიორიტეტების წესრიგი
TASKS_DIR = "To_DO_List"
TASKS_FILE = os.path.join(TASKS_DIR, "tasks.txt")
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# ფერადი გამოსახულებათა რუკა
COLOR_MAP = {"high": RED, "medium": YELLOW, "low": GREEN}

STATUS_EMOJIS = {False: "⏳", True: "✅"}


def ensure_dir() -> None:
    """Create tasks directory if missing."""
    os.makedirs(TASKS_DIR, exist_ok=True)


def load_tasks() -> List[Tuple[int, str, str, bool]]:
    """Load tasks from two-line formatted file."""
    ensure_dir()
    tasks: List[Tuple[int, str, str, bool]] = []
    if not os.path.exists(TASKS_FILE):
        return tasks
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        i = 0
        while i < len(lines):
            line1 = lines[i].strip()
            if not line1.startswith('['):
                i += 1
                continue
            # [ID] Description
            tid_str, desc = line1.split('] ', 1)
            tid = int(tid_str.strip('['))
            line2 = lines[i+1].strip()
            # category: prio | is_complete: True
            parts = [p.strip() for p in line2.split('|')]
            prio = parts[0].split(':', 1)[1].strip()
            done_str = parts[1].split(':', 1)[1].strip()
            done = True if done_str == 'True' else False
            tasks.append((tid, desc, prio, done))
            i += 2
    except IOError as err:
        print(f"⛔ შეცდომა ფაილის ჩატვირთვაში: {err}")
    return tasks


def save_tasks(tasks: List[Tuple[int, str, str, bool]]) -> None:
    """Save tasks with two-line format."""
    ensure_dir()
    try:
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            for tid, desc, prio, done in tasks:
                f.write(f"[{tid}] {desc}\n")
                f.write(f"    category: {prio} | is_complete: {done}\n")
    except IOError as err:
        print(f"⛔ შეცდომა შესანახად: {err}")


def add_task(tasks, description: str, priority: str) -> None:
    next_id = tasks[-1][0] + 1 if tasks else 1
    tasks.append((next_id, description, priority, False))
    save_tasks(tasks)
    print(f"✔ დავალება დაემატა: {description}")


def list_tasks(tasks, show_completed: bool = True) -> None:
    """Print tasks with ANSI colors."""
    filtered = [t for t in tasks if show_completed or not t[3]]
    if not filtered:
        print("📭 დავალებები არ მოიძებნა.")
        return
    for tid, desc, prio, done in filtered:
        color = COLOR_MAP.get(prio, RESET)
        status = STATUS_EMOJIS[done]
        print(f"{color}[{tid}] {desc}{RESET}")
        print(f"{color}    category: {prio} | is_complete: {done}{RESET}")


def complete_task(tasks, task_id: int) -> None:
    for i, (tid, desc, prio, done) in enumerate(tasks):
        if tid == task_id:
            if done:
                print("ℹ️ დავალება უკვე დასრულებულია.")
            else:
                tasks[i] = (tid, desc, prio, True)
                save_tasks(tasks)
                print(f"✅ დასრულდა: {desc}")
            return
    print("❌ დავალება ვერ მოიძებნა.")


def remove_task(tasks, task_id: int) -> None:
    for i, (tid, desc, prio, done) in enumerate(tasks):
        if tid == task_id:
            tasks.pop(i)
            # IDs გადამოცემა
            tasks[:] = [(idx+1, t[1], t[2], t[3]) for idx, t in enumerate(tasks)]
            save_tasks(tasks)
            print(f"🗑️ წაიშალა: {desc}")
            return
    print("❌ დავალება ვერ მოიძებნა.")


def edit_task(tasks, task_id: int, new_desc: str, new_prio: str) -> None:
    for i, (tid, desc, prio, done) in enumerate(tasks):
        if tid == task_id:
            tasks[i] = (tid, new_desc, new_prio, done)
            save_tasks(tasks)
            print(f"✏️ ამოცანის ცვლილება: {new_desc} ({new_prio})")
            return
    print("❌ დავალება ვერ მოიძებნა.")