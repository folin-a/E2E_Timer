##US
#Som användare
#vill jag kunna skapa och ta bort anteckningar
#så att jag kan skriva ner och organisera informationen

#Acceptanskriterier
#1. Användaren ska kunna skapa en anteckning via en knapp eller ikon som är tydligt markerad.
#2. När en anteckning skapas ska en ruta visas direkt i gränssnittet med en förifylld text.
#3. Användaren ska kunna skriva text i anteckningen utan några begränsningar som stoppar tangentbordet.
#4. Användaren ska kunna ta bort en anteckning via en knapp/ikon kopplad till just den anteckningen.
#5. När en anteckning tas bort ska den försvinna från gränssnittet omedelbart.
#6. Flera anteckningar ska kunna existera samtidigt och visas oberoende av varandra.

import re
from test_add_remove_timers import navigate_to_website
from playwright.sync_api import Page, expect

def test_create_note_default_text(page: Page):
    navigate_to_website(page)

    add_note = page.get_by_role("button").get_by_text(re.compile("Add note", re.IGNORECASE))
    add_note.click()

    notes = page.locator(".note")
    first_note = notes.nth(0)

    #Hittar timerns titel genom rubriken och klickar på den
    title_heading = first_note.locator('h3')

    expect(add_note).to_be_visible()
    expect(title_heading).to_have_text(re.compile("Click to change text", re.IGNORECASE))

def test_change_title_on_note(page: Page):
    navigate_to_website(page)

    #Klickar på knappen "Add note"
    page.get_by_role("button").get_by_text(re.compile("Add note", re.IGNORECASE)).click()

    #Hämtar alla timers, ta första
    notes = page.locator(".note")
    first_note = notes.nth(0)

    #Hittar anteckningens titel genom rubriken och klickar på den
    title_heading_note = first_note.locator('h3')
    title_heading_note.click()

    #Gör input fältet synligt och väntar på att det visas
    title_input_note = first_note.locator('input[placeholder="Description"]')
    expect(title_input_note).to_be_visible()

    #Tar bort befintlig titel och lägger till en ny
    title_input_note.clear()
    title_input_note.fill("Test of note")

    #Klicka Enter för att spara titeln och stänga input fältet
    title_input_note.press("Enter")

    #Verifier att titel är ändrad och att fältet inte är öppet
    expect(title_heading_note).to_have_text("Test of note")
    expect(title_input_note).to_be_hidden() 

def test_user_can_remove_note(page: Page):
    navigate_to_website(page)

    add_note = page.get_by_role("button").get_by_text(re.compile("Add note", re.IGNORECASE))

    #Lägg till två anteckningar
    add_note.click()
    add_note.click()

    #Verifiera att det finns 2 anteckningar
    notes = page.locator(".note")
    expect(notes).to_have_count(2)

    #Ta bort första anteckningen
    first_note = notes.nth(0)
    first_note.locator(".icon.close").click()

    #Förväntas att det finns 1 anteckning kvar
    expect(page.locator(".note")).to_have_count(1)

def test_add_multiple_notes(page: Page):
    navigate_to_website(page)
    add_note = page.get_by_role("button").get_by_text(re.compile("Add note", re.IGNORECASE))

    #Lägg till tre timers
    add_note.click()
    add_note.click()
    add_note.click()

    #Verifiera att tre timers har skapats
    notes = page.locator(".note")
    expect(notes).to_have_count(3)
    first_note = notes.nth(0)
    second_note = notes.nth(1)
    third_note =  notes.nth(2)

    #Kontrollera att de kommer i visad ordning
    expect(first_note).to_have_text(re.compile("Click to change text", re.IGNORECASE))
    expect(second_note).to_have_text(re.compile("Click to change text", re.IGNORECASE))
    expect(third_note).to_have_text(re.compile("Click to change text", re.IGNORECASE))