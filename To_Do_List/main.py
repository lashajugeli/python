import argparse
from to_do_manager import (
    load_tasks,
    add_task,
    list_tasks,
    complete_task,
    remove_task,
    edit_task,
    PRIORITY_ORDER
)


def parse_args():
    parser = argparse.ArgumentParser(description="To-Do List CLI (with colors & filters)")
    parser.add_argument('--show', choices=['all', 'pending', 'completed'], help='Which tasks to display')
    parser.add_argument('--sort', choices=['id', 'priority'], help='Sort tasks')
    return parser.parse_args()


def display_menu() -> None:
    print("\n=== დავალებების სია ===")
    print("1. ყველა დავალების ნახვა")
    print("2. დარჩენილი დავალებების ნახვა")
    print("3. დავალების დამატება")
    print("4. დავალების რედაქტირება")
    print("5. დავალების დასრულება")
    print("6. დავალების წაშლა")
    print("7. გასვლა")


def get_choice() -> int:
    try:
        c = int(input("არჩევა (1-7): "))
        if 1 <= c <= 7:
            return c
    except ValueError:
        pass
    print("❌ ცდებოდა. შეიყვანეთ რიცხვი 1-დან 7-მდე.")
    return get_choice()


def prompt_details(edit=False) -> tuple[str, str]:
    label = "ახალი აღწერა" if edit else "აღწერის დამატება"
    desc = input(f"{label}: ").strip()
    if not desc:
        print("❗ აღწერა არ უნდა იყოს ცარიელი.")
        return prompt_details(edit)

    prios = list(PRIORITY_ORDER.keys())
    print("აირჩიეთ პრიორიტეტი:")
    for idx, p in enumerate(prios, start=1):
        print(f"{idx}. {p}")
    try:
        sel = int(input("პირობითი რიცხვი: ")) - 1
        prio = prios[sel]
    except (ValueError, IndexError):
        print("❌ არასწორი პრიორიტეტი.")
        return prompt_details(edit)

    return desc, prio


def main() -> None:
    args = parse_args()
    tasks = load_tasks()

    # Non-interactive mode via flags
    if args.show or args.sort:
        # Filter
        if args.show == 'pending':
            show_completed = False
        else:
            show_completed = True
        # Sort
        if args.sort == 'priority':
            tasks = sorted(tasks, key=lambda x: PRIORITY_ORDER[x[2]])
        list_tasks(tasks, show_completed=show_completed)
        return

    # Interactive menu
    while True:
        display_menu()
        choice = get_choice()
        if choice == 1:
            list_tasks(tasks, show_completed=True)
        elif choice == 2:
            list_tasks(tasks, show_completed=False)
        elif choice == 3:
            d, p = prompt_details()
            add_task(tasks, d, p)
        elif choice == 4:
            try:
                tid = int(input("რედაქტირების ID: "))
                d, p = prompt_details(edit=True)
                edit_task(tasks, tid, d, p)
            except ValueError:
                print("❌ არასწორი ID.")
        elif choice == 5:
            try:
                tid = int(input("დასრულებული ID: "))
                complete_task(tasks, tid)
            except ValueError:
                print("❌ არასწორი ID.")
        elif choice == 6:
            try:
                tid = int(input("წაშლის ID: "))
                remove_task(tasks, tid)
            except ValueError:
                print("❌ არასწორი ID.")
        else:
            print("👋 ნახვამდის!")
            break

if __name__ == "__main__":
    main()