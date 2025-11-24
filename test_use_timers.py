#US3:
#Som en användare 
#vill jag kunna starta, pausa och återställa en timer
#så att jag kan kontrollera tiden för varje enskild aktivitet

'''Acceptanskriterie:
1. Det ska gå att starta en timer genom att klicka på "Start" knappen*
2. När en timer startas ska:
    - Tiden börjar räkna upp eller ner beroende på inställning
    - Knappen ändras till "Pause"
    - Widgetens bakgrundfärg blir ljusare **
3. Det ska gå att pausa en startad timer genom att klicka på en "Pause" knapp
4. När en timer pausas ska:
    - Nedräkningen stoppas
    - Knappen ändras tillbaka till att visa "Start"
    - Widgetens bakgrundsfärg återgår till att vara mörkare/grå**
5. Det ska gå att återställa en timer genom "Reset"-knappen
6. När en timer är återställd ska den visa ursprungsvärdet och vara stoppad
7. Användaren ska kunna ha flera timers aktiva samtidigt
8. Tillståndet för en timer ska vara isolerat och inte påverkas av förändringar i andra timers.'''

#Scenario:
#1. Navigera till webbsidan
#2. Skapa en ny timer genom att klicka på "Add timer"
#2. Starta timern genom att klicka på  "Start"
#3. Kontrollera att:
#   - tiden förändras, räknas upp eller ned
#   - att knappen ändras till Pause
#   - och att timern är i kör-läge
#4. Klicka på knappen "Pause"
#5. Kontrollera att:
#   - tiden slutar förändras
#   - knappen ändras tillbaka till Start
#5. Klicka på "Reset"
#6. Kontrollera att:
#   - timern visar ursprungsvärdet 15:00
#   - timern är i stoppat läge
#8. Skapa en till timer
#9. Starta bägge timers
#10. Kontrollera att:
#   - bägge timers räknar ner eller upp oberoende av varandra
#   - pausa en av dem, den andra ska fortsätta ticka
#   - återställ en av dem, den andra ska inte påverkas

import re
from playwright.sync_api import Page, expect
from test_add_remove_timers import navigate_to_website

def test_start_timer(page: Page):
    navigate_to_website(page)
    add = page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE))
    add.click()
    timer = page.locator(".timer").first

    #Verifierar att startvärdet är 15:00 och att startknappen visas
    expect(timer.locator(".time")).to_have_text("15:00")
    expect(timer.get_by_role("button").get_by_text(re.compile("Start", re.IGNORECASE))).to_be_visible()

    #Klickar på Start
    timer.get_by_role("button").get_by_text(re.compile("Start", re.IGNORECASE)).click()

    #Låter timer ticka i 2.5 sekunder
    page.wait_for_timeout(2500)

    #Förväntas att timer inte längre har ursprungsvärdet, knappen pause visas och timer körs
    expect(timer.locator(".time")).not_to_have_text("15:00")
    expect(timer.get_by_role("button").get_by_text(re.compile("Pause", re.IGNORECASE))).to_be_visible()
    expect(timer).to_have_class(re.compile(r"\brunning\b"))

def test_pause_timer(page: Page):
    navigate_to_website(page)

    #Lägg till en timer
    add = page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE))
    add.click()
    timer = page.locator(".timer").first

    #Starta timern och låt ticka i 2 sekunder
    timer.get_by_role("button").get_by_text(re.compile("Start", re.IGNORECASE)).click()
    page.wait_for_timeout(2000)

    #Pausa timern
    timer.get_by_role("button").get_by_text(re.compile("Pause", re.IGNORECASE)).click()
    #Verifierar att timern är pausad
    expect(timer).to_have_class(re.compile(r"\bpaused\b"))

    #Spara tiden som är vid pausen
    paused_time = timer.locator(".time").inner_text()

    #Vänta i 2 sekunder för att verifiera att tiden inte ändrat sig
    page.wait_for_timeout(2000)
    expect(timer.locator(".time")).to_have_text(paused_time)
    expect(timer.get_by_role("button").get_by_text(re.compile("Start", re.IGNORECASE))).to_be_visible()

def test_reset_timer(page: Page):
    navigate_to_website(page)

    #Lägg till en timer
    add = page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE))
    add.click()
    timer = page.locator(".timer").first

    #Starta timer och låt ticka i 3 sekunder
    timer.get_by_role("button").get_by_text(re.compile("Start", re.IGNORECASE)).click()
    page.wait_for_timeout(3000)
    
    #
    timer.get_by_role("button").get_by_text(re.compile("Reset", re.IGNORECASE)).click()
    expect(timer.locator(".time")).to_have_text("15:00")
    expect(timer.get_by_role("button").get_by_text(re.compile("Start", re.IGNORECASE))).to_be_visible()
    expect(timer).not_to_have_class(re.compile(r"\brunning\b"))

def test_multiple_timers_running_independently(page: Page):
    navigate_to_website(page)

    add = page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE))

    #Lägg till två timers
    add.click()
    add.click()

    timers = page.locator(".timer")

    #Tryck på start på första timern
    timers.nth(0).get_by_role("button").get_by_text(re.compile("Start", re.IGNORECASE)).click()

    #Tryck på start på andra timern
    timers.nth(1).get_by_role("button").get_by_text(re.compile("Start", re.IGNORECASE)).click()

    #Bägge ska visa att de räknar ner tiden
    expect(timers.nth(0)).to_have_class(re.compile(r"\brunning\b"))
    expect(timers.nth(1)).to_have_class(re.compile(r"\brunning\b"))

def test_timer_state_is_isolated(page: Page):
    navigate_to_website(page)

    add = page.get_by_role("button").get_by_text(re.compile("Add timer", re.IGNORECASE))

    #Lägg till två timers
    add.click()
    add.click()

    timers = page.locator(".timer")  

    #Tryck på start på första timern
    timers.nth(0).get_by_role("button").get_by_text(re.compile("Start")).click()

    #Tryck på start på andra timern
    timers.nth(1).get_by_role("button").get_by_text(re.compile("Start")).click()
    #Stanna andra timern
    timers.nth(1).get_by_role("button").get_by_text(re.compile("Pause")).click()

    expect(timers.nth(0)).to_have_class(re.compile(r"\brunning\b"))
    expect(timers.nth(1)).not_to_have_class(re.compile(r"\brunning\b"))