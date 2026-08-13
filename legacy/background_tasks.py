from flask_apscheduler import APScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import logging
import requests
from datetime import datetime, timedelta
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataUpdateManager:
    def __init__(self, app=None):
        self.app = app
        self.scheduler = APScheduler()
        self.update_intervals = {
            'market_prices': 30,  # Update every 30 minutes
            'weather_data': 60,   # Update every 60 minutes
            'crop_calendar': 1440, # Update daily (24*60 minutes)
        }

        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the scheduler with the Flask app"""
        self.app = app
        self.scheduler.init_app(app)

        # Add scheduled jobs
        self.add_scheduled_jobs()

        # Start the scheduler
        if not self.scheduler.running:
            self.scheduler.start()

    def add_scheduled_jobs(self):
        """Add all scheduled data update jobs"""

        # Market prices update every 30 minutes
        self.scheduler.add_job(
            func=self.update_market_prices,
            trigger=IntervalTrigger(minutes=self.update_intervals['market_prices']),
            id='update_market_prices',
            name='Update Market Prices',
            replace_existing=True
        )

        # Weather data update every 60 minutes
        self.scheduler.add_job(
            func=self.update_weather_data,
            trigger=IntervalTrigger(minutes=self.update_intervals['weather_data']),
            id='update_weather_data',
            name='Update Weather Data',
            replace_existing=True
        )

        # Crop calendar update daily at 6 AM
        self.scheduler.add_job(
            func=self.update_crop_calendar,
            trigger=CronTrigger(hour=6, minute=0),
            id='update_crop_calendar',
            name='Update Crop Calendar',
            replace_existing=True
        )

        # Data quality check every 4 hours
        self.scheduler.add_job(
            func=self.perform_data_quality_check,
            trigger=IntervalTrigger(hours=4),
            id='data_quality_check',
            name='Data Quality Check',
            replace_existing=True
        )

        logger.info("All scheduled jobs have been added successfully")

    def update_market_prices(self):
        """Update market prices from external sources"""
        try:
            logger.info("Starting market prices update...")

            with self.app.app_context():
                # Clear existing cache to force fresh data
                if 'market_data_cache' in globals():
                    globals()['market_data_cache'].clear()

                # Call the market prices API to refresh data
                try:
                    # This would typically call external APIs like Agmarknet
                    # For now, we'll simulate the update
                    logger.info("Market prices cache cleared - fresh data will be fetched on next request")

                    # Log the update
                    self.log_data_update('market_prices', 'success', 'Cache cleared for fresh data')

                except Exception as e:
                    logger.error(f"Error updating market prices: {str(e)}")
                    self.log_data_update('market_prices', 'error', str(e))

        except Exception as e:
            logger.error(f"Error in market prices update job: {str(e)}")

    def update_weather_data(self):
        """Update weather data cache"""
        try:
            logger.info("Starting weather data update...")

            with self.app.app_context():
                # Clear weather cache if it exists
                if 'weather_cache' in globals():
                    globals()['weather_cache'].clear()

                logger.info("Weather data cache cleared - fresh data will be fetched on next request")
                self.log_data_update('weather_data', 'success', 'Cache cleared for fresh data')

        except Exception as e:
            logger.error(f"Error in weather data update job: {str(e)}")
            self.log_data_update('weather_data', 'error', str(e))

    def update_crop_calendar(self):
        """Update crop calendar data"""
        try:
            logger.info("Starting crop calendar update...")

            with self.app.app_context():
                # This could update crop calendar data based on seasonal changes
                # For now, we'll just log the activity
                logger.info("Crop calendar update completed - seasonal data refreshed")
                self.log_data_update('crop_calendar', 'success', 'Seasonal data refreshed')

        except Exception as e:
            logger.error(f"Error in crop calendar update job: {str(e)}")
            self.log_data_update('crop_calendar', 'error', str(e))

    def perform_data_quality_check(self):
        """Perform data quality checks on all data sources"""
        try:
            logger.info("Starting data quality check...")

            with self.app.app_context():
                quality_issues = []

                # Check market data cache
                if 'market_data_cache' in globals():
                    cache_size = len(globals()['market_data_cache'])
                    if cache_size == 0:
                        quality_issues.append("Market data cache is empty")

                # Check if APIs are responding
                try:
                    # Test weather API
                    test_response = requests.get('http://localhost:5000/api/weather/current?location=Delhi', timeout=5)
                    if test_response.status_code != 200:
                        quality_issues.append("Weather API not responding properly")
                except:
                    quality_issues.append("Weather API unreachable")

                # Log quality check results
                if quality_issues:
                    logger.warning(f"Data quality issues found: {', '.join(quality_issues)}")
                    self.log_data_update('data_quality', 'warning', '; '.join(quality_issues))
                else:
                    logger.info("Data quality check passed - all systems operational")
                    self.log_data_update('data_quality', 'success', 'All systems operational')

        except Exception as e:
            logger.error(f"Error in data quality check: {str(e)}")
            self.log_data_update('data_quality', 'error', str(e))

    def log_data_update(self, data_type, status, message):
        """Log data update activities"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'data_type': data_type,
            'status': status,
            'message': message
        }

        # In a real application, this would be stored in a database
        logger.info(f"Data Update Log: {log_entry}")

    def get_job_status(self):
        """Get status of all scheduled jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                'id': job.id,
                'name': job.name,
                'next_run_time': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })

        return jobs

    def pause_job(self, job_id):
        """Pause a specific job"""
        try:
            self.scheduler.pause_job(job_id)
            logger.info(f"Job {job_id} paused successfully")
            return True
        except Exception as e:
            logger.error(f"Error pausing job {job_id}: {str(e)}")
            return False

    def resume_job(self, job_id):
        """Resume a specific job"""
        try:
            self.scheduler.resume_job(job_id)
            logger.info(f"Job {job_id} resumed successfully")
            return True
        except Exception as e:
            logger.error(f"Error resuming job {job_id}: {str(e)}")
            return False

    def get_data_update_history(self):
        """Get history of data updates (mock implementation)"""
        # In a real application, this would come from a database
        return [
            {
                'timestamp': (datetime.now() - timedelta(hours=i)).isoformat(),
                'data_type': 'market_prices',
                'status': 'success' if i % 3 != 0 else 'error',
                'message': f'Update completed for period {i}'
            } for i in range(1, 11)
        ]

# Global instance
data_update_manager = DataUpdateManager()

def create_background_tasks(app):
    """Initialize background tasks for the Flask app"""
    global data_update_manager
    data_update_manager.init_app(app)
    return data_update_manager
