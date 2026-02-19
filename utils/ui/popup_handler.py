from utils.logger import printf

class PopupHandler:

    @staticmethod
    def inject_appointment_reminder_killer(driver):
        try:
            driver.execute_script("""
            setInterval(() => {
              let btn = document.getElementById("appointment-reminder-close-btn");
              if (btn) btn.click();
            }, 1000);
            """)
            printf("Appointment reminder auto-close handler enabled.")
        except Exception as e:
            printf(f"Failed to inject popup handler: {e}")