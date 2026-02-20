from utils.logger import printf

class PopupHandler:

    @staticmethod
    def enable_appointment_reminder_handler(context):
        drivers = []

        if hasattr(context, "driver") and context.driver:
            drivers.append(context.driver)

        if hasattr(context, "user_drivers") and context.user_drivers:
            drivers.extend(context.user_drivers.values())

        if not drivers:
            printf("PopupHandler: No active drivers found.")
            return

        script = """
        (function() {
            if (window.__reminderObserverInstalled) return;
            window.__reminderObserverInstalled = true;

            const closePopup = () => {
                const btn = document.getElementById("appointment-reminder-close-btn");
                if (btn) btn.click();
            };

            const observer = new MutationObserver(() => closePopup());

            observer.observe(document.body, {
                childList: true,
                subtree: true
            });

            closePopup(); // try immediately too
        })();
        """

        for driver in drivers:
            try:
                driver.execute_script(script)
                printf("PopupHandler: Reminder suppression active.")
            except Exception as e:
                printf(f"PopupHandler failed: {e}")