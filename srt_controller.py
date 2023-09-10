import os
import subprocess
from dotenv import load_dotenv

from data_classes.srt_procedure import SRTProcedure
from email_controller import EmailController


class SrtController:
    def __init__(self, task: dict[str, any], emailClient: EmailController):
        load_dotenv()
        self.srtn_dir = os.getenv("SRTN_FILE_DIR")
        self.config_filename = os.getenv("CONFIG_FILENAME")
        self.config_output_dir = os.getenv("CONFIG_OUTPUT_FILE_DIR")
        self.procedure = SRTProcedure.from_dict(**task)
        self.email = emailClient

    def run_process(self) -> int:
        """
        Runs the srt process. Emails the srt admin if there is an error.

        NOTE: This function blocks until the srt process exits

        :return: the exit code of the srt process or -1 if there is an error
        """
        try:
            srt_process = subprocess.Popen("./srtn", cwd=self.srtn_dir, stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL, shell=True, preexec_fn=os.setsid)
            exit_code = srt_process.wait()
            return exit_code
        except Exception as e:
            self.email.send_error(contents=[f"Error running SRT process:\n {e}"])
            return -1

    def create_run_file(self) -> None:
        """
        Creates a run file for the srt process to read from. Emails the srt admin if there is an error.

        :return: None
        """
        instructions = self.procedure.generate_instruction_str_list()
        try:
            config_file_path = os.path.join(self.config_output_dir, self.config_filename)
            if not os.path.exists(self.config_output_dir):
                os.makedirs(self.config_output_dir)
            if os.path.exists(config_file_path):
                os.remove(config_file_path)
            with open(config_file_path, "w+") as f:
                for line in instructions:
                    f.write(line + "\n")
        except Exception as e:
            self.email.send_error(contents=[f"Error running SRT process:\n {e}"])

    @staticmethod
    def get_paths_of_results() -> list[str]:
        """
        Gets the paths of the results of the srt process

        :return: the paths of the results of the srt process
        """
        return [os.path.join(os.getenv("CONFIG_OUTPUT_FILE_DIR"), filename) for filename in
                os.listdir(os.getenv("CONFIG_OUTPUT_FILE_DIR"))]
