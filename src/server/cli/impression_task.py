from typing import Optional, Callable
from datetime import datetime, timedelta
import colorama as col


class ImpressionTask:
    MAX_CENTER: int = 50
    MESSAGE_SUCCESS_DEFAULT: str = "Task successfully completed!"

    def __init__(
        self,
        title: str,
        subtitle: Optional[str] = None,
        debug: bool = False
    ) -> None:
        self.__title: str = title
        self.__subtitle: str = subtitle
        self.__debug: bool = debug

    def __print_head(self):
        print(col.Back.MAGENTA + col.Fore.WHITE)
        print('[', f' {self.__title} '.center(ImpressionTask.MAX_CENTER, '-'), ']')
        print('|', ''.center(ImpressionTask.MAX_CENTER, ' '), '|')

        if self.__subtitle:
            print('[', f' {self.__subtitle} '.center(ImpressionTask.MAX_CENTER, ' '), ']')

        print('[', ''.center(ImpressionTask.MAX_CENTER, '-'), ']')

    def __print_timer(
        self,
        initial_time: datetime,
        end_time: datetime
    ) -> None:
        interval: timedelta = end_time - initial_time

        print(col.Back.BLUE + col.Fore.WHITE)
        print('[', f' TIMER '.center(ImpressionTask.MAX_CENTER, '-'), ']')
        print('|', ''.center(ImpressionTask.MAX_CENTER, ' '), '|')
        print('|', f' INITIAL TIME: {initial_time} '.center(ImpressionTask.MAX_CENTER, ' '), '|')
        print('|', f' END TIME: {end_time} '.center(ImpressionTask.MAX_CENTER, ' '), '|')
        print('|', f' INTERVAL: {interval} '.center(ImpressionTask.MAX_CENTER, ' '), '|')
        print('|', ''.center(ImpressionTask.MAX_CENTER, ' '), '|')
        print('[', f''.center(ImpressionTask.MAX_CENTER, '-'), ']')

    def __print_message_sucess(self) -> None:
        print(col.Back.GREEN + col.Fore.WHITE)
        print('[', f' SUCESS '.center(ImpressionTask.MAX_CENTER, '-'), ']')
        print('|', ''.center(ImpressionTask.MAX_CENTER, ' '), '|')
        print('|', f'{ImpressionTask.MESSAGE_SUCCESS_DEFAULT}'.center(ImpressionTask.MAX_CENTER, ' '), '|')
        print('[', ''.center(ImpressionTask.MAX_CENTER, '-'), ']')

    def __print_message_error(self, exception: Exception) -> None:
        print(col.Back.RED + col.Fore.WHITE)
        print('|', f' ERROR '.center(ImpressionTask.MAX_CENTER, '-'), '|')
        print('|', ''.center(ImpressionTask.MAX_CENTER, ' '), '|')
        print('|', f' {exception} '.center(ImpressionTask.MAX_CENTER, ' '), '|')
        print('|', ''.center(ImpressionTask.MAX_CENTER, ' '), '|')
        print('|', ''.center(ImpressionTask.MAX_CENTER, '-'), '|')

    def __formatter_default(self) -> None:
        print(col.Fore.BLACK + col.Style.BRIGHT)

    def __clear_formatter(self) -> None:
        print(col.Back.RESET + col.Fore.RESET)

    def print(self, call: Callable) -> None:
        col.init()

        self.__formatter_default()

        self.__print_head()

        initial_time: datetime = datetime.now()

        try:
            call()

        except Exception as error:
            self.__print_message_error(error)

            if self.__debug:
                raise error

        else:
            self.__print_message_sucess()

        finally:
            end_time: datetime = datetime.now()

            self.__print_timer(initial_time, end_time)

            self.__clear_formatter()