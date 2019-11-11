import argparse

from juggling.application import Application
from juggling.configuration import Configuration


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--amount", required=True, type=int,
                        help="Amount of juggling balls that should de detected, for example, 2.")
    parser.add_argument("-s", "--simulate", required=False, action='store_true',
                        help="Simulate circles.")
    parser.add_argument("-r", "--resolution", required=False, type=str, default="1280x720",
                        help="Camera resolution (by default 1280x720).")
    parser.add_argument("-p", "--play", required=False, type=str,
                        help="Use video file instead of camera.")
    parser.add_argument("-o", "--output", required=False, type=str, default=None,
                        help="File name where output video stream is written (by default is not specified).")
    parser.add_argument("-d", "--delay", required=False, type=int, default=1,
                        help="Delay for camera between frames in case of camera or playing file (by default 1 ms).")
    parser.add_argument("-c", "--colors", required=False,
                        help="HSV Color ranges for detection, for example, in case of "
                             "orange balls \"[[(10, 100, 120), (25, 255, 255)]]\".")

    arguments = vars(parser.parse_args())

    amount_string = arguments.get('amount', None)
    if amount_string is not None:
        amount = int(amount_string)
        Configuration().set_amount(amount)

    simulation = arguments.get('simulate', False)
    Configuration().set_simulation_state(simulation)

    play_file = arguments.get('play', None)
    Configuration().set_play_file(play_file)

    output_file = arguments.get('output', None)
    Configuration().set_output_file(output_file)

    resolution = arguments.get('resolution')
    Configuration().set_resolution(resolution)

    delay = arguments.get('delay')
    Configuration().set_delay(delay)

    ranges_string = arguments.get('colors', None)
    if ranges_string is not None:
        ranges = eval(ranges_string)
        Configuration().set_color_ranges(ranges)

    application = Application()
    application.start()


if __name__ == "__main__":
    main()
