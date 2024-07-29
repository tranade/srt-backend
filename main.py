import time
from datetime import datetime
import pytz

from db_controller import DBController
from email_controller import EmailController
from srt_controller import SrtController


def main():
    db = DBController()
    emailClient = EmailController()
    while True:
        time.sleep(60)
        db.sendServiceCheckinToDB()
        
        est = pytz.timezone('US/Eastern')
        current_time = datetime.now(tz=est).replace(second=0, microsecond=0)
        task = db.get_tasks_scheduled_before_now(current_time)
        
        if len(task) > 0:
            print("Running SRT process")
            db.mark_task_started(task[0]["_id"], current_time)
            srt = SrtController(task[0], emailClient)
            srt.create_run_file()
            srt.run_process()
            result_paths = srt.get_paths_of_results()
            emailClient.send_results_to_user(result_paths, task[0]["userEmail"], task[0]["userName"])
            db.mark_task_completed(task[0]["_id"])


if __name__ == "__main__":
    main()
