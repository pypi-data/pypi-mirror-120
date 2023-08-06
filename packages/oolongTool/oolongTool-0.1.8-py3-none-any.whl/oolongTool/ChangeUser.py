import pexpect
import argparse
import sys

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', type=str, required=True)
    parser.add_argument('-p', '--password', type=str, required=True)
    parser.add_argument('-c', '--command', type=str, required=True)
    parser.add_argument('-e', '--expect', type=list, default=['-*Best result.*'])
    args = parser.parse_args()
    return args

def change_user(user, password, command, expect=['-*Best result.*']):
    command = command.replace(',', ' ')
    child = pexpect.spawn(f'su {user}', encoding='utf-8', logfile=sys.stdout)
    # child.sendline('su {}'.format(user_name))
    index = child.expect('Password:')
    if index == 0:
        child.sendline(password)
        # child.sendline('cd ~')
        child.sendline(command)
        child.expect(expect, timeout=None)
            
    

def main():
    args = parse()
    change_user(args.user, args.password, args.command, args.expect)



if __name__ == "__main__":
    main()