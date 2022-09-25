from selenium.webdriver.common.by import By

MOS_ENTER = (By.CSS_SELECTOR, "#root > div.style_site_wrapper__3M7Hm.undefined > div.style_main-container__3z5Nv > "
                              "main > section > div > div.style_sec-intro_left__2XBWp > "
                              "div.style_sec-intro_aside__2Be41 > div > div.style_aside-login__3YTaH > "
                              "div.style_aside-login_action__2KJI4 > div")

LOGIN_FORM_LOADING_LOCK = (By.CLASS_NAME, "preloaderScreen__lock")

LOGIN_FIELD = (By.ID, "login")
PASSWORD_FIELD = (By.ID, "password")
MOS_LOGIN = (By.ID, "bind")
