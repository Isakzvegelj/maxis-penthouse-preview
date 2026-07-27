#!/usr/bin/env python3
"""Generate a polished PDF brochure for the Bled Penthouse rental.
Uses fpdf2 (installed) + Pillow. No external assets required.
Output: /Users/isakzvegelj/bled-penthouse/bled-penthouse.pdf
"""
from fpdf import FPDF

ACCENT = (47, 125, 110)      # lake/forest green
ACCENT_D = (34, 92, 81)
GOLD = (201, 161, 74)
INK = (29, 43, 42)
MUTED = (95, 111, 109)
LINE = (226, 232, 230)
LIGHT = (244, 247, 246)
WHITE = (255, 255, 255)

SITE = "https://bled-penthouse.netlify.app"


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(8)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 5, "Bled Penthouse  -  Presernova cesta 15, Bled", align="L")
        self.cell(0, 5, SITE, align="R")
        self.set_draw_color(*LINE)
        self.line(self.l_margin, 15, self.w - self.r_margin, 15)
        self.ln(8)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 6, f"Page {self.page_no()}", align="C")


def clean(s: str) -> str:
    # fpdf core fonts are latin-1; map common unicode
    return (s.replace("·", "-").replace("–", "-").replace("—", "-")
             .replace("✓", "[x]").replace("✗", "[ ]").replace("€", "EUR ")
             .replace("’", "'").replace("“", '"').replace("”", '"')
             .replace("Š", "S").replace("š", "s").replace("Ž", "Z").replace("ž", "z")
             .encode("latin-1", "replace").decode("latin-1"))


def h1(pdf, text):
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*ACCENT_D)
    pdf.multi_cell(0, 8, clean(text))
    pdf.ln(1)


def h2(pdf, text):
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 6, clean(text))
    pdf.ln(0.5)


def body(pdf, text, size=10):
    pdf.set_font("Helvetica", "", size)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 5.2, clean(text))
    pdf.ln(1)


def bullet(pdf, text, size=10):
    pdf.set_font("Helvetica", "", size)
    pdf.set_text_color(*INK)
    x = pdf.get_x()
    pdf.cell(5, 5.2, clean("[x]"))
    pdf.multi_cell(0, 5.2, clean(text))
    pdf.set_x(x)


def chip_row(pdf, items, start_y):
    pdf.set_y(start_y)
    pdf.set_font("Helvetica", "B", 9)
    col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / 3
    for i, (big, small) in enumerate(items):
        col = i % 3
        row = i // 3
        y = start_y + row * 16
        x = pdf.l_margin + col * col_w
        pdf.set_xy(x, y)
        pdf.set_fill_color(*LIGHT)
        pdf.set_draw_color(*LINE)
        pdf.rect(x, y, col_w - 4, 14, "DF")
        pdf.set_xy(x + 3, y + 2)
        pdf.set_text_color(*ACCENT_D)
        pdf.cell(col_w - 10, 5, clean(big))
        pdf.set_xy(x + 3, y + 8)
        pdf.set_text_color(*MUTED)
        pdf.set_font("Helvetica", "", 8)
        pdf.cell(col_w - 10, 4, clean(small))


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.set_margins(18, 18, 18)
pdf.add_page()

# ---------- COVER ----------
pdf.set_fill_color(*ACCENT)
pdf.rect(0, 0, pdf.w, 78, "F")
# gold accent bar
pdf.set_fill_color(*GOLD)
pdf.rect(0, 78, pdf.w, 4, "F")

pdf.set_xy(18, 22)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(*GOLD)
pdf.cell(0, 6, "LAKE BLED - SLOVENIA")

pdf.set_xy(18, 32)
pdf.set_font("Helvetica", "B", 30)
pdf.set_text_color(*WHITE)
pdf.multi_cell(pdf.w - 36, 12, "Bled Penthouse")

pdf.set_xy(18, 56)
pdf.set_font("Helvetica", "", 12)
pdf.set_text_color(*LIGHT)
pdf.multi_cell(pdf.w - 36, 6, "A bright 1-bedroom penthouse, steps from the lake.")

pdf.ln(20)
pdf.set_x(18)
h2(pdf, "Your stay at a glance")
chip_row(pdf, [
    ("1", "Bedroom"),
    ("2", "Guests"),
    ("1", "Bathroom"),
    ("2", "Parking spots"),
    ("~300 EUR", "Per night (season)"),
    ("AC", "Air conditioned"),
], pdf.get_y() + 2)

pdf.ln(40)
pdf.set_x(18)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*ACCENT_D)
pdf.cell(0, 6, "Live now: " + SITE)
pdf.ln(7)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*MUTED)
pdf.multi_cell(0, 5, clean("Prešernova cesta 15, 4260 Bled, Slovenia  ·  Opening soon - enquiries welcome"))
pdf.ln(2)
pdf.set_font("Helvetica", "I", 8)
pdf.multi_cell(0, 4.5, clean("This brochure pairs the live website with full rental details, a photo shot-list for launch, and a guest info card."))

# ---------- PAGE 2: THE APARTMENT + AMENITIES ----------
pdf.add_page()
h1(pdf, "The Apartment")
body(pdf, "Perched on the top floor at Prešernova cesta 15, this one-bedroom penthouse is all warm wood floors, skylights, and a private balcony looking out over gardens and the hills beyond Bled.")
body(pdf, "Wake up to roof windows full of Slovenian light, step onto the balcony with your coffee, and walk to Lake Bled in minutes. After a day of rowing to the island or hiking to the castle, come back to cool air-con, a quiet bedroom, and your own parking spot below.")
body(pdf, "Designed for two - a couple's retreat, a remote-work escape, or a weekend by the water.")

pdf.ln(2)
h2(pdf, "Amenities")
amenities = [
    "Private balcony with garden & hill views",
    "Air conditioning",
    "Free parking for 2 cars",
    "Warm wooden floors",
    "Roof windows / skylights",
    "Mountain & possible lake view",
    "1 bedroom - sleeps 2",
    "1 bathroom",
    "WiFi (to confirm)",
    "No kitchen - please note for guests",
]
for a in amenities:
    bullet(pdf, a)
pdf.ln(3)

# ---------- PAGE 3: LOCATION + PRICING ----------
pdf.add_page()
h1(pdf, "Location")
body(pdf, "Prešernova cesta 15, 4260 Bled, Slovenia")
for l in [
    "Walking distance to Lake Bled shoreline",
    "Walk to Bled Castle & the island",
    "Cafes, bakeries & restaurants nearby",
    "Private parking for 2 cars on site",
    "~35 km from Ljubljana Airport (LJU)",
]:
    bullet(pdf, l)
pdf.ln(2)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*ACCENT_D)
pdf.multi_cell(0, 5, clean("Map: https://www.google.com/maps/search/?api=1&query=Pre%C5%A1ernova+cesta+15+Bled"))

pdf.ln(4)
h1(pdf, "Pricing (suggested)")
price_rows = [
    ("Season (Jun-Sep, Dec hol.)", "~300 EUR / night"),
    ("Shoulder (Apr-May, Oct)", "200-240 EUR / night"),
    ("Low (Nov, Jan-Mar ex hol.)", "150-180 EUR / night"),
    ("Cleaning fee", "40 EUR"),
    ("Min stay", "2 nights (3 in peak)"),
    ("Tourist tax", "~2-3.50 EUR / guest / night"),
    ("Weekly / monthly discount", "7% / 15%"),
]
pdf.set_font("Helvetica", "", 10)
for k, v in price_rows:
    pdf.set_text_color(*INK)
    pdf.cell(95, 7, clean(k))
    pdf.set_text_color(*ACCENT_D)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 7, clean(v))
    pdf.set_font("Helvetica", "", 10)
    pdf.ln(7)
pdf.ln(2)
pdf.set_font("Helvetica", "I", 8)
pdf.set_text_color(*MUTED)
pdf.multi_cell(0, 4.5, clean("Pricing is a starting point - adjust by demand and local competition. Tourist tax is the Slovenia standard and can be collected separately or included."))

# ---------- PAGE 4: LAUNCH PHOTO SHOT-LIST ----------
pdf.add_page()
h1(pdf, "Launch Photo Shot-List (Booking.com)")
body(pdf, "Take these when the build is done. First photo is the hero - make it the best wide shot. Aim for 20-30 bright, landscape photos (min 2000px wide).")
shots = [
    "Hero: wide living area with balcony light",
    "Living room from balcony door angle",
    "Bedroom - bed made, roof-window light",
    "Bedroom detail (wood floor, headboard)",
    "Bathroom - full, clean, bright",
    "Bathroom detail (shower / sink)",
    "Balcony with garden + hill view",
    "Balcony corner / seating",
    "Roof windows / skylight detail",
    "Entrance / hallway to apartment",
    "Parking spot (show 2 spaces)",
    "Building exterior from street",
    "View toward Lake Bled",
    "Neighbourhood / walk to lake",
    "Standout detail (light, wood, view)",
]
for s in shots:
    bullet(pdf, s)
pdf.ln(2)
pdf.set_font("Helvetica", "I", 8)
pdf.set_text_color(*MUTED)
pdf.multi_cell(0, 4.5, clean("Tip: shoot 10:00-15:00 with windows open, no clutter. Add a few lifestyle shots (coffee on balcony, laptop by window)."))

# ---------- PAGE 5: GUEST INFO CARD ----------
pdf.add_page()
h1(pdf, "Guest Info Card (print & leave in apartment)")
info = [
    ("Check-in", "15:00"),
    ("Check-out", "10:00"),
    ("Address", "Prešernova cesta 15, 4260 Bled"),
    ("WiFi", "NETWORK / PASSWORD  (set at handover)"),
    ("Parking", "2 spaces on site - spot numbers ___"),
    ("Guests", "Max 2 - no pets, no smoking"),
    ("No kitchen", "Plan to enjoy Bled's cafes & restaurants"),
    ("Emergency", "112 (EU)  ·  Police 113  ·  Ambulance 112"),
    ("Host contact", "YOUR_NAME - YOUR_PHONE"),
    ("House rules", "Quiet after 22:00 · leave tidy · lock up"),
]
LM = pdf.l_margin
val_w = pdf.w - pdf.r_margin - (LM + 42)
for k, v in info:
    pdf.set_x(LM)
    pdf.set_text_color(*ACCENT_D)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(42, 7, clean(k))
    pdf.set_text_color(*INK)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(LM + 42, pdf.get_y())
    pdf.multi_cell(val_w, 7, clean(v))
pdf.ln(3)
pdf.set_fill_color(*LIGHT)
pdf.set_draw_color(*LINE)
box_y = pdf.get_y()
pdf.rect(pdf.l_margin, box_y, pdf.w - 36, 34, "DF")
pdf.set_xy(pdf.l_margin + 4, box_y + 4)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*ACCENT_D)
pdf.cell(0, 6, "Nearby favourites")
pdf.set_xy(pdf.l_margin + 4, box_y + 12)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*INK)
pdf.multi_cell(pdf.w - 44, 4.6, clean("- Lake Bled promenade & rowing to the island\n- Bled Castle viewpoint\n- Vintgar Gorge (short drive)\n- Triglav National Park trails"))

out = "/Users/isakzvegelj/bled-penthouse/bled-penthouse.pdf"
pdf.output(out)
print("WROTE", out)
