from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import logging
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from automations.tasks import send_status_notifications, check_overdue_tasks

logger = logging.getLogger(__name__)

class AutomationScheduler:
    """Class to manage scheduled automation tasks"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.configure_scheduler()
        
    def configure_scheduler(self):
        """Configure and add jobs to the scheduler"""
        # Example: Send status notifications every day at 9am
        self.scheduler.add_job(
            send_status_notifications,
            CronTrigger(hour=9, minute=0),
            id='daily_notifications',
            replace_existing=True
        )
        
        # Example: Check for overdue tasks every hour
        self.scheduler.add_job(
            check_overdue_tasks,
            IntervalTrigger(hours=1),
            id='check_overdue',
            replace_existing=True
        )
        
        logger.info("Scheduler configured with automation jobs")
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Automation scheduler started")
            
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Automation scheduler shut down")
            
    def add_job(self, func, trigger, **kwargs):
        """Add a new job to the scheduler"""
        self.scheduler.add_job(func, trigger, **kwargs)
        logger.info(f"Added new job: {kwargs.get('id', 'unnamed')}")
        
    def remove_job(self, job_id):
        """Remove a job from the scheduler"""
        self.scheduler.remove_job(job_id)
        logger.info(f"Removed job: {job_id}")
        
    def get_jobs(self):
        """Get all scheduled jobs"""
        return self.scheduler.get_jobs() 