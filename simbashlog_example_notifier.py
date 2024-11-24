#!/usr/bin/env python3

# TODO: Add some notes about the notifier
'''
NOTES:

For more information:
- ...
'''

import sys
from enum import Enum
import simbashlog_notify_helper as snh # type: ignore

# simbashlog-notifier specific imports
# TODO: Add your own imports
#import ...

'''
Try to avoid modifying the following:
- SIMBASHLOG_NOTIFIER_NAME
- NotifierConfigField
- load_config
- create_message
- perform_action
'''

# TODO: Replace the value with the name of your notifier but keep the prefix 'simbashlog-' and the suffix '-notifier'
SIMBASHLOG_NOTIFIER_NAME = "simbashlog-example-notifier"

class NotifierConfigField(Enum):
    # TODO: Here you should add your own configuration fields based on the `setup.py` function `NotifierConfig.get_data_for_config_file()`
    # General
    MIN_REQUIRED_LOG_LEVEL = "min_required_log_level"
    SHOW_IN_CONSOLE_SENT_MESSAGE = "show_in_console_sent_message"
    # Header
    SHOW_IN_HEADER_PID = "show_in_header_pid"
    # Body
    SHOW_IN_BODY_LOG_FILE_RESULT = "show_in_body_log_file_result"
    SHOW_IN_BODY_LOG_FILE_CONTENT = "show_in_body_log_file_content"
    SHOW_IN_BODY_SUMMARY_FOR_PID = "show_in_body_summary_for_pid"
    SHOW_IN_BODY_SUMMARY_FOR_LOG_FILE = "show_in_body_summary_for_log_file"
    # Footer
    SHOW_IN_FOOTER_LOG_FILE_NAMES = "show_in_footer_log_file_names"
    SHOW_IN_FOOTER_HOST = "show_in_footer_host"
    SHOW_IN_FOOTER_NOTIFIER_NAME = "show_in_footer_notifier_name"

    # Notifier specific
    EXAMPLE_KEY = "example_key"

    def __str__(self):
        return self.value

def load_config() -> snh.NotifierConfig:
    try:
        config_data = snh.NotifierConfig.get_data(SIMBASHLOG_NOTIFIER_NAME, NotifierConfigField)
    except Exception as e:
        print(f"An error occurred while the config file was being processed:\n{e}")
        sys.exit(1)

    return snh.NotifierConfig(
        # TODO: Don't forget to adjust the configuration based on the `NotifierConfigField` enum
        # General
        min_required_log_level=config_data[
            NotifierConfigField.MIN_REQUIRED_LOG_LEVEL.value
        ],
        show_in_console_sent_message=config_data[
            NotifierConfigField.SHOW_IN_CONSOLE_SENT_MESSAGE.value
        ].lower() == "true",

        # Header
        show_in_header_pid=config_data[
            NotifierConfigField.SHOW_IN_HEADER_PID.value
        ].lower() == "true",

        # Body
        show_in_body_log_file_result=config_data[
            NotifierConfigField.SHOW_IN_BODY_LOG_FILE_RESULT.value
        ].lower() == "true",
        show_in_body_log_file_content=config_data[
            NotifierConfigField.SHOW_IN_BODY_LOG_FILE_CONTENT.value
        ].lower() == "true",
        show_in_body_summary_for_pid=config_data[
            NotifierConfigField.SHOW_IN_BODY_SUMMARY_FOR_PID.value
        ].lower() == "true",
        show_in_body_summary_for_log_file=config_data[
            NotifierConfigField.SHOW_IN_BODY_SUMMARY_FOR_LOG_FILE.value
        ].lower() == "true",

        # Footer
        show_in_footer_log_file_names=config_data[
            NotifierConfigField.SHOW_IN_FOOTER_LOG_FILE_NAMES.value
        ].lower() == "true",
        show_in_footer_host=config_data[
            NotifierConfigField.SHOW_IN_FOOTER_HOST.value
        ].lower() == "true",
        show_in_footer_notifier_name=config_data[
            NotifierConfigField.SHOW_IN_FOOTER_NOTIFIER_NAME.value
        ].lower() == "true",

        # Notifier specific
        example_key=config_data[
            NotifierConfigField.EXAMPLE_KEY.value
        ]
    )

def get_min_required_log_level(config: snh.NotifierConfig) -> int:
    # TODO: Remove the logic below and return 7 if nothing should be filtered
    if config.min_required_log_level is not None:
        min_required_log_level = int(config.min_required_log_level)
        
        if not min_required_log_level in range(0, 8):
            print(f"Invalid minimum required log level'{min_required_log_level}'")
            sys.exit(1)

        return min_required_log_level

    return 7

def create_message(config: snh.NotifierConfig, stored_log_info: snh.StoredLogInfo) -> str:
    builder = snh.MessageBuilder(
        stored_log_info = stored_log_info,
        notifier_name = SIMBASHLOG_NOTIFIER_NAME,
        # TODO: Replace the lambda functions with your own formatting
        apply_heading = lambda content: f"{content}",
        apply_subheading = lambda content: f"\n{content}\n",
        apply_paragraph = lambda content: f"\n{content}\n",
        apply_code = lambda content: f"\n{content}\n",
        apply_bold = lambda content: f"{content}",
        apply_italic = lambda content: f"{content}"
    )

    builder.add_header(
        show_pid=config.show_in_header_pid
    ).add_body(
        show_log_file_result=config.show_in_body_log_file_result,
        show_log_file_content=config.show_in_body_log_file_content,
        show_summary_for_pid=config.show_in_body_summary_for_pid,
        show_summary_for_log_file=config.show_in_body_summary_for_log_file
    ).add_footer(
        show_log_file_names=config.show_in_footer_log_file_names,
        show_host=config.show_in_footer_host,
        show_notifier_name=config.show_in_footer_notifier_name
    )

    return builder.build()

def perform_action(config: snh.NotifierConfig, message: str):
    # TODO: Here you can add your own action
    if config.show_in_console_sent_message:
        print(message)

# ░░░░░░░░░░░░░░░░░░░░░▓▓▓░░░░░░░░░░░░░░░░░░░░░░
# ░░                                          ░░
# ░░                                          ░░
# ░░      DO NOT MODIFY ANYTHING BELOW!       ░░
# ░░                                          ░░
# ░░                                          ░░
# ░░░░░░░░░░░░░░░░░░░░░▓▓▓░░░░░░░░░░░░░░░░░░░░░░

@snh.unexpected_exception_handler
def notify(config: snh.NotifierConfig, stored_log_info: snh.StoredLogInfo):
    # Check if there are any log entries
    if len(stored_log_info.data_df) == 0:
        print("No matching log entries found. Nothing to notify.")
        sys.exit(0)

    # Create message
    message = create_message(config, stored_log_info)

    # Perform action
    perform_action(config, message)

@snh.unexpected_exception_handler
def filter_log_data_by_min_required_log_level(config: snh.NotifierConfig, stored_log_info: snh.StoredLogInfo) -> None:
    min_required_log_level = get_min_required_log_level(config)

    if min_required_log_level == 7:
        return

    # TODO: Remove this line
    print(stored_log_info)

    initial_count = len(stored_log_info.data_df)

    stored_log_info.data_df[snh.DataFrameField.SEVERITY_CODE.value] = stored_log_info.data_df[snh.LogField.LEVEL.value].apply(
        lambda level_name: snh.Severity.get_by_name(level_name).rfc_5424_numerical_code
    )

    stored_log_info.data_df.drop(
        stored_log_info.data_df[stored_log_info.data_df[snh.DataFrameField.SEVERITY_CODE.value] > min_required_log_level].index,
        inplace=True
    )

    stored_log_info.data_df.drop(columns=[snh.DataFrameField.SEVERITY_CODE.value], inplace=True)

    final_count = len(stored_log_info.data_df)

    # Set summary to 0 if the severity is greater than the minimum required log level
    for column in stored_log_info.summary_df.columns:
        try:
            severity_code = snh.Severity.get_by_name(column).rfc_5424_numerical_code
            if severity_code > min_required_log_level:
                stored_log_info.summary_df[column] = 0
        except AttributeError:
            continue

    # TODO: Remove this line
    print(stored_log_info)

    if initial_count != final_count:
        print(f"Removed {initial_count - final_count} log entries with severity greater than {min_required_log_level} (Original count: {initial_count} | Final count: {final_count})")

@snh.unexpected_exception_handler
def main():
    # Load configuration
    config = load_config()

    # Process command-line arguments
    stored_log_info = snh.process_arguments()

    # Filter log data by minimum required log level
    filter_log_data_by_min_required_log_level(config, stored_log_info)

    # Notify
    notify(config, stored_log_info)

if __name__ == "__main__":
    main()