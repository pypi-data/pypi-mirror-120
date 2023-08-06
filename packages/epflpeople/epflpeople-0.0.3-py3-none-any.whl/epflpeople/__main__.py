import sys
import epflpeople


def main():
    search_term = input('Find : ')
    if search_term:
        print(epflpeople.find_all(search_term, format_output=True))


if __name__ == '__main__':
    main()
