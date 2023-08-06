from .auto import *
import click
import sys
from os import system
from random import choice

developer = {"name": "정지효 (Jung Ji-Hyo)", "email": "cord0318@gmail.com", "age": "13"}
key = {"right":"v", "left":"x"}

def check_version():
    version = "0.0.11"
    click.echo("autoclick " + version)

cmd_list = ["contact", "developer (개발자)", "friend (도와준 친구)"]

def print_menu():
    system("cls")
    for i in range(len(cmd_list)):
        click.echo(f"[{i}] " + cmd_list[i])

def cmd():
    print_menu()
    cmd = int(input("> "))
    if cmd == 0:
        try:
            discord_message = ["(Please buy me Discord NITRO...)", "(Please send me message!)", "(Please send me friend)"]
            system("cls")
            click.echo("My Discord : 정지효#6521 " + choice(discord_message))
            click.echo("My Email : cord0318@gmail.com")
            system("cls")
            system("auto")

        except Exception as e:
            click.echo("알수 없는 오류가 나타났습니다.\n오류 코드 : " + e)
            system("cls")
            system("auto")
    elif cmd == 1:
        system("cls")
        for dev in developer:
            click.echo(f"{dev} : {developer[dev]}")
        click.echo("\n")
    elif cmd == 2:
        system("cls")
        click.echo("이 개발을 도와준 '위정우'에게 감사움을 표합니다.\n")
        system("cls")
        system("auto")

def set_key(key_type, key_val):
    global key
    if key_type == "right":
        key["right"] = key_val
        click.echo("Set AutoClick right key '{}'".format(key["right"]))
    else:
        key["left"] = key_val
        click.echo("Set AutoClick left key '{}'".format(key["left"]))

@click.option('--delay', "--start", type=click.FLOAT, default=0.04, help='Start AutoClick.')
@click.option("-v", '--version', is_flag=True, help="Show version of this Program.")
@click.option("--command", "--cmd", is_flag=True, help="Open the autoclick cmd.")
@click.option("--right_key", "--right", type=click.STRING, help="Set AutoClick right key.")
@click.option("--left_key", "--left", type=click.STRING, help="Set AutoClick left key.")
@click.option("--check_key", is_flag=True, help="Check AutoClick Key.")
@click.command()
def main(delay, right_key, left_key, check_key, version, command):
    global key
    if check_key:
        click.echo("right key : {}\nleft key : {}".format(key["right"], key["left"]))
        sys.exit()
    if left_key:
        set_key("left", left_key)
        sys.exit()
        
    if right_key:
        set_key("right", right_key)
        sys.exit()

    if version:
        check_version()
        sys.exit()
    if command:
        cmd()
        sys.exit()

    if delay:
        click.echo("Your delay : " + str(delay))
        click.echo("start autoclick . . .")
        auto_click = AutoClick(delay=delay, right_key=key["right"], left_key=key["left"])
        auto_click.run_autoclick()

if __name__ == '__main__':
    main()