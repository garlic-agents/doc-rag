def check_user_intention(hint_text: str) -> bool:
    while True:
        user_input = input(f"{hint_text} (y/n): ").strip().lower()
        if user_input in {'y', 'n'}:
            return user_input == 'y'
        else:
            print("无效输入，请输入 'y' 或 'n'。")