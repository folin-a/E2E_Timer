#Test of timers from the website

#US
#Som användare
#vill jag kunna skapa och ta bort timers
#så att jag kan mäta tiden för flera aktiviterer samtidigt

'''Acceptanskriterie:
1. Användaren ska kunna skapa en ny timer genom att klicka på en knapp "Add timer"
2. När en timer skapas ska den visas på webbsidan med standardvärdet 15:00 minuter
    - Första timern lägger sig högst upp på sidan
    - Efterföljande timers läggs under den första i skapandeordning som standard
3. Användaren ska kunna ta bort en timer via papperskorgs-ikonen kopplad till varje widget
4. När en timer tas bort ska den försvinna från gränssnittet
'''
#Testscenario:
#1. Navigera till webbsidan
#2. Skapa en timer
#3. Kontrollera att timer visas med standardvärdet i minuter och sekunder
#4. Skapa flera timers
#5. Kontrollera att  de lägger sig i rätt ordning, första högst upp och de andra under den första
#6. Ta bort en timer via papperskorgsikonen
#7. Kontrollera att timern tas bort
#
import re
from playwright.sync_api import Page, expect

def navigate_to_website(page: Page):
    page.goto("https://lejonmanen.github.io/timer-vue/")

def test_create_timer(page: Page):
    #Anropar funktionen för navigering till webbsidan
    navigate_to_website(page)

    #Klickar på knappen "Add timer" 
    page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE)).click()

    #Hittar en klass med namn timer och kontrollerar att en timer visas
    timers = page.locator(".timer")
    expect(timers).to_have_count(1)

    expect(timers.first.locator(".time")).to_have_text("15:00")

def test_create_multiple_timers_in_order(page: Page):
    navigate_to_website(page)
    add = page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE))

    #Lägg till tre timers
    add.click()
    add.click()
    add.click()

    #Verifiera att tre timers har skapats
    timers = page.locator(".timer")
    expect(timers).to_have_count(3)

    #Kontrollera att de kommer i visad ordning
    expect(timers.nth(0).locator(".time")).to_have_text("15:00")
    expect(timers.nth(1).locator(".time")).to_have_text("15:00")
    expect(timers.nth(2).locator(".time")).to_have_text("15:00")

def test_user_can_delete_timer(page: Page):
    navigate_to_website(page)

    add = page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE))

    #Lägg till två timers
    add.click()
    add.click()

    #Verifiera att det finns 2 timers
    timers = page.locator(".timer")
    expect(timers).to_have_count(2)

    #Ta bort första timern
    first_timer = timers.nth(0)
    first_timer.locator(".icon.close").click()

    #Förväntas att det finns 1 timer kvar
    expect(page.locator(".timer")).to_have_count(1)



