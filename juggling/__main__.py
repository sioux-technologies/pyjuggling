import argparse

from juggling.application import Application
from juggling.configuration import Configuration


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--amount", required=True,
                        help="Amount of juggling balls that should de detected, for example, 2.")
    parser.add_argument("-c", "--colors", required=False,
                        help="HSV Color ranges for detection, for example, in case of "
                             "orange balls \"[[(10, 100, 120), (25, 255, 255)]]\".")

    arguments = vars(parser.parse_args())

    amount_string = arguments.get('amount', None)
    if amount_string is not None:
        amount = int(amount_string)
        Configuration().set_amount(amount)

    ranges_string = arguments.get('colors', None)
    if ranges_string is not None:
        ranges = eval(ranges_string)
        Configuration().set_color_ranges(ranges)

    application = Application()
    application.start()


if __name__ == "__main__":
    main()
