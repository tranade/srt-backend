import os
from datetime import datetime
from typing import Any, Mapping

import pymongo
import pytz
from dotenv import load_dotenv
from pymongo import MongoClient


class DBController:
    def __init__(self):
        load_dotenv()
        self.db = MongoClient(os.getenv("DB_URI"))[os.getenv("DB_NAME")]

    def get_tasks_scheduled_before_now(self, current_time: datetime) -> list[Mapping[str, Any] | Any]:
        """
        Gets the tasks scheduled to start before or at the current time
        :param current_time: the current time to check against scheduledTime
        :return: the tasks scheduled to start before or at the current time
        """
        pipeline = [
            {
                "$match": {
                    "completionTime": {"$type": "null"},
                    "scheduledTime": {"$lte": current_time}
                }
            },
            {
                "$lookup": {
                    "from": "User",
                    "localField": "userId",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {
                "$unwind": "$user"
            },
            {
                "$sort": {
                    "scheduledTime": pymongo.ASCENDING
                }
            },
            {
                "$limit": 1
            },
            {
                "$project": {
                    "_id": 1,
                    "completionTime": 1,
                    "instructions": 1,
                    "userId": "$user._id",
                    "userName": "$user.fullName",
                    "userEmail": "$user.email",
                }
            }
        ]
        task = list(self.db["SRTProcedure"].aggregate(pipeline))  # Get the first (and only) task
        return task

    def mark_task_started(self, task_id: int, start_time: datetime):
        """
        Marks a task as started in the database
        :param task_id: the id of the task to mark as started
        :param start_time: the time the task started
        """
        self.db["SRTProcedure"].update_one({"_id": task_id}, {"$set": {"startedAt": start_time}})

    def mark_task_completed(self, task_id: int):
        """
        Marks a task as completed in the database
        :param task_id: the id of the task to mark as completed
        """
        est = pytz.timezone('US/Eastern')
        completionTime = datetime.now(tz=est)
        self.db["SRTProcedure"].update_one({"_id": task_id}, {"$set": {"completionTime": completionTime}})

    def sendServiceCheckinToDB(self):
        """
        Sends a service checkin to the database
        """
        est = pytz.timezone('US/Eastern')
        checkInTime = datetime.now(tz=est)
        self.db["SRTCheckin"].insert_one({"checkInTime": checkInTime})
