import sys
import traceback

class ExceptionUtils:
    def print_exception(e):
        """Prints useful information about an exception, including type, line number, and filename."""
        exc_type, exc_obj, exc_tb = sys.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        lineno = exc_tb.tb_lineno
        print(f"Exception Type: {exc_type}")
        print(f"File Name: {filename}")
        print(f"Line Number: {lineno}")
        print(f"Exception: {e}")

        if isinstance(exc_obj, OSError):
            print(f"OSError Errno: {exc_obj.errno}")
            print(f"OSError Filename: {exc_obj.filename}")
            print(f"OSError Strerror: {exc_obj.strerror}")
        elif isinstance(exc_obj, AttributeError):
            print(f"AttributeError Name: {exc_obj.name}")

        traceback.print_exc() 