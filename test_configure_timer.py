#US:
#Som en användare
#vill jag kunna konfigurera varje timers titel, tidsinställning,upp-eller nedräkning
#så att jag kan anpassa mina timers för den specifika aktiviteten

#Acceptans:
#1. Användaren ska kunna ändra tidsinställning på timern
#2. Användaren ska kunna ändra titel på timern genom att klicka på rubriken
#3. Användaren ska kunna ändra om timern ska räkna upp eller ned och standardvärdet ska vara nedräkning.
#4. Om uppräkning används på timern ska det inte gå att konfigurera tid.
#5. Användaren ska kunna konfigurera om timern även ska visa tiondelar, standardvärde är av, ändringen ska gälla under pågående nedräkning eller uppräkning
#
#Scenario:
#1. Navigera till webbsidan
#2. Skapa en timer med knappen "Add timer"
#3. Klicka på ikonen kugghjulet för att göra förändringar 
#3. Kontrollera att läget är nedräkning som standard
#4. Kontrollera att inmatningsfältet är upplåst när "counting down" är valt
#5. Kontrollera att det inte visas tiondelar som standard
#6. Skriv i en tid i inmatningsfältet
#7. Klicka på knappen "Reset" och kontrollera att den nya tiden visas som timer
#8. Ändra inställningen för växlingsknappen för "counting down" 
#9. Klicka på knappen "Reset"
#10. Verifiera att:
#   - inskrivningsfältet för tid inte går att skriva i
#   - timern är 00:00 och pausad
#10. Ändra inställningen med växlingsknappen för "Hide tenth"
#11. Verifiera att timer visar minuter:sekunder:tiondelar
#12. Klicka på timer titeln "Break" och ändra titel (titel sparas när du klickar utanför rutan eller använder Enter)
#13. Verifiera att titeln sparas när du startar timern

import re
from test_add_remove_timers import navigate_to_website
from playwright.sync_api import Page, expect

def test_default_timer_settings(page: Page):
    navigate_to_website(page)

    #Klickar på knappen "Add timer"
    page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE)).click()

    timers = page.locator(".timer")

    #Ta första timern på sidan och klicka på inställningarna
    first_timer = timers.nth(0)
    first_timer.locator(".icon.settings").click()    
    
    #Verifiera att standard är att timer räknas ned, det går att skriva in tid och tiondelar inte är på
    countdown_toggle_on = page.locator(".on-off.on")
    time_input = page.locator('input[type="text"]').nth(1)
    show_tenth_hide = page.locator(".on-off").nth(1)

    expect(countdown_toggle_on).to_be_visible()
    expect(time_input).to_be_enabled()
    expect(show_tenth_hide).to_be_visible()

def test_changing_time_on_timer(page: Page):
    navigate_to_website(page)

    #Klickar på knappen "Add timer"
    page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE)).click()

    timers = page.locator(".timer")

    #Ta första timern på sidan och klicka på inställningarna
    first_timer = timers.nth(0)
    first_timer.locator(".icon.settings").click()

    #Skriv in ny tid i inmatningsfältet
    time_input = page.locator('input[type="text"]').nth(1)
    time_input.fill("30")

    #Verifiera att texten i fältet har ändrats
    expect(time_input).to_have_value("30")

    #Klicka på knappen "Reset"
    page.get_by_role("button").get_by_text(re.compile("Reset", re.IGNORECASE)).click()

    #Verifiera att timern har ändrat tid
    expect(first_timer.locator(".time")).to_have_text("30:00")

def test_change_timer_to_count_down(page: Page):
    navigate_to_website(page)

    #Klickar på knappen "Add timer"
    page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE)).click()

    timers = page.locator(".timer")

    #Ta första timern på sidan och klicka på inställningarna
    first_timer = timers.nth(0)
    first_timer.locator(".icon.settings").click()

    countdown_toggle_on = page.locator(".on-off.on")
    countdown_toggle_on.click()

    expect(countdown_toggle_on).not_to_be_visible()

    expect(first_timer.locator(".time")).to_have_text("00:00")
    expect(first_timer).to_have_class(re.compile(r"\bpaused\b"))

    page.get_by_role("button").get_by_text(re.compile("Start", re.IGNORECASE)).click()
    page.wait_for_timeout(3000)
    expect(first_timer.locator(".time")).to_have_text(re.compile("00:03"))


def test_show_timer_with_tenth(page: Page):
    navigate_to_website(page)

    #Klickar på knappen "Add timer"
    page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE)).click()

    #Hämtar alla timers
    timers = page.locator(".timer")

    #Ta första timern på sidan och klicka på inställningarna
    first_timer = timers.nth(0)
    first_timer.locator(".icon.settings").click()

    show_tenth = page.locator(".on-off").nth(1)
    show_tenth.click()

    expect(show_tenth).to_be_visible()
    expect(first_timer.locator(".time")).to_have_text(re.compile(r"\d{2}:\d{2}.\d{1}"))

def test_change_title_on_timer_with_enter(page: Page):
    navigate_to_website(page)

    #Klickar på knappen "Add timer"
    page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE)).click()

    #Hämtar alla timers
    timers = page.locator(".timer")
    first_timer = timers.nth(0)

    #Hittar timerns titel genom rubriken och klickar på den
    title_heading = first_timer.locator('h3')
    title_heading.click()

    #Gör input fältet synligt och väntar på att det visas
    title_input = first_timer.locator('input[placeholder="Title"]')
    expect(title_input).to_be_visible()

    #Tar bort befintlig titel och lägger till en ny
    title_input.clear()
    title_input.fill("Test of timer")

    #Klicka enter för att spara titeln och stänga input fältet
    title_input.press("Enter")

    #Verifier att titel är ändrad och att fältet inte är öppet
    expect(title_heading).to_have_text("Test of timer 🖊️ ")
    expect(title_input).to_be_hidden()

    #Starta timern och låt ticka i 2 sekunder
    first_timer.get_by_role("button").get_by_text(re.compile("Start", re.IGNORECASE)).click()
    page.wait_for_timeout(2000)

    expect(title_heading).to_have_text("Test of timer 🖊️ ")