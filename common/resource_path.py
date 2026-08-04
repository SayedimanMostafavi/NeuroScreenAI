import os
import sys


def resource_path(relative_path):

    if getattr(sys, "frozen", False):

        base_path = getattr(
            sys,
            "_MEIPASS",
            os.path.dirname(sys.executable),
        )

    else:

        base_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
            )
        )

    return os.path.join(
        base_path,
        relative_path,
    )
