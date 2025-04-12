import logging
import sys

from pymongo import monitoring

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class CustomCommandListener(monitoring.CommandListener):
    def started(self, event):
        print(f"[Mongo Command] Started: {event.command_name} with {event.command}")

    def succeeded(self, event):
        print(f"[Mongo Command] Succeeded: {event.command_name} in {event.duration_micros}μs")

    def failed(self, event):
        print(f"[Mongo Command] Failed: {event.command_name} with {event.failure}")
