import time

from db_controller import DBController
from email_controller import EmailController
from srt_controller import SrtController


def main():
    db = DBController()
    emailClient = EmailController()
    FIVE_MINUTES = 5 * 60
    while True:
        time.sleep(60)
        db.sendServiceCheckinToDB()
        task = db.get_oldest_incomplete_task()
        if len(task) > 0:
            print("Running SRT process")
            srt = SrtController(task[0], emailClient)
            srt.create_run_file()
            srt.run_process()
            result_paths = srt.get_paths_of_results()
            emailClient.send_results_to_user(result_paths, task[0]["userEmail"], task[0]["userName"])
            db.mark_task_completed(task[0]["_id"])


if __name__ == "__main__":
    main()
