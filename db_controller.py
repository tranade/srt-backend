import os
from datetime import datetime
from typing import Any, Mapping

import pymongo
import pytz as pytz
from dotenv import load_dotenv
from pymongo import MongoClient


class DBController:
    def __init__(self):
        load_dotenv()
        self.db = MongoClient(os.getenv("DB_URI"))[os.getenv("DB_NAME")]

    def get_oldest_incomplete_task(self) -> list[Mapping[str, Any] | Any]:
        """
        Gets the oldest incomplete SRT procedure task from the database
        :return: the oldest incomplete SRT procedure task
        """
        pipeline = [
            {
                "$match": {
                    "completionTime": {"$type": "null"}  # Filter incomplete SRT procedures
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
                    "createdAt": pymongo.ASCENDING  # Sort by oldest first
                }
            },
            {
                "$limit": 1  # Only get the oldest task
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

    def mark_task_completed(self, task_id: int):
        """
        Marks a task as completed in the database
        :param task_id: the id of the task to mark as completed
        """
        est = pytz.timezone('US/Eastern')
        completionTime = datetime.now(tz=est)
        self.db["SRTProcedure"].update_one({"_id": task_id}, {"$set": {"completionTime": completionTime}})
