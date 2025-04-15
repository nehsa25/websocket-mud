import sys
import traceback

class ExceptionUtils:
    def print_exception(e):
        """Prints useful information about an exception, including type, line number, and filename."""
        exc_type, exc_obj, exc_tb = sys.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        lineno = exc_tb.tb_lineno
        error_message = f"Exception Type: {exc_type}\n"
        error_message += f"File Name: {filename}\n"
        error_message += f"Line Number: {lineno}\n"
        error_message += f"Exception: {e}\n"

        if isinstance(exc_obj, OSError):
            error_message += f"OSError Errno: {exc_obj.errno}\n"
            error_message += f"OSError Filename: {exc_obj.filename}\n"
            error_message += f"OSError Strerror: {exc_obj.strerror}\n"
        elif isinstance(exc_obj, AttributeError):
            error_message += f"AttributeError Name: {getattr(exc_obj, 'name', 'N/A')}\n"

        error_message += traceback.format_exc()
        return error_message